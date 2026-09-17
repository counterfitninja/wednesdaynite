# Research: Safe and Verifiable Administration

## Existing Architecture

The application is a Flask server-rendered application centered in `app.py`, with SQLite persistence and Jinja templates under `templates/`. Existing administrative routes use a `login_required` decorator, while several state-changing routes and upload workflows require a complete security audit. The implementation should preserve this architecture and avoid an unnecessary framework migration.

## Security Approach

Use a lightweight Flask-compatible CSRF implementation or a small application-local validation layer that supports the current server-rendered forms. All state-changing forms must emit a session-bound token, and all covered POST requests must reject missing, malformed, expired, or cross-session tokens before database mutation.

Keep the standard-library `logging` module as the operational logging boundary. Emit event names and safe metadata, never credentials or raw request secrets. Validate local login redirect targets with URL parsing rather than trusting the `next` query parameter.

## Upload and Health Validation

Validate upload size and content type before parsing or storing the file. Keep error responses generic and safe. Health checks should report only a stable status and non-sensitive dependency availability; database exception text and configuration values must not be returned to clients.

## Test Strategy

Use pytest-compatible Flask test-client fixtures backed by temporary SQLite databases. Test security failures for zero database changes, then test successful requests and existing attendance, payment, score, team, import, upload, and abandoned-game rules. Capture logs with pytest logging facilities and assert sensitive values are absent.

## Decisions

- Preserve Flask, SQLite, Jinja, and the current route structure.
- Prefer a small dependency footprint; add a CSRF dependency only if it materially reduces implementation risk.
- Treat security regression tests as required because the constitution and feature specification explicitly require them.
