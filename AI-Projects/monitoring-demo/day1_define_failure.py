# Day 1 - Define the Failure (Monitoring Demo)
# Beginner-friendly: this script just prints the demo scenario.

def main():
    problem_name = "Silent latency degradation"
    what_happened = (
        "Latency slowly increased over several hours while the service stayed 'up'."
    )
    why_monitoring_failed = (
        "Alerts were based on fixed thresholds, so nothing triggered until it was already bad."
    )
    impact = (
        "Users experienced slowness and support tickets appeared before engineers noticed."
    )
    what_we_want_instead = (
        "Detect drift early and alert with context before users complain."
    )

    print("=== Monitoring Demo: Day 1 ===")
    print(f"Problem: {problem_name}")
    print(f"What happened: {what_happened}")
    print(f"Why monitoring failed: {why_monitoring_failed}")
    print(f"Impact: {impact}")
    print(f"What we want instead: {what_we_want_instead}")

if __name__ == "__main__":
    main()
