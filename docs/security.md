# Security (MVP)

## Passwords
- Store passwords only as bcrypt hashes (never plaintext).
- Minimum length: 8 characters.

## Sessions & Cookies
- Server-side sessions stored in the database.  
- Browser only receives a random `session_token` via cookie.  
- Expiry: 7 days.  
- Cookie name: `sid`.  

### Cookie Flags
- **HttpOnly:** prevents JavaScript from reading the cookie; only the browser sends it automatically.  
  - `enabled`
- **SameSite:** controls when the browser includes the cookie in requests:
  - `Lax`: sent for normal navigation requests (links, top-level requests). Blocks most cross-site attacks.
- **Secure:** cookie is only sent via HTTPS (not HTTP). For production = enabled, for local development = disabled.

## Errors
- Use consistent HTTP codes:  
  - 200/201 → success  
  - 400 → bad request (missing/invalid data)  
  - 401 → unauthorized (not logged in / bad credentials)  
  - 409 → conflict (e.g., username already exists)

## Non-Goals (MVP)
- No password reset flow.  
- No CSRF tokens (safe as long as frontend and backend share the same origin).  
- No 2FA.  
