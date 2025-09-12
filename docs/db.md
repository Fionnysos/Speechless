# Database Documentation

## Tables:

### users
| Column        | Type       | Constraints                | Description                  |
|---------------|------------|----------------------------|------------------------------|
| id            | INTEGER PK | AUTOINCREMENT              | Unique user ID               |
| username      | TEXT       | UNIQUE, NOT NULL           | Username                     |
| password_hash | TEXT       | NOT NULL                   | Password hash (bcrypt)       |
| created_at    | TIMESTAMP  | NOT NULL, UTC              | User creation timestamp      |

---

### sessions
| Column        | Type       | Constraints                | Description                  |
|---------------|------------|----------------------------|------------------------------|
| id            | INTEGER PK | AUTOINCREMENT              | Unique session ID            |
| user_id       | INTEGER FK | NOT NULL → users.id        | Linked user                  |
| session_token | TEXT       | UNIQUE, NOT NULL           | Random session tokeny        |
| created_at    | TIMESTAMP  | NOT NULL, UTC              | Session creation timestamp   |
| expires_at    | TIMESTAMP  | NOT NULL, UTC              | Session expiration timestamp |

---

### conversations
| Column        | Type       | Constraints                | Description                  |
|---------------|------------|----------------------------|------------------------------|
| id            | INTEGER PK | AUTOINCREMENT              | Unique conversation ID       |
| user1_id      | INTEGER FK | NOT NULL → users.id        | First participant            |
| user2_id      | INTEGER FK | NOT NULL → users.id        | Second participant           |
| created_at    | TIMESTAMP  | NOT NULL, UTC              | Conversation creation time   |

---

### messages
| Column         | Type       | Constraints                | Description                       |
|----------------|------------|----------------------------|-----------------------------------|
| id             | INTEGER PK | AUTOINCREMENT              | Unique message ID                 |
| conversation_id| INTEGER FK | NOT NULL → conversations.id| Linked conversation               |
| sender_id      | INTEGER FK | NOT NULL → users.id        | Sender of the message             |
| content        | TEXT       | NOT NULL, max 2000 chars   | Message text                      |
| created_at     | TIMESTAMP  | NOT NULL, UTC              | Message creation timestamp        |

---

### Indexes
- `users(username)` → UNIQUE  
- `sessions(session_token)` → UNIQUE  
- `sessions(user_id)` → INDEX  
- `messages(conversation_id, id)` → INDEX (for polling efficiency)

---

### Polling Strategy
- **Variant:** `since_id` → `GET /messages?since_id=<id>`  
- Advantage: stable, fast index lookup.
