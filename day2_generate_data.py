import csv
from datetime import datetime, timedelta
import random

def generate_latency_value(base_ms: float, noise_ms: float) -> float:
    """Return a latency value with random noise, never below 1ms."""
    val = base_ms + random.uniform(-noise_ms, noise_ms)
    return max(1.0, val)

def main():
    # --- Locked demo parameters ---
    start_time = datetime(2026, 1, 1, 0, 0, 0)  # arbitrary, just for the demo
    interval_minutes = 5
    total_hours = 48
    total_points = int((total_hours * 60) / interval_minutes)

    # Baseline behavior (Day 1)
    baseline_latency_ms = 180.0   # "normal" p95 latency
    noise_ms = 10.0              # small jitter

    # Drift behavior (Day 2)
    drift_start_hour = 24        # start drifting after 24 hours
    drift_total_increase_pct = 0.30  # 30% increase by the end of Day 2

    output_file = "latency_metrics.csv"

    rows = []
    for i in range(total_points):
        ts = start_time + timedelta(minutes=i * interval_minutes)

        hour = i * interval_minutes / 60.0  # hour since start

        # Base latency starts at baseline
        base = baseline_latency_ms

        # Add a simple daily pattern (slightly higher during midday)
        # This makes the data look more real.
        # day_fraction ranges 0..1 each day
        day_fraction = (hour % 24) / 24.0
        midday_bump = 8.0 * (1 - abs(day_fraction - 0.5) * 2)  # peak near midday
        base += midday_bump

        # Apply gradual drift on Day 2 (after hour 24)
        if hour >= drift_start_hour:
            drift_progress = (hour - drift_start_hour) / 24.0  # 0..1 over Day 2
            drift_multiplier = 1.0 + (drift_total_increase_pct * drift_progress)
            base *= drift_multiplier

        latency = generate_latency_value(base_ms=base, noise_ms=noise_ms)

        rows.append({
            "timestamp": ts.isoformat(),
            "p95_latency_ms": round(latency, 2)
        })

    # Write CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "p95_latency_ms"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Wrote {len(rows)} rows to {output_file}")
    print("Sample rows:")
    for r in rows[:3]:
        print(r)
    print("...")
    for r in rows[-3:]:
        print(r)

if __name__ == "__main__":
    main()
