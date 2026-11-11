"""Regression tests for FredDesk V2.1 database behavior.

Run: python -m unittest discover -s tests -v
Each test uses an isolated temporary SQLite database.
"""
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import database
from ticket import create_ticket


class IncidentPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_patch = patch.object(
            database, "DB_NAME", Path(self.temp_dir.name) / "test.db"
        )
        self.db_patch.start()
        self.addCleanup(self.db_patch.stop)
        database.initialize_database()

    def new_ticket(self, title="High Memory Usage"):
        return create_ticket(
            title, "Threshold exceeded", "Performance",
            evidence=["Memory utilization: 91%"]
        )

    def test_ticket_persists_across_new_connections(self):
        ticket = self.new_ticket()
        database.save_ticket(ticket)
        saved = database.get_ticket_by_id(ticket["ticket_id"])
        self.assertEqual(saved["ticket_id"], ticket["ticket_id"])
        self.assertEqual(saved["status"], "Open")
        self.assertEqual(saved["evidence"], ticket["evidence"])
        self.assertEqual(len(database.get_all_tickets()), 1)

    def test_duplicate_suppression_lookup_for_open_ticket(self):
        ticket = self.new_ticket()
        database.save_ticket(ticket)
        existing = database.get_open_ticket_by_title(ticket["title"])
        self.assertIsNotNone(existing)
        self.assertEqual(existing["ticket_id"], ticket["ticket_id"])
        # Mirrors the application's conditional insertion; not atomic deduplication.
        if not existing:
            database.save_ticket(self.new_ticket())
        self.assertEqual(len(database.get_all_tickets()), 1)

    def test_resolution_persists_and_cannot_repeat(self):
        ticket = self.new_ticket()
        database.save_ticket(ticket)
        self.assertTrue(database.resolve_ticket(
            ticket["ticket_id"], "Closed after investigation"
        ))
        stored = database.get_ticket_by_id(ticket["ticket_id"])
        self.assertEqual(stored["status"], "Resolved")
        self.assertEqual(stored["resolution"], "Closed after investigation")
        self.assertFalse(database.resolve_ticket(
            ticket["ticket_id"], "Second resolution"
        ))
        self.assertIsNone(database.get_open_ticket_by_title(ticket["title"]))

    def test_blank_resolution_rejected(self):
        ticket = self.new_ticket()
        database.save_ticket(ticket)
        self.assertFalse(database.resolve_ticket(ticket["ticket_id"], "   "))
        self.assertEqual(
            database.get_ticket_by_id(ticket["ticket_id"])["status"], "Open"
        )

    def test_duplicate_ticket_id_rejected(self):
        ticket = self.new_ticket()
        database.save_ticket(ticket)
        with self.assertRaises(sqlite3.IntegrityError):
            database.save_ticket(ticket)
        self.assertEqual(len(database.get_all_tickets()), 1)


if __name__ == "__main__":
    unittest.main()
