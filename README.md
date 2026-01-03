\# Monitoring Demo: Silent Latency Degradation



\## Problem (Plain English)

\- Problem name: Silent latency degradation

\- What happened: Latency slowly increased over several hours while the service stayed “up”.

\- Why monitoring failed: Alerts were based on fixed thresholds, so nothing triggered until it was already bad.

\- Impact: Users experienced slowness and support tickets appeared before engineers noticed.

\- What we want instead: Detect drift early and alert with context before users complain.



\## Demo Inputs (Locked)

\- Metric: p95\_latency\_ms

\- Resolution: every 5 minutes

\- Time span: 48 hours (Day 1 normal, Day 2 drifting worse)



\## Demo Success Criteria

\- Detect gradual latency drift BEFORE a fixed threshold would fire.

\- Trigger ONE early warning alert (not noisy).

\- Alert includes:

&nbsp; - baseline latency

&nbsp; - current latency

&nbsp; - percent increase

&nbsp; - duration of drift



\## Example Alert Output (Target)

Early Warning: Latency Drift Detected

\- Metric: p95\_latency\_ms

\- Drift: +25% above baseline

\- Duration: 3 hours

\- Why it matters: Drift often precedes user complaints

\- Suggested checks: recent deploys, downstream dependency latency, traffic changes











\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*8

Problem name: Silent latency degradation



What happened: \[Describe in 1 sentence]



Why monitoring failed: \[Describe in 1 sentence]



Impact: \[Describe in 1 sentence]



What we want instead: \[Describe in 1 sentence]



\*\*\*\*\*\* EXAMPLE  \*\*\*\*\*\*\*\*



Problem name: Silent latency degradation



What happened: Latency slowly increased over several hours while the service stayed “up.”



Why monitoring failed: Alerts were based on hard thresholds, so nothing triggered until it was already bad.



Impact: Users experienced slowness and support tickets appeared before engineers noticed.



What we want instead: A system that detects drift early and alerts with context before users complain.



Metric: p95\_latency\_ms



Resolution: every 5 minutes



Time span: 48 hours (Day 1 normal, Day 2 drifting worse)



------------------  Demo Success Criteria     --------------------



The system detects a gradual latency increase before a fixed threshold alarm would.



It triggers one clear early-warning alert (not spam).



The alert includes:



baseline latency



current latency



percent increase



how long it’s been drifting



--------------------------------------------------------------



Example Alert Output (what we want)



Early Warning: Latency Drift Detected



Metric: p95\_latency\_ms



Drift: +25% above baseline



Duration: 3 hours



Why it matters: Drift often precedes user complaints



Suggested checks: recent deploys, downstream dependency latency, traffic changes



--------------------------------------------------------------

--Day 1 Checklist

README.md has the filled template
python day1_define_failure.py prints your scenario

--Day 2 Checklist
Generate a believable 48-hour latency dataset:
Day 1: normal
Day 2: gradual latency drift (silent degradation)
--Day 3 Checklist

Script loads CSV without errors
Baseline average prints
Current latency prints
Percent change is > 20%

--Day 4 Checklist
python day4_detect_drift.py prints:
baseline avg
detection threshold + duration
first trigger time
trigger window showing sustained drift
latest % above baseline

--Day 5 — Generate an Actionable Alert (60–90 min)
Goal (what “done” looks like)
By end of Day 5 you will have:
A script that detects drift (from Day 4)
AND prints a clean alert message with:
what happened
when it started
severity (% above baseline)
how long it has persisted
what to check first (suggested actions)
-------------
4️⃣ Why this alert is $25k-worthy (important)
Read this sentence carefully:
“Drift started at 20:00, sustained for 60 minutes, 29% above baseline, before users complained.”
That sentence:
explains when
explains why
explains impact
explains urgency
explains what to do next
Most alerts only say:  “Latency high.”
Yours says:
“Latency is behaving abnormally and here’s why you should care.”
-----------------
5️⃣ You have now completed the CORE demo
At this point, you have:
| Day                               | Status |
| --------------------------------- | ------ |
| Day 1 – Failure definition        | ✅      |
| Day 2 – Realistic data            | ✅      |
| Day 3 – Baseline logic            | ✅      |
| Day 4 – Sustained drift detection | ✅      |
| Day 5 – Actionable alert          | ✅      |
------------------


