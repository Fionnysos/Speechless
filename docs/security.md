# Security (MVP)

## Passwords
- Store passwords only as bcrypt hashes (never plaintext).
- Minimum length: 8 characters; document bcrypt cost factor (e.g., 12).

## Sessions & Cookies
- Server-side sessions in DB; cookie carries only an opaque `session_token` (no user data).
- Expiry: 7 days **with sliding TTL** (refresh on each authenticated request).
- On successful login: **session rotation** (issue a new session).
- On logout: mark session as revoked and invalidate cookie (Max-Age=0).
- Cookie name: `sid`.

### Cookie Flags
- **HttpOnly:** enabled (prevents JS access).
- **SameSite:** `Lax` (mitigates most cross-site requests).
- **Secure:** enabled in production (HTTPS only); may be disabled only for local dev if HTTPS is unavailable.
- **Path:** `/`
- **Max-Age:** `604800` (7 days)

## CSRF (tokenless, MVP)
- No state changes via GET.
- For POST/DELETE: enforce `Origin`/`Referer` to match your exact origin.
- Additionally require a custom header (e.g., `X-Requested-With: fetch`) from the frontend.

## Errors
- 200/201 → success
- 204 → logout success (no content, cookie cleared)
- 400 → bad request (missing/invalid data)
- 401 → unauthorized (no/invalid session or bad credentials)
- 409 → conflict (e.g., username already exists)

## Rate Limiting (Auth)
- Login: at most 5 failed attempts per 15 minutes per IP/username; apply exponential backoff.
- Return a generic error for invalid credentials.

## Logging & Privacy
- Never log passwords or session tokens.
- Log minimal metadata (user_id, route, status code, UTC timestamp).

## Non-Goals (MVP)
- No password reset.
- No CSRF tokens (Origin/Referer check suffices for same-origin MVP).
- No 2FA.
