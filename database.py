import sqlite3
from pathlib import Path

DB_NAME = Path(__file__).resolve().parent / "freddesk.db"


def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                priority TEXT,
                status TEXT,
                source TEXT,
                evidence TEXT,
                created_at TEXT,
                resolution TEXT
            )
        """)


def row_to_ticket(row):
    if row is None:
        return None

    ticket = dict(row)
    ticket["evidence"] = (
        ticket["evidence"].splitlines()
        if ticket["evidence"] else []
    )

    return ticket


def save_ticket(ticket):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO tickets (
                ticket_id,
                title,
                description,
                category,
                priority,
                status,
                source,
                evidence,
                created_at,
                resolution
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket["ticket_id"],
            ticket["title"],
            ticket["description"],
            ticket["category"],
            ticket["priority"],
            ticket["status"],
            ticket["source"],
            "\n".join(ticket["evidence"]),
            ticket["created_at"],
            ticket.get("resolution", "")
        ))


def get_open_ticket_by_title(title):
    with get_connection() as connection:
        row = connection.execute("""
            SELECT *
            FROM tickets
            WHERE title = ?
              AND status IN ('Open', 'In Progress')
            ORDER BY id DESC
            LIMIT 1
        """, (title,)).fetchone()

    return row_to_ticket(row)


def get_all_tickets():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT *
            FROM tickets
            ORDER BY id DESC
        """).fetchall()

    return [row_to_ticket(row) for row in rows]


def get_ticket_by_id(ticket_id):
    with get_connection() as connection:
        row = connection.execute("""
            SELECT *
            FROM tickets
            WHERE ticket_id = ?
        """, (ticket_id,)).fetchone()

    return row_to_ticket(row)


def resolve_ticket(ticket_id, resolution):
    resolution = resolution.strip()

    if not resolution:
        return False

    with get_connection() as connection:
        cursor = connection.execute("""
            UPDATE tickets
            SET status = 'Resolved',
                resolution = ?
            WHERE ticket_id = ?
              AND status IN ('Open', 'In Progress')
        """, (resolution, ticket_id))

        return cursor.rowcount > 0