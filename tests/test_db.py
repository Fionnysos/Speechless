import sqlite3

import pytest
import backend.db

@pytest.fixture()
def startup_database():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.cursor().executescript("""PRAGMA foreign_keys = ON;

    CREATE TABLE "users" (
        "id"            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "username"      TEXT NOT NULL UNIQUE,
        "password_hash" TEXT NOT NULL,
        "created_at"    TEXT NOT NULL
    );

    CREATE TABLE "sessions" (
        "id"            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "user_id"       INTEGER NOT NULL,
        "session_token" TEXT NOT NULL UNIQUE,
        "created_at"    TEXT NOT NULL,
        "last_seen_at"  TEXT NOT NULL,
        "expires_at"    TEXT NOT NULL,
        "revoked"       INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY("user_id") REFERENCES "users"("id")
    );

    CREATE TABLE "conversations" (
        "id"        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "user1_id"  INTEGER NOT NULL,
        "user2_id"  INTEGER NOT NULL,
        "created_at" TEXT NOT NULL,
        FOREIGN KEY("user1_id") REFERENCES "users"("id"),
        FOREIGN KEY("user2_id") REFERENCES "users"("id")
    );

    CREATE TABLE "messages" (
        "id"              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "conversation_id" INTEGER NOT NULL,
        "sender_id"       INTEGER NOT NULL,
        "content"         TEXT NOT NULL,
        "created_at"      TEXT NOT NULL,
        FOREIGN KEY("conversation_id") REFERENCES "conversations"("id"),
        FOREIGN KEY("sender_id") REFERENCES "users"("id"),
        CHECK(length(content) <= 2000)
    );
    """)
    return conn

# Users

@pytest.mark.parametrize("username, hashed_password, created_at", [("testname", "$2b$12$LwCTz/h8D1GCFWLRRzcwbOnTSR88vi1A6fVz8tFxEuKuHX1eBcpE2", "2025-09-16T12:42:38Z")])
class TestUserCreation:

    def test_valid_user_creation(self, startup_database, username, hashed_password, created_at):
        backend.db.create_user_database(startup_database, username, hashed_password, created_at)
        row = startup_database.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        assert row["username"] == username is not None

    def test_user_creation_unique_username(self, startup_database, username, hashed_password, created_at):
        backend.db.create_user_database(startup_database, username, hashed_password, created_at)
        with pytest.raises(sqlite3.IntegrityError):
            backend.db.create_user_database(startup_database, username, hashed_password, created_at)

@pytest.mark.parametrize("username, hashed_password, created_at", [("testname", None, "2025-09-16T12:42:38Z")])
def test_user_creation_with_none(startup_database, username,hashed_password,created_at):
    with pytest.raises(sqlite3.IntegrityError):
        backend.db.create_user_database(startup_database, username, hashed_password, created_at)

# Sessions
@pytest.mark.parametrize("username, password, created_at", [("testname", "test12345678", "2025-09-16T12:42:38Z")])
def test_valid_session_creation(startup_database, username, password, created_at):
    backend.db.create_session(startup_database, username, password)
    row = startup_database.execute("SELECT * FROM sessions WHERE userID = ?", (username,)).fetchone()
    assert row is not None















