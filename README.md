# Speechless – MVP

**Speechless** is a web application that supports people with speech impairments (e.g., stuttering, selective mutism, deafness).  
Users can register, log in, and later enter text that will be spoken aloud via text-to-speech.

---

## Project Structure

```
/backend       → FastAPI app, DB logic, authentication  
/frontend      → HTML/JS (Login, Register, Chat)  
/docs          → Project documentation (api.md, db.md, security.md, …)  
```

---

## Requirements

- Python 3.11+  
- SQLite (bundled with Python)  
- Dependencies listed in `docs/dependencies.md`  

---

## Setup

1. Clone the repository or download the project.  
2. Create a virtual environment:  
   ```bash
   python -m venv .venv
   ```
3. Activate the environment:  
   - Linux/Mac:  
     ```bash
     source .venv/bin/activate
     ```  
   - Windows (PowerShell):  
     ```powershell
     .venv\Scripts\activate
     ```
4. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
5. Initialize the database (if not already present):  
   ```bash
   python backend/init_db.py
   ```
   → creates `backend/db/app.db` and sets up tables (`users`, `sessions`, …).

---

## Start the Server

```bash
uvicorn backend.main:app --reload
```

- Default URL: `http://127.0.0.1:8000`  
- API endpoints: see [`docs/api.md`](docs/api.md)  

---

## Frontend

Open in browser:  
- `frontend/register.html` → registration form  
- `frontend/login.html` → login form  
- `frontend/chat.html` → simple chat (placeholder for TTS calls)  

---

## Security (MVP)

- **Passwords**: stored only as bcrypt hashes (never plaintext).  
- **Sessions**: server-side, persisted in DB, sent via cookie `sid`.  
- **Cookie flags**:  
  - `HttpOnly`  
  - `SameSite=Lax`  
  - `Secure` (enabled in production only)  

---

## Notes

- This is the MVP (minimum viable product).  
- No password reset, no CSRF tokens, no 2FA for now.  
- Later versions will extend functionality with TTS calls.  
