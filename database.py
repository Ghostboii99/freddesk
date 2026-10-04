import sqlite3

DB_NAME = "freddesk.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
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

    connection.commit()
    connection.close()


def save_ticket(ticket):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
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
        ticket["resolution"]
    ))

    connection.commit()
    connection.close()


def get_open_ticket_by_title(title):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM tickets
        WHERE title = ?
        AND status = 'Open'
        ORDER BY id DESC
        LIMIT 1
    """, (title,))

    row = cursor.fetchone()
    connection.close()

    return row
