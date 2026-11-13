# FredDesk operational policies — v0.1

Prepared: November 12, 2026  
Proposed owner: Frederick Fleming  
Status: Proposed baseline for review; application enforcement is incomplete.  
Scope: FredDesk V2.1 incident records, diagnostic evidence, resolution and exports.

## Objective and boundaries

Make every incident traceable from observation to verified outcome while collecting only necessary information. FredDesk remains a local lab project until access controls, data handling and release checks are implemented and validated. These policies do not establish a customer SLA or claim regulatory compliance.

Use only owned systems or systems with explicit authorization. Record the authorized scope before diagnostics. Separate lab/personal work from paid client work; never count lab results as client accomplishments. Unknown facts remain "Unknown" or "Not tested"; assumptions must be labeled. Do not fabricate results, time spent or customer confirmation.

Policy changes require owner review, a version/date and a record of affected controls. Review monthly and after a material incident or workflow change. Exceptions require an owner, reason, limited scope, expiry and compensating action; an exception cannot turn an untested outcome into a verified result.

## FD-01 — Incident handling

### Required record

Each incident must have:
- Unique ticket ID, creation time with timezone, source and affected system alias.
- Issue description and observed impact; separate observations from suspected causes.
- Severity with rationale, work type (lab/personal/paid client), assigned owner and next action.
- Evidence or an explicit missing-evidence note, including capture time.
- Current status, troubleshooting steps and their actual results.
- Authorization reference for any third-party system; do not put credentials in that reference.

Intake may preserve unknown fields, but the owner must identify what is missing before remediation. Automated observations create candidate incidents; they do not establish a root cause or prove compromise.

### Severity and escalation

| Severity | Trigger | Required action |
| --- | --- | --- |
| Critical | Suspected active compromise, data loss or widespread service interruption | Stop routine changes, preserve minimal evidence and contact the authorized system owner through an agreed channel. |
| High | Major service loss with no practical workaround | Prioritize investigation and escalate when scope or expertise is exceeded. |
| Medium | Degraded service or recurring fault with limited impact | Investigate, document impact and assign a next action. |
| Low | Minor issue or informational observation | Queue with an owner and review date. |

These are prioritization rules, not response-time promises. Resource thresholds alone do not establish Critical severity. Do not conduct containment, destructive repairs or changes outside authorization.

### Lifecycle

Open → In Progress → Needs Verification → Resolved → Closed.

- Open: observation recorded; triage pending.
- In Progress: an owner is investigating or performing an authorized fix.
- Needs Verification: a fix was attempted, but validation is incomplete or unknown.
- Resolved: the FD-02 technical verification requirements passed.
- Closed: technical verification passed, required customer confirmation is recorded, and unresolved follow-ups are completed or explicitly transferred to linked open tickets.
- Reopen: a failed validation or recurrence returns the ticket to In Progress with the reason and original resolution history preserved.

For lab/personal work, customer confirmation may be Not Applicable with a reason. For paid client work, technical resolution may precede customer confirmation, but closure must wait for that confirmation.

Duplicates must reference a canonical ticket and preserve relevant evidence. Do not silently discard records. Any future duplicate detection must account for affected system and active states, including Needs Verification; matching a title alone is insufficient for multiple systems.

## FD-02 — Verified resolution

A technician must record all of the following before Resolved:
1. What was changed and by whom.
2. The validation procedure and expected outcome.
3. The actual observed result, recorded as Pass, Fail or Not Tested.
4. Evidence or a restricted evidence reference, validation time with timezone and validator identity.
5. Remaining limitations or follow-up work.

Only Pass permits Resolved. Blank, Fail and Not Tested must not qualify. A status label or resolution note alone is not proof. Historical records marked Resolved without these fields must be flagged as legacy/unverified; do not backfill invented evidence or silently certify them.

Example acceptance criterion for high memory: record the workload and sampling interval, then observe memory against the stated threshold during that interval. A single healthy sample does not establish a lasting fix. Document any limits of the observation.

Controls must validate at the server and persistence boundary, not only in the browser. Status changes and their evidence must be saved atomically. Invalid requests must leave the prior record unchanged. Repeated submissions must not overwrite a verified resolution or erase history.

### Required acceptance checks — not yet run for these policies

| ID | Scenario | Expected result |
| --- | --- | --- |
| VR-01 | Submit empty or whitespace-only resolution notes | Reject; preserve prior record. |
| VR-02 | Submit notes but omit validation procedure, evidence, validator or time | Reject Resolved; retain an unverified state. |
| VR-03 | Submit Fail, Not Tested or an unknown validation value | Reject Resolved. |
| VR-04 | Submit complete passing verification | Save fields and Resolved together; values survive a fresh database connection. |
| VR-05 | Call persistence function directly without verification | Reject; UI bypass cannot satisfy the policy. |
| VR-06 | Close a paid-client ticket without customer confirmation | Reject Closed. |
| VR-07 | Reopen a ticket after recurrence | Preserve prior resolution and record reason/time. |
| VR-08 | Load legacy resolved tickets without verification | Display unverified legacy evidence status. |
| VR-09 | Submit a duplicate resolution request | Preserve original verification and history. |

## FD-03 — Data protection and retention

### Collection and access

Collect the smallest useful evidence excerpt. Never intentionally store passwords, API keys, session cookies, recovery codes, private keys or unnecessary personal information in tickets, logs, attachments or screenshots.

Use system aliases and redact usernames, addresses, client names and sensitive file paths before sharing. Treat raw client logs as restricted. Keep the database and evidence outside the public repository and restrict local filesystem access to the authorized operator. Do not expose the current lab server to the internet or a shared network.

Before multi-user or client deployment, implement and test authentication, authorization, request protection and access auditing. A local binding alone is not a substitute for these controls.

### Proposed lab retention baseline

| Data | Default retention | Disposal rule |
| --- | --- | --- |
| Raw diagnostic captures | 30 days from capture | Delete once no longer needed; retain only minimal redacted evidence. |
| Lab ticket records and redacted evidence | 90 days after closure | Review and delete or retain a sanitized portfolio summary with a recorded reason. |
| Lab backups | Rolling 30 days | Expire copies on schedule; document restoration and disposal checks. |

These are proposed lab defaults, not existing automated deletion behavior. Client retention must be explicitly agreed before client data is collected; do not apply lab defaults to client records by assumption. Record a retain-until date for exceptions and review it monthly. Pause disposal for a documented preservation requirement.

Deletion must include database records, attachments, exports and expired backups. SQLite deletion alone may leave recoverable data in free pages, journals or backups; validate the chosen cleanup procedure before claiming secure erasure. Restoring a backup must not silently reintroduce records whose retention period has expired.

### Exposure response and publication

If a secret or sensitive record is exposed: stop further sharing, restrict access, notify the authorized owner, rotate exposed credentials where authorized, and document cleanup without repeating the secret. Deleting a Git file alone does not remove its history.

Publish only synthetic or sanitized portfolio evidence. Client-derived case studies require client permission and a separate redaction review. No raw client databases, credentials or identifying screenshots belong in the public repository.

Acceptance checks: confirm database/log artifacts are excluded from commits; test redaction with synthetic secrets; verify unauthorized access is rejected before shared use; test retention on disposable fixtures and backups. Record actual results and commit IDs—these checks are not reported as passed here.

## Current source observations and implementation gaps

Inspected on November 12, 2026 on branch `v2.1-incident-resolution`. This was source review, not runtime validation.

| Area | Observed source | Gap against policy |
| --- | --- | --- |
| Resolution | `app.py` and `database.py` reject blank notes; database update accepts Open/In Progress | No recorded validation gate before Resolved. |
| Ticket schema | `database.py` stores core ticket fields and resolution text | No dedicated validation, owner, work-type, customer-confirmation or transition-history fields. |
| Duplicate suppression | `app.py` searches active tickets by title | No host scoping or Needs Verification state handling. |
| Local operation | `app.py` binds to 127.0.0.1 when run directly, enables debug and contains a development secret | Deployment hardening and access controls remain prerequisites for shared use. |
| Evidence | Ticket evidence is stored as text | No demonstrated redaction or retention enforcement in inspected files. |

Evidence checkpoints: `app.py` blob `3aaf50855fc2ca9ee08854feeb1a0f4367e8086b`; `database.py` blob `c7d61fe534fa86c4c52dce060d6e9bc3d47ce5e4`; `ticket.py` blob `30759cbdf2e61dcbf3cabf3e30732ea6fd2abebd`.

## Next three implementation actions

1. Add a backward-compatible schema migration for verification fields and legacy evidence status; test on a copy of the database.
2. Enforce verified resolution in both the route and database function, add Needs Verification to active-ticket logic, and run VR-01 through VR-05 plus VR-08/09.
3. Add work type, customer confirmation and durable transition history; then test closure/reopening and establish redaction and retention checks before client use.

For every control track: policy ID, implementation commit, test command, actual result, evidence location and remaining limitation. Mark it Verified only after a reproducible passing check.
