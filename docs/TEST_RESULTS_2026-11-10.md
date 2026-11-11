# FredDesk V2.1 — Regression Test Evidence

## Test run: 2026-11-10

**Result: 5 passed, 0 failures, 0 errors (approximately 0.031 seconds).**

**Execution environment:** Local Linux Python environment. The executed fixture was reconstructed from the GitHub V2.1 versions of `database.py` and `ticket.py`; it was **not** a fresh clone or a test invocation against the actual checked-out V2.1 branch. The test file was subsequently committed to that branch in commit `ee80a386446a8234f5813b07b9acec423386228d`. Consequently, this is a preliminary local logic result, **not** a verified GitHub branch test or Windows end-to-end test.

Command run on local reconstructed fixture:
```sh
python -m unittest discover -s tests -v
```

Observed output:
```text
test_blank_resolution_rejected ... ok
test_duplicate_suppression_lookup_for_open_ticket ... ok
test_duplicate_ticket_id_rejected ... ok
test_resolution_persists_and_cannot_repeat ... ok
test_ticket_persists_across_new_connections ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.031s

OK
```

## Scope

| Case | Result | Limit |
| --- | --- | --- |
| Ticket persistence across new SQLite connections | Passed locally | Does not restart Flask process |
| Open-ticket title lookup / suppression condition | Passed locally | Does not test simultaneous requests or Flask route |
| Resolution state and notes persist | Passed locally | Does not test HTML form |
| Blank resolution rejected | Passed locally | Database function only |
| Duplicate ticket ID rejected | Passed locally | SQLite UNIQUE constraint |

Tests use isolated temporary databases, never `freddesk.db`.

## Required independent verification

From the V2.1 branch checkout:
```sh
python -m unittest discover -s tests -v
```
Record OS, Python version, commit SHA, exact output, and failures. Then run Windows Flask dashboard integration tests separately. Do not mark the application production-ready based on this report.

**Known limitation:** Title-based suppression checks for existing open tickets and is not atomic. Concurrent requests may still create separate IDs for the same incident. This is a documented risk, not a passing concurrency test.
