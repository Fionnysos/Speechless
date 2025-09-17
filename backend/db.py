from datetime import datetime, timedelta

import bcrypt

from backend import exceptions
import sqlite3
import secrets
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db", "app.db")

def startup_database():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_user_database(username, hashed_password, created_at):
    conn = startup_database()
    conn.cursor().execute("INSERT INTO users (username,password_hash, created_at) VALUES (?, ?, ?)", (username, hashed_password, created_at))
    conn.commit()
    user_id = conn.cursor().lastrowid
    conn.close()
    return "User created: (?,?)", (user_id, username)

def get_user(username, password):
    conn = startup_database()
    user = conn.cursor().execute("SELECT id, username, password_hash, created_at FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if user is None:
        raise exceptions.UserNotFoundError("User not found")
    else:
        if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            print("Login Successfully")
            return user
        else:
            raise exceptions.InvalidPasswordError("Wrong Password!")


def create_session(username, password):
    conn = startup_database()
    db_user = get_user(username,password)
    token_str = secrets.token_urlsafe(64)
    created_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    expires_at_raw = datetime.now() + timedelta(days=7)
    expires_at = expires_at_raw.strftime("%Y-%m-%dT%H:%M:%SZ")
    conn.cursor().execute("INSERT INTO sessions (user_id, session_token, created_at, last_seen_at, expires_at) VALUES (?,?,?,?,?)", (db_user["id"], token_str, created_at, created_at, expires_at))
    conn.commit()
    conn.close()
    return token_str