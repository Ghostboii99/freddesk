# FD-CASE-001 — CPU monitoring interpretation

**Status:** Resolved for diagnostic explanation. Software remediation and runtime validation remain open.

**Context:** Personal lab troubleshooting and portfolio documentation; not paid client work.

## Reported issue

A monitoring dashboard displayed a process CPU percentage above 100%, raising concern about system load.

## Investigation

- Compared dashboard observations with Windows Task Manager.
- Checked how processor topology affects CPU percentage interpretation.
- Consulted monitoring-library documentation and reviewed relevant published source.
- Distinguished observations taken at different times from a synchronized comparison.

## Finding and resolution

Process CPU percentages may use a per-logical-processor scale rather than a whole-system scale. A reading above 100% can therefore be valid without indicating that the entire CPU is overloaded. Source review identified a reporting-scale concern.

The diagnostic explanation was provided. The precise running software revision was not verified, and the observations were not simultaneous. No deployed correction or measured performance improvement is claimed.

## Follow-up

[Validate CPU reporting and alert behavior — issue #3](https://github.com/Ghostboii99/freddesk/issues/3).

No software changes or runtime tests were performed for this case. This document does not change records in the local application.

## Publication scope

This public summary omits device identifiers, hardware specifications, raw telemetry, screenshots, personal details, and detailed implementation notes. Time spent was not recorded.

## Skills demonstrated

Windows troubleshooting, measurement interpretation, documentation review, source inspection, and evidence-based incident documentation.
