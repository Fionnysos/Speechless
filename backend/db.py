import sqlite3

def startup_database():
    conn = sqlite3.connect("../db/app.db")
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