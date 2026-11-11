# FredDesk V2.1 — Flask/SQLite Incident Management

**Status:** Development lab. Historical manual validation was recorded in earlier development sessions; automated regression tests and a fresh reproducible run are pending.

## Overview
FredDesk V2.1 combines workstation diagnostics, Windows event analysis and a Flask dashboard with SQLite-backed incident tickets.

## Architecture
- `app.py` — Flask dashboard and ticket-resolution POST route
- `scanner.py` — host health and process diagnostics
- `log_analyzer.py` — event analysis
- `ticket.py` — incident record creation
- `database.py` — SQLite schema, inserts, lookup and resolution updates
- `templates/Dashboard.html` — technician dashboard

## Implemented in source
1. Automatically create a High Memory Usage ticket when the memory threshold exceeds 80%.
2. Suppress additional **open** High Memory Usage tickets by checking title and status.
3. Store tickets and evidence in a local SQLite database.
4. Resolve an open/in-progress ticket using a POST form with nonempty resolution notes.
5. Display open and resolved ticket counts.

**Scope:** The suppression rule is title-based and only applies while an incident is open. It is not general event deduplication. No production deployment or SIEM integration is claimed.

## Run locally (Windows development lab)
```powershell
git clone --branch v2.1-incident-resolution https://github.com/Ghostboii99/freddesk.git
cd freddesk
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`. The project uses Windows-oriented dependencies; other operating systems have not been verified. **Do not expose the Flask development server to a network.** Current code enables debug mode and uses a development-only secret key.

## Verification plan (not yet rerun)
| Test | Procedure | Expected result | Current evidence |
| --- | --- | --- | --- |
| T01 Startup | Install dependencies and launch on Windows | Dashboard renders | Pending fresh run |
| T02 Ticket persistence | Create ticket, restart app, query SQLite | Same ticket ID and fields | Historical manual record; raw log pending |
| T03 Open-ticket suppression | Trigger the same high-memory finding and refresh | Only one open ticket | Historical manual record; raw log pending |
| T04 Resolution persistence | Resolve ticket, restart app and query SQLite | Status remains Resolved with notes | Historical manual record; raw log pending |
| T05 Validation | Submit empty resolution | Ticket remains open | Pending fresh run |
| T06 Regression | Repeat all tests on clean checkout | Reproducible results | Pending |

Record commit SHA, Python version, OS, commands, actual results and redacted logs before marking a test Passed.

## Known risks
- Hardcoded Flask development secret and `debug=True` are unsuitable for deployment.
- SQLite writes are not yet covered by committed automated regression tests.
- Title-only open-ticket suppression may not match all intended incident identities.
- Dependency versions are not pinned.
- No authentication or authorization is implemented for incident actions.

## Resume-ready description (carefully scoped)
*Developed a Python/Flask IT diagnostics and incident-management lab using SQLite for structured tickets, status tracking and resolution notes; implemented open-ticket suppression and documented persistence and regression-test scenarios.*

This describes implemented code without claiming unverified production reliability.

## Responsible use
Use on owned or authorized systems only. Redact hostnames, usernames and event details before sharing logs.
