from datetime import datetime
import uuid


def create_ticket(
    title,
    description,
    category,
    priority="Medium",
    source="Manual",
    evidence=None
):
    """Create a standardized FredDesk support ticket."""

    ticket_id = f"FD-{uuid.uuid4().hex[:6].upper()}"

    return {
        "ticket_id": ticket_id,
        "title": title,
        "description": description,
        "category": category,
        "priority": priority,
        "status": "Open",
        "source": source,
        "evidence": evidence or [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "resolution": None
    }
