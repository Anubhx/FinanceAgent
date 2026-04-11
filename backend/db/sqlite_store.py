import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "finance.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT,
            created_at TEXT
        );
        
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            date TEXT,
            name TEXT,
            amount REAL,
            category TEXT,
            source TEXT,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            filename TEXT,
            file_type TEXT,
            parsed_count INTEGER,
            uploaded_at TEXT
        );
    """)
    conn.commit()
    conn.close()

def upsert_user(user_id: str, email: str = ""):
    conn = get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO users (id, email, created_at) VALUES (?, ?, ?)",
        (user_id, email, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def store_transactions(user_id: str, transactions: list[dict], source: str):
    conn = get_conn()
    for t in transactions:
        conn.execute(
            "INSERT INTO transactions (user_id, date, name, amount, category, source, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, t.get("date"), t.get("name"), t.get("amount"), t.get("category", "Other"), source, datetime.now().isoformat())
        )
    conn.commit()
    conn.close()

def get_user_transactions(user_id: str, limit: int = 100) -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT date, name, amount, category FROM transactions WHERE user_id = ? ORDER BY date DESC LIMIT ?",
        (user_id, limit)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def log_upload(user_id: str, filename: str, file_type: str, parsed_count: int):
    conn = get_conn()
    conn.execute(
        "INSERT INTO uploaded_files (user_id, filename, file_type, parsed_count, uploaded_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, filename, file_type, parsed_count, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

# Initialise on import
init_db()
