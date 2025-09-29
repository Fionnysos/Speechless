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
| Column        | Type       | Constraints                  | Description                                 |
|---------------|------------|------------------------------|---------------------------------------------|
| id            | INTEGER PK | AUTOINCREMENT                | Internal DB identifier                      |
| user_id       | INTEGER FK | NOT NULL → users.id          | Linked user                                 |
| session_token | TEXT       | UNIQUE, NOT NULL             | Random opaque token stored in cookie        |
| created_at    | TIMESTAMP  | NOT NULL, UTC                | Session creation time                       |
| last_seen_at  | TIMESTAMP  | NOT NULL, UTC                | Last activity (used for sliding TTL)        |
| expires_at    | TIMESTAMP  | NOT NULL, UTC, INDEX         | Session expiration time                     |
| revoked       | INTEGER    | NOT NULL, DEFAULT 0          | 0 = active, 1 = revoked by user/logout      |

---

### calls
| Column       | Type       | Constraints         | Description                                                      |
|--------------|------------|---------------------|------------------------------------------------------------------|
| id           | INTEGER PK | AUTOINCREMENT       | Internal DB identifier                                           |
| user_id      | INTEGER FK | NOT NULL → users.id | Initiating user                                                  |
| status       | TEXT       | NOT NULL            | Call state (`created`, `dialing`, `connected`, `ended`, `error`) |
| created_at   | TIMESTAMP  | NOT NULL, UTC       | When the call was created                                        |
| connected_at | TIMESTAMP  | NULL, UTC           | When the call was connected (NULL if not yet connected)          |
| ended_at     | TIMESTAMP  | NULL, UTC           | When the call ended (NULL if still active)                       |
| provider_id  | TEXT       | OPTIONAL            | External provider reference (for real PSTN integration)          |

---

### utterances
| Column     | Type       | Constraints         | Description                                                       |
|------------|------------|---------------------|-------------------------------------------------------------------|
| id         | INTEGER PK | AUTOINCREMENT       | Internal DB identifier                                            |
| call_id    | INTEGER FK | NOT NULL → calls.id | Associated call                                                   |
| direction  | TEXT       | NOT NULL            | `outbound_tts` (system speaking) or `inbound_stt` (remote speech) |
| text       | TEXT       | NOT NULL            | Utterance text                                                    |
| is_final   | INTEGER    | NOT NULL, DEFAULT 0 | 0 = partial, 1 = final (for STT results)                          |
| created_at | TIMESTAMP  | NOT NULL, UTC       | When this utterance was created                                   |

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
