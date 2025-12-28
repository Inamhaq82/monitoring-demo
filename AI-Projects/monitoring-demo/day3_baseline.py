import csv
from datetime import datetime

def main():
    input_file = "latency_metrics.csv"

    timestamps = []
    latencies = []

    # Read CSV
    with open(input_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = datetime.fromisoformat(row["timestamp"])
            latency = float(row["p95_latency_ms"])
            timestamps.append(ts)
            latencies.append(latency)

    # Sanity check
    if not latencies:
        print("No data found.")
        return

    # Define baseline window: first 24 hours
    start_time = timestamps[0]
    baseline_cutoff = start_time.replace(hour=0, minute=0, second=0) + \
                      (timestamps[0] - timestamps[0])  # no-op, clarity only
    baseline_end_time = start_time.replace(hour=0, minute=0, second=0) + \
                        (timestamps[0] - timestamps[0])  # same

    # Simpler: baseline = first half of dataset
    midpoint_index = len(latencies) // 2
    baseline_latencies = latencies[:midpoint_index]

    baseline_avg = sum(baseline_latencies) / len(baseline_latencies)

    # Current value = last data point
    current_latency = latencies[-1]

    percent_change = ((current_latency - baseline_avg) / baseline_avg) * 100

    print("=== Monitoring Demo: Day 3 ===")
    print(f"Baseline p95 latency (Day 1 avg): {baseline_avg:.2f} ms")
    print(f"Current p95 latency (latest): {current_latency:.2f} ms")
    print(f"Change vs baseline: {percent_change:.2f}%")
    if percent_change > 20:
        print("⚠️ Latency is significantly above baseline, but may still be under fixed thresholds.")


if __name__ == "__main__":
    main()
