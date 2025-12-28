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

