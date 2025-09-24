import sqlite3

import pytest
import backend.db

def startup_database():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;,")
    cursor.execute("""""")
    return conn

conn = startup_database()
conn.cursor().execute("PRAGMA foreign_keys = ON;")

