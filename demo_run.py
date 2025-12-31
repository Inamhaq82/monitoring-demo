import csv
import sys
from datetime import datetime
from email_notifier import send_email

# Ensure clean output on Windows
sys.stdout.reconfigure(encoding="utf-8")

DATA_FILE = "latency_metrics.csv"
METRIC_NAME = "p95_latency_ms"

THRESHOLD_PCT = 0.20        # 20% above baseline
SUSTAIN_MINUTES = 60
INTERVAL_MINUTES = 5


def read_data(path):
    timestamps = []
    latencies = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamps.append(datetime.fromisoformat(row["timestamp"]))
            latencies.append(float(row[METRIC_NAME]))
    return timestamps, latencies


def average(values):
    return sum(values) / len(values)


def find_sustained_drift(timestamps, latencies, baseline_avg):
    sustain_points = SUSTAIN_MINUTES // INTERVAL_MINUTES
    start_index = len(latencies) // 2  # Day 2
    consecutive = 0

    for i in range(start_index, len(latencies)):
        pct_above = (latencies[i] - baseline_avg) / baseline_avg
        if pct_above >= THRESHOLD_PCT:
            consecutive += 1
        else:
            consecutive = 0

        if consecutive >= sustain_points:
            return i - sustain_points + 1, sustain_points

    return None, sustain_points


def build_alert(baseline_avg, timestamps, latencies, trigger_index, sustain_points):
    trigger_time = timestamps[trigger_index]
    trigger_latency = latencies[trigger_index]
    trigger_pct = ((trigger_latency - baseline_avg) / baseline_avg) * 100

    latest_latency = latencies[-1]
    latest_pct = ((latest_latency - baseline_avg) / baseline_avg) * 100

    return f"""
ALERT: Early Warning - Latency Drift Detected

Metric: {METRIC_NAME}
Baseline (healthy avg): {baseline_avg:.2f} ms

Drift started: {trigger_time.isoformat()}
Latency at drift start: {trigger_latency:.2f} ms ({trigger_pct:.2f}% above baseline)
Sustained for: {SUSTAIN_MINUTES} minutes

Current latency: {latest_latency:.2f} ms ({latest_pct:.2f}% above baseline)

Why it matters:
- Gradual drift often precedes customer-facing slowness and incident escalation.

Suggested checks:
- Recent deploys in the last 6 to 12 hours
- Downstream dependency latency (DB, cache, APIs)
- Traffic pattern changes
- Resource saturation (CPU, memory, queues)
""".strip()


def main():
    print("=== Monitoring Demo: Early Detection of Silent Degradation ===\n")

    timestamps, latencies = read_data(DATA_FILE)

    baseline_avg = average(latencies[:len(latencies)//2])

    print(f"Baseline learned from Day 1: {baseline_avg:.2f} ms")
    print(f"Detection rule: >= {int(THRESHOLD_PCT*100)}% above baseline for {SUSTAIN_MINUTES} minutes\n")

    trigger_index, sustain_points = find_sustained_drift(
        timestamps, latencies, baseline_avg
    )

    if trigger_index is None:
        print("No sustained drift detected.")
        return

    alert = build_alert(
        baseline_avg, timestamps, latencies, trigger_index, sustain_points
    )

    print(alert)
    # Send email notification (optional)
    try:
        subject = "Early Warning: Latency Drift Detected"
        send_email(subject=subject, body=alert)
        print("\n✅ Email notification sent.")
    except Exception as e:
        print(f"\n⚠️ Email not sent: {e}")


if __name__ == "__main__":
    main()
