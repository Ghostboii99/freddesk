# FredDesk — IT Diagnostics and Incident Management

FredDesk is a personal IT-support engineering project with two separate development lines. **The default `main` branch is an incomplete diagnostic CLI snapshot; it is not the Flask/SQLite V2.1 application.** The CLI README previously described files and tests not present on `main`. Do not use `python -m freddesk` as proof of a working application from this branch.

## Where to find the work

| Branch | Purpose | Evidence status |
| --- | --- | --- |
| [`main`](../../tree/main) | Earlier Python diagnostics CLI concept | Incomplete published snapshot; startup/tests not verified |
| [`v2-ticketing-checkpoint`](../../tree/v2-ticketing-checkpoint) | Earlier Flask/SQLite ticketing checkpoint | Source present; current automated verification pending |
| [`v2.1-incident-resolution`](../../tree/v2.1-incident-resolution) | Flask dashboard, SQLite incident records, duplicate suppression and resolution | Source present; current automated verification pending |

**Start with [FredDesk V2.1](../../tree/v2.1-incident-resolution) for the incident-ticketing project referenced on the resume.**

## V2.1 architecture (source-inspected)

- `app.py`: Flask dashboard, automated high-memory incident creation and POST resolution endpoint.
- `database.py`: SQLite schema, ticket inserts, queries, open-ticket lookup and status/resolution updates.
- `ticket.py`: ticket IDs and structured ticket records.
- `scanner.py` and `log_analyzer.py`: system diagnostics and log analysis.
- `templates/Dashboard.html`: web interface.

The code checks for an **open** ticket with the title `High Memory Usage` before creating another. This is title/status-based suppression, **not universal deduplication**; a resolved ticket can be followed by a new incident if the condition remains. The SQLite update uses a ticket ID and open/in-progress status predicate. These are implementation observations, not proof of successful end-to-end execution.

## Validation and limitations

Prior development sessions recorded tests of ticket persistence, duplicate prevention and resolution after reopening. Their raw logs are **not yet published here**, so those results are historical records rather than independently reproduced CI results.

Current blockers:
1. Reproduce the V2.1 installation and run on a supported Windows lab machine.
2. Add and execute automated tests for SQLite persistence, duplicate suppression and resolution.
3. Capture redacted command output, environment/version and commit SHA in a dated test report.
4. Review local-development settings (including Flask debug mode and secret key) before any network exposure. **Do not deploy this version to the public internet.**

This is a learning and demonstration project, not a production security monitoring system.

## Resume evidence standard

Describe only the code and tests that can be supported by the linked branch and test artifacts. Separate **implemented**, **historically tested**, and **currently reproduced** claims. See the V2.1 branch for the source; do not interpret this `main` snapshot as V2.1.

## Responsible use

Run diagnostics only on systems you own or have permission to assess. Remove private data from logs and screenshots before publishing.
