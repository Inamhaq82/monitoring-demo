import csv
from datetime import datetime

def read_latency_csv(path: str):
    timestamps = []
    latencies = []
    with open(path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.append(datetime.fromisoformat(row["timestamp"]))
            latencies.append(float(row["p95_latency_ms"]))
    return timestamps, latencies

def average(values):
    return sum(values) / len(values) if values else 0.0

def main():
    input_file = "latency_metrics.csv"

    # 1) Load data
    timestamps, latencies = read_latency_csv(input_file)
    if not latencies:
        print("No data found. Make sure latency_metrics.csv exists.")
        return

    # 2) Define baseline as Day 1 (first 24 hours)
    midpoint_index = len(latencies) // 2  # first half = day 1, second half = day 2
    baseline_latencies = latencies[:midpoint_index]
    baseline_avg = average(baseline_latencies)

    # 3) Detection parameters (simple and explainable)
    threshold_pct = 0.15         # 20% above baseline
    sustain_minutes = 30         # must sustain for 60 minutes
    data_interval_minutes = 5    # known from our dataset design
    sustain_points = sustain_minutes // data_interval_minutes  # 12 points for 60 minutes

    # 4) Scan Day 2 for sustained drift
    start_scan_index = midpoint_index  # start of Day 2

    consecutive = 0
    first_trigger_index = None

    for i in range(start_scan_index, len(latencies)):
        current = latencies[i]
        pct_above = (current - baseline_avg) / baseline_avg  # e.g., 0.25 means +25%

        if pct_above >= threshold_pct:
            consecutive += 1
        else:
            consecutive = 0  # reset if we drop below threshold

        # If we've sustained long enough and haven't recorded first trigger, record it
        if consecutive >= sustain_points and first_trigger_index is None:
            first_trigger_index = i - sustain_points + 1
            break

    # 5) Print results
    print("=== Monitoring Demo: Day 4 (Drift Detection) ===")
    print(f"Baseline (Day 1 avg): {baseline_avg:.2f} ms")
    print(f"Threshold: +{threshold_pct*100:.0f}% for {sustain_minutes} minutes ({sustain_points} points)")

    if first_trigger_index is None:
        print("✅ No sustained drift detected (with current settings).")
        return

    trigger_time = timestamps[first_trigger_index]
    trigger_latency = latencies[first_trigger_index]
    trigger_pct = ((trigger_latency - baseline_avg) / baseline_avg) * 100

    print("⚠️ Sustained latency drift detected!")
    print(f"First trigger time: {trigger_time.isoformat()}")
    print(f"Latency at trigger: {trigger_latency:.2f} ms")
    print(f"Above baseline at trigger: {trigger_pct:.2f}%")
    # Show the 60-minute window that caused the trigger (proof it is sustained)
    print("--- Trigger window (first 12 points = 60 minutes) ---")
    for j in range(first_trigger_index, first_trigger_index + sustain_points):
        t = timestamps[j].isoformat()
        val = latencies[j]
        pct = ((val - baseline_avg) / baseline_avg) * 100
        print(f"{t}  {val:.2f} ms  ({pct:.2f}% above baseline)")

    # Optional: also show latest values (end of Day 2)
    latest_latency = latencies[-1]
    latest_pct = ((latest_latency - baseline_avg) / baseline_avg) * 100
    print("---")
    print(f"Latest latency: {latest_latency:.2f} ms ({latest_pct:.2f}% above baseline)")
    
    print("")
    print("Business meaning:")
    print("This detects gradual degradation early, before fixed threshold alerts and before users complain.")


if __name__ == "__main__":
    main()
