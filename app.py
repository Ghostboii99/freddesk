from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from scanner import (
    get_system_health,
    get_top_processes,
    calculate_health_score
)

from log_analyzer import analyze_logs
from ticket import create_ticket

from database import (
    initialize_database,
    save_ticket,
    get_open_ticket_by_title,
    get_all_tickets,
    resolve_ticket
)


app = Flask(__name__)
app.secret_key = "freddesk-local-development-only"

initialize_database()


@app.route("/")
def dashboard():

    # SYSTEM DIAGNOSTICS
    health = get_system_health()
    logs = analyze_logs()

    health_score = calculate_health_score(health, logs)
    top_processes = get_top_processes()

    # PROCESS ANALYSIS
    process_alerts = []

    for proc in top_processes:

        if proc["memory_mb"] > 500:
            process_alerts.append(
                f"{proc['name']} is using "
                f"{proc['memory_mb']} MB of memory."
            )

        if proc["cpu_percent"] > 50:
            process_alerts.append(
                f"{proc['name']} is using high CPU "
                f"at {proc['cpu_percent']}%."
            )

    if not process_alerts:
        process_alerts.append(
            "No major process issues detected."
        )

    # AUTOMATED INCIDENT DETECTION
    if health["memory_percent"] > 80:

        existing_ticket = get_open_ticket_by_title(
            "High Memory Usage"
        )

        if not existing_ticket:

            new_ticket = create_ticket(
                title="High Memory Usage",
                description=(
                    "System memory utilization exceeded "
                    "the FredDesk threshold."
                ),
                category="Performance",
                priority="Medium",
                source="Automated Diagnostic",
                evidence=[
                    f"Memory utilization: "
                    f"{health['memory_percent']}%"
                ]
            )

            save_ticket(new_ticket)

    # TECHNICIAN RECOMMENDATIONS
    issues = []

    if health["disk_percent"] > 85:
        issues.append(
            "Disk space is high. Free up storage soon."
        )

    if health["memory_percent"] > 80:
        issues.append(
            "Memory usage is high. Check running apps."
        )

    if health["cpu_percent"] > 85:
        issues.append(
            "CPU usage is high. Check top processes."
        )

    if not issues:
        issues.append("System looks healthy.")

    # PERSISTENT INCIDENT HISTORY
    tickets = get_all_tickets()

    open_count = sum(
        1 for ticket in tickets
        if ticket["status"] in ("Open", "In Progress")
    )

    resolved_count = sum(
        1 for ticket in tickets
        if ticket["status"] == "Resolved"
    )

    return render_template(
        "Dashboard.html",
        health=health,
        logs=logs,
        issues=issues,
        health_score=health_score,
        top_processes=top_processes,
        process_alerts=process_alerts,
        tickets=tickets,
        open_count=open_count,
        resolved_count=resolved_count
    )


@app.route("/tickets/<ticket_id>/resolve", methods=["POST"])
def resolve_incident(ticket_id):

    resolution = request.form.get(
        "resolution", ""
    ).strip()

    if not resolution:
        flash(
            "Resolution notes are required.",
            "error"
        )

        return redirect(url_for("dashboard"))

    updated = resolve_ticket(
        ticket_id,
        resolution
    )

    if updated:
        flash(
            f"Ticket {ticket_id} marked as resolved.",
            "success"
        )
    else:
        flash(
            "Ticket could not be resolved. "
            "It may already be resolved or closed.",
            "error"
        )

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )