import win32evtlog
from datetime import datetime, timedelta


def count_events(log_type, event_ids, hours=24):
    server = "localhost"
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    count = 0
    cutoff = datetime.now() - timedelta(hours=hours)

    try:
        handle = win32evtlog.OpenEventLog(server, log_type)

        while True:
            events = win32evtlog.ReadEventLog(handle, flags, 0)
            if not events:
                break

            for event in events:
                event_time = event.TimeGenerated
                if event_time < cutoff:
                    return count
                if event.EventID in event_ids:
                    count += 1

        return count
    except Exception as error:
        print(f"Could not read {log_type} log: {error}")
        return 0


def analyze_logs():
    failed_logins = count_events("Security", [4625])
    account_lockouts = count_events("Security", [4740])
    unexpected_shutdowns = count_events("System", [6008])
    service_crashes = count_events("System", [7031, 7034])
    application_errors = count_events("Application", [1000])
    critical_errors = unexpected_shutdowns + service_crashes + application_errors
    warnings = count_events("System", [51, 55, 129, 153])

    recommendations = []

    if failed_logins > 5:
        recommendations.append("Multiple failed logins detected. Review possible password issues or brute-force attempts.")
    if account_lockouts > 0:
        recommendations.append("Account lockouts detected. Check user credentials, saved passwords, or mapped drives.")
    if unexpected_shutdowns > 0:
        recommendations.append("Unexpected shutdown detected. Check power loss, overheating, or system crashes.")
    if service_crashes > 0:
        recommendations.append("Windows service crashes detected. Review failed services in Event Viewer.")
    if application_errors > 0:
        recommendations.append("Application crashes detected. Check recently installed or unstable programs.")
    if warnings > 5:
        recommendations.append("System warnings are elevated. Review disk, driver, and hardware-related events.")
    if not recommendations:
        recommendations.append("No major Windows Event Log issues found in the last 24 hours.")

    return {
        "failed_logins": failed_logins,
        "account_lockouts": account_lockouts,
        "unexpected_shutdowns": unexpected_shutdowns,
        "service_crashes": service_crashes,
        "application_errors": application_errors,
        "critical_errors": critical_errors,
        "warnings": warnings,
        "recommendations": recommendations
    }
