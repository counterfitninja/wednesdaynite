# Matchday Workflow Contract

## Protected session behavior

- `GET /login` renders the shared administrator login form.
- Successful login creates a Flask session and redirects only to a same-origin path.
- Unauthenticated requests to protected routes redirect to `/login` without changing data.
- State-changing requests without a valid CSRF token are rejected without changing data.
- `POST /logout` clears the session and private browser caches.

## Dashboard and game workflow

- `GET /` presents the next upcoming non-abandoned game, when one exists, with date, location, attendance summary, payment status, and primary actions.
- `GET /games/<id>` presents distinct attendance, payments, teams, and result sections.
- Existing route contracts should remain backward-compatible unless a migration is documented.

## Offline synchronization

- Attendance and payment updates may be queued while offline.
- Each queued operation has a unique operation ID and is synchronized independently.
- Synchronization reports success, conflict, or rejection without exposing secrets.
- Conflicts apply latest successful update wins and produce a visible administrator warning.
- Rejected operations retry automatically with backoff and do not block unrelated operations.

## Health and observability

- `GET /healthz` remains a lightweight health check.
- Diagnostics and logs exclude passwords, session secrets, tokens, and unnecessary personal data.
- Health or smoke validation must cover authentication, representative mutations, statistics, and migration/database connectivity.
