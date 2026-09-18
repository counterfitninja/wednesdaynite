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

## Import Request

- A CSV/import request is accepted only within configured byte, row, field-count,
	and field-length limits.
- Required headers and values are validated before writes.
- Unknown, duplicate, malformed, or overlong names are rejected or reported by a
	documented safe policy.
- Writes are transactional: a failed request leaves the database unchanged.

## Health Response

- Healthy response contains stable `status` and `build_version` fields only.
- Database failure returns a stable non-sensitive degraded/error status and an
	appropriate non-2xx response.
- Host, port, filesystem paths, SQL text, exception details, and configuration
	secrets are never response fields.

## Relationship Invariants

- Attendance, team assignments, payments, share tokens, and historical game
	records retain valid player/game references under SQLite foreign keys.
- Player merge/delete operations explicitly migrate, reconcile, or remove every
	dependent relationship; they must not silently orphan history.
- A rejected authorization, CSRF, validation, or upload request changes neither
	persisted rows nor an existing valid uploaded asset.
