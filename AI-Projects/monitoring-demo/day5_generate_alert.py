import csv
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding="utf-8")

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

def find_sustained_drift(timestamps, latencies, baseline_avg, start_index,
                         threshold_pct=0.20, sustain_minutes=60, interval_minutes=5):
    """
    Returns:
      - trigger_index: first index where sustained drift begins, or None
      - sustain_points: number of points needed to qualify
    """
    sustain_points = sustain_minutes // interval_minutes
    consecutive = 0

    for i in range(start_index, len(latencies)):
        pct_above = (latencies[i] - baseline_avg) / baseline_avg

        if pct_above >= threshold_pct:
            consecutive += 1
        else:
            consecutive = 0

        if consecutive >= sustain_points:
            trigger_index = i - sustain_points + 1
            return trigger_index, sustain_points

    return None, sustain_points

def build_alert_message(metric_name, baseline_avg, trigger_time, trigger_latency,
                        trigger_pct, duration_minutes, latest_latency, latest_pct):
    lines = []
    lines.append("ALERT: Early Warning - Latency Drift Detected")
    lines.append("")
    lines.append(f"- Metric: {metric_name}")
    lines.append(f"- Baseline (healthy avg): {baseline_avg:.2f} ms")
    lines.append(f"- Drift started: {trigger_time.isoformat()}")
    lines.append(f"- Drift at start: {trigger_latency:.2f} ms ({trigger_pct:.2f}% above baseline)")
    lines.append(f"- Sustained for: {duration_minutes} minutes")
    lines.append(f"- Current level: {latest_latency:.2f} ms ({latest_pct:.2f}% above baseline)")
    severity = "HIGH" if latest_pct >= 30 else "MEDIUM"
    lines.append(f"- Severity: {severity}")
    lines.append("")
    lines.append("Why it matters:")
    lines.append("- Gradual drift often precedes customer-facing slowness and incident escalation.")
    lines.append("")
    lines.append("Suggested checks (first 10 minutes):")
    lines.append("- Recent deploys/releases in the last 6 to 12 hours")
    lines.append("- Downstream dependency latency (DB, cache, third-party APIs)")
    lines.append("- Traffic/usage pattern changes (new batch job, campaign, cron spike)")
    lines.append("- Resource saturation (CPU/memory), thread pools, queue depth")
    return "\n".join(lines)

def main():
    input_file = "latency_metrics.csv"
    metric_name = "p95_latency_ms"

    # 1) Load data
    timestamps, latencies = read_latency_csv(input_file)
    if not latencies:
        print("No data found. Make sure latency_metrics.csv exists.")
        return

    # 2) Baseline = Day 1 (first half of dataset)
    midpoint_index = len(latencies) // 2
    baseline_avg = average(latencies[:midpoint_index])

    # 3) Detect drift in Day 2
    threshold_pct = 0.20
    sustain_minutes = 60
    interval_minutes = 5

    trigger_index, sustain_points = find_sustained_drift(
        timestamps=timestamps,
        latencies=latencies,
        baseline_avg=baseline_avg,
        start_index=midpoint_index,
        threshold_pct=threshold_pct,
        sustain_minutes=sustain_minutes,
        interval_minutes=interval_minutes
    )

    print("=== Monitoring Demo: Day 5 (Alert Generation) ===")
    print(f"Baseline (Day 1 avg): {baseline_avg:.2f} ms")
    print(f"Rule: >= {threshold_pct*100:.0f}% above baseline for {sustain_minutes} minutes")
    print("")

    if trigger_index is None:
        print("✅ No sustained drift detected. If you expected drift, lower threshold to 15% or reduce sustain_minutes.")
        return

    # 4) Compute alert details
    trigger_time = timestamps[trigger_index]
    trigger_latency = latencies[trigger_index]
    trigger_pct = ((trigger_latency - baseline_avg) / baseline_avg) * 100

    duration_minutes = sustain_points * interval_minutes

    latest_latency = latencies[-1]
    latest_pct = ((latest_latency - baseline_avg) / baseline_avg) * 100

    # 5) Build alert message
    alert_text = build_alert_message(
        metric_name=metric_name,
        baseline_avg=baseline_avg,
        trigger_time=trigger_time,
        trigger_latency=trigger_latency,
        trigger_pct=trigger_pct,
        duration_minutes=duration_minutes,
        latest_latency=latest_latency,
        latest_pct=latest_pct
    )

    # 6) Print the alert
    print(alert_text)

if __name__ == "__main__":
    main()
