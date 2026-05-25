#!/usr/bin/env python3
"""
Femirins Budget CLI - A minimalist, scriptable budgeting tool for power users.
"""

import sqlite3
import argparse
import csv
import json
from pathlib import Path
from typing import List, Dict, Optional

# Database setup
DB_PATH = Path.home() / ".femirins-budget.db"


def init_db():
    """Initialize the SQLite database with tables for transactions and budgets."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            tags TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            period TEXT DEFAULT 'monthly'
        )
        """)
        conn.commit()


def add_transaction(date: str, description: str, amount: float, category: Optional[str] = None, tags: Optional[str] = None):
    """Add a transaction to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (date, description, amount, category, tags) VALUES (?, ?, ?, ?, ?)",
            (date, description, amount, category, tags)
        )
        conn.commit()


def list_transactions() -> List[Dict]:
    """List all transactions."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def export_transactions(format: str = "csv") -> str:
    """Export transactions to CSV or JSON."""
    transactions = list_transactions()
    if format == "csv":
        output = "date,description,amount,category,tags\n"
        for t in transactions:
            output += f"{t['date']},{t['description']},{t['amount']},{t['category'] or ''},{t['tags'] or ''}\n"
        return output
    elif format == "json":
        return json.dumps(transactions, indent=2)
    else:
        raise ValueError("Unsupported format. Use 'csv' or 'json'.")


def main():
    parser = argparse.ArgumentParser(description="Femirins Budget CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize the database")

    # Add transaction command
    add_parser = subparsers.add_parser("add", help="Add a transaction")
    add_parser.add_argument("--date", required=True, help="Transaction date (YYYY-MM-DD)")
    add_parser.add_argument("--description", required=True, help="Transaction description")
    add_parser.add_argument("--amount", type=float, required=True, help="Transaction amount")
    add_parser.add_argument("--category", help="Transaction category")
    add_parser.add_argument("--tags", help="Comma-separated tags")

    # List transactions command
    list_parser = subparsers.add_parser("list", help="List all transactions")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export transactions")
    export_parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Export format")

    args = parser.parse_args()

    if args.command == "init":
        init_db()
        print("Database initialized.")
    elif args.command == "add":
        add_transaction(args.date, args.description, args.amount, args.category, args.tags)
        print("Transaction added.")
    elif args.command == "list":
        transactions = list_transactions()
        for t in transactions:
            print(f"{t['date']} | {t['description']} | ${t['amount']:.2f} | {t['category'] or 'N/A'}")
    elif args.command == "export":
        print(export_transactions(args.format))


if __name__ == "__main__":
    main()