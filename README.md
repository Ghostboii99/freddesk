# FredDesk

**Support diagnostics with a defender's mindset.**

FredDesk is a dependency-free Python toolkit that turns a workstation snapshot into an explainable health score, a help-desk checklist, and a clean HTML/JSON report. On Windows, it also reviews selected event IDs and gives analysts cautious, actionable follow-up guidance.

> Built for a real support workflow: collect the facts, explain the signal, and show the next review step.

## Why it stands out

- Runs with the Python standard library—useful on locked-down or freshly imaged machines
- Checks CPU, memory, disk, and memory-heavy processes
- Applies visible thresholds instead of a black-box score
- Reviews Windows Event IDs `1102`, `4625`, `4688`, `7045`, `1000`, `1001`, and `1314`
- Treats event matches as **review signals**, not automatic proof of malicious activity
- Produces a responsive, self-contained HTML report plus machine-readable JSON
- Includes deterministic demo data and automated tests

## Quick start

```bash
git clone https://github.com/Ghostboii99/freddesk.git
cd freddesk
python -m freddesk
```

Reports are saved to `reports/freddesk-report.html` and `reports/freddesk-report.json`.

Create a privacy-safe demo report on any operating system:

```bash
python -m freddesk --demo --output docs
```

[Open the sample HTML report](docs/freddesk-report.html)

## Commands

```text
python -m freddesk [--output DIR] [--format html|json|both]
                   [--top 8] [--hours 24] [--no-events] [--demo]
```

Examples:

```bash
# Only JSON, with the 12 largest processes
python -m freddesk --format json --top 12

# Skip Event Log collection
python -m freddesk --no-events

# Review up to seven days of selected Windows events
python -m freddesk --hours 168
```

## Health scoring

| Signal | Review threshold | Score impact |
|---|---:|---:|
| CPU | 50% / 90% | -10 / -25 |
| Memory | 80% / 90% | -15 / -25 |
| Disk | 85% / 95% | -20 / -30 |
| Process | Over 50% CPU or 500 MB memory | -3 each, capped at -12 |
| High-priority event | Event ID 1102 or 7045 | -4 each, capped at -16 |

Scores map to `Healthy` (85–100), `Review` (65–84), or `Attention` (0–64). The report lists every deduction so a technician can audit the result.

## Windows event triage

FredDesk uses `Get-WinEvent` and records only event ID, provider, and timestamp. It does not collect message bodies, usernames, command lines, or credentials. Some Security log access may require an elevated PowerShell session.

Event IDs can mean different things across providers and logs—especially `1314`. FredDesk keeps the provider visible and asks the analyst to validate context before reaching a conclusion.

## Tests

```bash
python -m unittest discover -s tests -v
```

The suite checks threshold boundaries, event classification, safe HTML escaping, and valid JSON output.

## Project structure

```text
freddesk/
├── freddesk/
│   ├── cli.py          # command-line workflow
│   ├── diagnostics.py  # cross-platform system collection
│   ├── events.py       # Windows event collection and classification
│   ├── reports.py      # HTML and JSON output
│   └── scoring.py      # explainable health score
├── tests/
├── docs/               # privacy-safe sample output
└── pyproject.toml
```

## Responsible use

FredDesk is a diagnostic and triage aid. It does not replace endpoint protection, incident-response procedures, or analyst judgment. Run it only on systems you own or are authorized to assess.

---

Built by Fred · **Build it. Test it. Understand it. Improve it.**
