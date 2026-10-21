# Ist-Daten data profile

## Source
- Website: opentransportdata.swiss, "Ist-Daten v2" dataset
- One CSV file per day, approximately 413 MB on a Sunday, ~600 MB on a weekday 
- 1,709,145 rows for September 20, 2026
- One row represents a vehicle passing a stop

## Actual-time status
- REAL: 88.4% -> actually measured time
- PROGNOSE, GESCHAETZT, UNBEKANNT: predicted or estimated, not measured
- Decision: delays are calculated only for REAL records

## Observations
- The website preview export is truncated at 1,664,000 rows (2.6% data loss); always use the direct URL
- Scheduled times have no seconds, while actual times do
- The first stop has no arrival time, except for TPG and TL
- Some trips contain duplicate stops

- Volume varies substantially by day of the week: Sunday 20/09 = 1.7 million rows, Monday 21/09 = 2.5 million. Volume checks should compare against the same weekday in the previous week.
- The website blocks Python's default User-Agent (403 error). The script identifies itself with its own name.

## Source retention (observed 2026-10-21)

The dataset page lists 50 daily files, from 2026-09-01 to 2026-10-20.
Two rules fit this single observation:

- a sliding window of about 50 days
- the current month plus the previous one (the list starts exactly on the 1st)

To check on 1–2 November: if the list then starts on 2026-10-01, the rule
is monthly and a whole month disappears at once.

## Daily row counts (2026-09-01 to 2026-10-20)

| Day type  | Rows per day   |
|-----------|----------------|
| Mon–Fri   | 2.58M – 2.71M  |
| Saturday  | 2.16M – 2.19M  |
| Sunday    | 1.69M – 1.72M  |

Below their peers:

- 2026-09-21 (Mon): 2.52M. Likely the Lundi du Jeûne fédéral, a public
  holiday in the canton of Vaud.
- 2026-09-10 (Thu): 2.53M. No explanation found.

2026-09-20 has 1,709,145 rows, matching the official file checked during
the first exploration (the truncated export had stopped at 1,664,000).

Consequence for quality checks: a day must be compared with days of the
same type. Against the overall average, every Sunday would look ~30% short.