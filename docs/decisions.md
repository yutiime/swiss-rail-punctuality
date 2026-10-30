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



## Daily collection on GitHub Actions
- Choice: a scheduled GitHub Actions workflow runs `daily.py` every day at 05:37 UTC.
- Reason: the source keeps only about 50 days, so collection must not depend on my laptop being on. A single short daily job does not justify an orchestrator such as Airflow; GitHub Actions is free for public repositories and already runs the CI.
- Timing: files are published around 03:12 UTC. 05:37 leaves a margin and avoids the top of the hour, when scheduled runs queue up.
- Limitation: start times are not guaranteed, and scheduled workflows are disabled after 60 days without activity on the repository.



## 7-day catch-up window
- Choice: each run looks at the last 7 days and processes only the ones missing from storage.
- Reason: a failed or skipped run is repaired by the following ones without manual action. Checking a day that is already stored costs a single request.
- Limitation: a day that keeps failing is retried, and reported, every morning for a week.



## Azure Blob Storage as the reference
- Choice: daily Parquet files go to an ADLS Gen2 container in Switzerland North, with LRS redundancy and 7-day soft delete.
- Reason: the GitHub machine is wiped after each run, so the files must live elsewhere, and the "already done?" check looks at storage instead of the local disk. ADLS Gen2 is the storage Databricks will read from later.
- Uploads never overwrite an existing file.
- Limitation: LRS keeps three copies in one datacentre. For days older than the source's retention, storage and my laptop hold the only copies.



## SAS token with least privilege
- Choice: the job authenticates with a SAS token limited to the `processed` container: read, create, write and list, no delete, HTTPS only, 3-month expiry.
- Reason: if it leaks, it cannot delete data and stops working on its own.
- Next step: OIDC federation would remove the stored secret entirely.
- Expiry: 26-01-2027. Renew the token and update the GitHub secret before then.



## Row-count check before publishing
- Choice: each day is written to a `.part` file, its row count is checked against a floor for its day type, and only then is it renamed (write-audit-publish).
- Floors: 2,000,000 rows on weekdays, 1,700,000 on Saturdays, 1,300,000 on Sundays, about 80% of the lowest day observed in September–October 2026.
- Reason: a bad day never gets its final name, so it can never be mistaken for a finished day.
- Limitation: only large losses are caught (a 3% truncation would pass), and weekday public holidays will trigger false alarms.