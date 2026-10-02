"""SQLite helpers for the Dunbar clinic application."""

import os
import sqlite3

from flask import g

SCHEMA = """
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT,
    client_type TEXT,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS animals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    name TEXT NOT NULL,
    species TEXT NOT NULL,
    breed TEXT
);

CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    name TEXT NOT NULL,
    locality TEXT NOT NULL,
    access_notes TEXT
);

CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    kind TEXT NOT NULL,                 -- 'consultation' | 'farm_visit'
    day TEXT NOT NULL,                  -- YYYY-MM-DD
    start_time TEXT NOT NULL,           -- HH:MM
    room TEXT,                          -- consulting room, consultation only
    animal_id INTEGER REFERENCES animals(id),     -- consultation only
    property_id INTEGER REFERENCES properties(id), -- farm visit only
    duration_hours REAL,                -- farm visit only, hours > 0
    reason TEXT,
    status TEXT NOT NULL DEFAULT 'booked'  -- 'booked' | 'cancelled'
);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app_db_path())
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def app_db_path():
    from flask import current_app
    db_path = current_app.config["DATABASE"]
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return db_path


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(path):
    """Initialise schema. Used by CLI entry and tests."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
