# Research: Safe and Verifiable Administration

## Existing Architecture

The application is a Flask server-rendered application centered in `app.py`, with SQLite persistence and Jinja templates under `templates/`. Existing administrative routes use a `login_required` decorator, while several state-changing routes and upload workflows require a complete security audit. The implementation should preserve this architecture and avoid an unnecessary framework migration.

## Findings

The repository already has application-local CSRF validation, secure-cookie
defaults, local `next` URL validation, safe error templates, SQLite foreign-key
activation, and basic upload limits. The main risk is incomplete or inconsistent
coverage: `edit_player` is publicly mutable, team generation mutates on GET,
AJAX payment requests omit their CSRF token, and signed CSRF tokens are accepted
across sessions. Imports expose raw exception text, replacement uploads can delete
the old asset before validation, SVG checks are unsafe, and health checks expose
unnecessary host/port data without checking the database.

## Decisions

### Decision: Harden the existing application-local CSRF layer

Require an exact token match with the current session and reject missing,
malformed, expired, and cross-session tokens before route execution. Add tokens
to every server form and the payment AJAX request. Do not add Flask-WTF or
another dependency because the existing serializer and test seams are sufficient.

### Decision: Audit and classify the full mutation surface

Protect every administrative mutation, specifically `edit_player`, and convert
or split GET routes that write state, specifically team generation and public
game auto-creation as compatibility allows. Validate referenced IDs and allowed
status/score values before writes. Keep public read-only pages explicitly public.

### Decision: Use redacted structured logging

Use standard-library logging with event names, route, method, outcome, and safe
stable IDs only. Never log passwords, secret values, raw CSRF/session/share
tokens, contact data, complete request bodies, or raw exception details. Log
exception details only through controlled server logs when needed for diagnosis.

### Decision: Make uploads validate-before-replace and imports bounded

Read within explicit byte/row/field limits, validate content rather than relying
only on extensions, process into a temporary output, and atomically replace an
existing asset only after success. Reject or safely rasterize SVG rather than
serving unsanitized active content. Imports must be transactional and return
generic user-facing errors.

### Decision: Define a minimal database-aware health contract

Return only stable status and build version on success. Probe the database and
return a stable non-sensitive degraded/503 response on failure; do not expose
host, port, database paths, or exception text. Keep `/status` behavior aligned
with `/healthz`.

### Decision: Test behavior at the route and invariant boundaries

Use temporary SQLite databases and Flask's test client. For rejected requests,
assert zero database/file changes. Cover authentication, CSRF lifecycle, all
mutation categories, upload/import limits, merge/delete semantics, safe logs,
health failure, and 403/404/500 responses. This verifies both security and
preservation of existing football business rules.

## Alternatives Considered

- **Flask-WTF or a new CSRF package**: rejected for unnecessary dependency and
	migration cost while a local mechanism already exists.
- **Large blueprint/service refactor**: deferred to the maintainability feature;
	it would increase the change surface during a security hardening increment.
- **Return detailed import/database errors to users**: rejected because it leaks
	implementation details; retain details only in controlled logs.
- **Delete-and-recreate uploads**: rejected because failed validation can destroy
	a valid existing asset; use atomic replacement.
