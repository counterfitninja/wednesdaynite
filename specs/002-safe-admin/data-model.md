# Data Model: Safe and Verifiable Administration

## Admin Session

- `session['logged_in']`: authenticated session marker; must be protected by a strong production `SECRET_KEY`.
- Session cookies must use secure production settings: `HttpOnly`, `SameSite=Lax`, and `Secure` when HTTPS is enabled.
- Login redirect targets are relative/local only; external URLs are rejected or replaced with the admin landing page.

## Game Record

Existing `games` rows retain their current schema and historical values. Related attendance, team assignments, payments, scores, and abandoned-game state must remain backward-compatible. Abandoned games remain distinguishable and excluded from statistics where current business rules require it.

## Player Record

Existing `players` rows retain identity, aliases, skill, contact, attendance, and payment attributes. Deletion or merge behavior must preserve documented historical relationships and must not silently corrupt game history.

## Upload

Uploads are validated before processing or storage:

- supported content types/formats must be explicitly allow-listed;
- size must be bounded by the application limit;
- malformed or oversized content must be rejected without unsafe storage;
- user-facing errors must not expose filesystem paths, stack traces, or secrets.

## Application Log Event

Structured events may include event name, route, outcome, and non-sensitive identifiers needed for diagnosis. They must not include passwords, secret values, CSRF tokens, session cookies, raw credentials, or unnecessary personal data.
