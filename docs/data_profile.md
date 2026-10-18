# Ist-Daten data profile

## Source
- Website: opentransportdata.swiss, "Ist-Daten v2" dataset
- One CSV file per day, approximately 413 MB
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


