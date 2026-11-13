from flask import Flask, render_template
from scanner import get_system_health, get_top_processes, calculate_health_score
from log_analyzer import analyze_logs
from ticket import create_ticket
from database import initialize_database, save_ticket, get_open_ticket_by_title

app = Flask(__name__)
initialize_database()


@app.route("/")
def dashboard():
    health = get_system_health()
    logs = analyze_logs()
    health_score = calculate_health_score(health, logs)
    top_processes = get_top_processes()

    process_alerts = []

    for proc in top_processes:
        if proc["memory_mb"] > 500:
            process_alerts.append(
                f"{proc['name']} is using {proc['memory_mb']} MB of memory."
            )

        if proc["cpu_percent"] > 50:
            process_alerts.append(
                f"{proc['name']} is using high CPU at {proc['cpu_percent']}%."
            )

    if not process_alerts:
        process_alerts.append("No major process issues detected.")

    tickets = []

    if health["memory_percent"] > 80:
        existing_ticket = get_open_ticket_by_title("High Memory Usage")

        if existing_ticket:
            tickets.append({
                "ticket_id": existing_ticket[1],
                "title": existing_ticket[2],
                "description": existing_ticket[3],
                "category": existing_ticket[4],
                "priority": existing_ticket[5],
                "status": existing_ticket[6],
                "source": existing_ticket[7],
                "evidence": existing_ticket[8].split("\n"),
                "created_at": existing_ticket[9],
                "resolution": existing_ticket[10]
            })
        else:
            new_ticket = create_ticket(
                title="High Memory Usage",
                description="System memory utilization exceeded the FredDesk threshold.",
                category="Performance",
                priority="Medium",
                source="Automated Diagnostic",
                evidence=[
                    f"Memory utilization: {health['memory_percent']}%"
                ]
            )

            save_ticket(new_ticket)
            tickets.append(new_ticket)

    issues = []

    if health["disk_percent"] > 85:
        issues.append("Disk space is high. Free up storage soon.")

    if health["memory_percent"] > 80:
        issues.append("Memory usage is high. Check running apps.")

    if health["cpu_percent"] > 85:
        issues.append("CPU usage is high. Check top processes.")

    if not issues:
        issues.append("System looks healthy.")

    return render_template(
        "dashboard.html",
        health=health,
        logs=logs,
        issues=issues,
        health_score=health_score,
        top_processes=top_processes,
        process_alerts=process_alerts,
        tickets=tickets
    )


if __name__ == "__main__":
    app.run(debug=True)
