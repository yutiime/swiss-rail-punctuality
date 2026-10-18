# Decisions

## Downloading through the dataset page
- Choice: the script reads the dataset's HTML page to find the file link for each day.
- Reason: the official API (CKAN) rejects requests without an access key (403).
- Limitation: the page lists only recent days. Historical data will require the monthly archive. If the page structure changes, switch to an API key.



## Comparison with the official SBB figure

My result: 93.56% (September 2026, 3-minute threshold, all rail operators)
SBB's 2025 figure: 94.1% (passenger services, 3-minute threshold) — source: <https://reporting.sbb.ch/fr/ponctualite?=&years=1,4,5,6,7&scroll=0&highlighted=>

The 0.5 percentage-point difference can be explained by four methodological differences:

| Difference | Likely effect |
| --- | --- |
| Scope: all operators in my dataset, SBB only in theirs | pulls my figure down |
| Period: one month versus a full year | could shift the result either way |
| SBB also publishes punctuality weighted by passenger numbers | different methodology from mine |
| Measurement points: all stops in my dataset, scope unknown in theirs | uncertain effect |