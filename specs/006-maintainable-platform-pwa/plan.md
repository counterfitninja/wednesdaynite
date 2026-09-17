# Implementation Plan: Maintainable Platform and Reliable PWA

## Technical Context

- Existing application: Flask server-rendered web application currently centered in `app.py`.
- Persistence: SQLite database in `football.db`; preserve existing records and route behavior.
- Migrations: Add an ordered migration runner and migration table under `migrations/` with startup integration in `app.py`.
- Backend structure: Extract incrementally into `db.py`, `auth.py`, `services/`, and `routes/` while retaining a compatibility boundary for existing imports.
- UI/PWA: Jinja templates under `templates/`; service worker and notification client assets under `static/`.
- Testing: pytest-compatible Flask tests with isolated temporary SQLite databases plus JavaScript/service-worker unit tests where the repository's test harness supports them.
- Packaging: Keep the default runtime profile lightweight; move OCR-only packages to `requirements-ocr.txt` and use guarded imports.

## Project Structure

- `app.py`: application factory/startup wiring and compatibility route registration during extraction.
- `db.py`: connection, transaction, foreign-key, backup, and migration-runner integration.
- `auth.py`: authentication helpers extracted without changing route contracts.
- `services/`: statistics, payments, teams, OCR adapter, and other domain services.
- `routes/`: route blueprints or route modules introduced incrementally.
- `migrations/`: ordered migration modules and migration registry.
- `static/service-worker.js`: versioned cache lifecycle, navigation strategy, and offline fallback.
- `static/notifications.js`: explicit opt-in and safe notification state handling.
- `templates/`: opt-in UI, offline fallback, and safe OCR-unavailable feedback.
- `tests/`: migration, module-boundary, PWA, notification, backup/restore, and regression tests.
- `requirements.txt`, `requirements-ocr.txt`: dependency profiles.
- `README.md`, `RELEASE_CHECKLIST.md`, `HOW_IT_WORKS.md`: operational documentation.

## Design Decisions

1. Use an application-owned migration table with immutable numeric/string versions; startup applies only pending migrations in order.
2. Enable SQLite foreign keys on every connection and test behavior before changing delete semantics.
3. Extract modules in compatibility-preserving slices; route URLs, methods, response statuses, redirects, and database behavior remain regression-tested.
4. Use network-first navigation handling in the service worker, with a versioned static cache and a small local offline fallback.
5. Do not request notification permission during page load; require an explicit user action and persist opt-in/last-prompt state.
6. Guard OCR imports behind a service adapter so ordinary application startup does not require OCR packages.
7. Treat backup/restore as an operational workflow with verification, not as an unverified file copy.

## Delivery Strategy

1. Establish isolated fixtures and characterization tests for startup, routes, migrations, PWA, notifications, and OCR availability.
2. Add migration and foreign-key infrastructure with backup/restore helpers.
3. Extract backend modules in small compatibility-preserving slices.
4. Harden service-worker cache/version/update behavior and add the offline fallback.
5. Change notification behavior to explicit opt-in and recoverable no-op states.
6. Separate optional OCR dependencies and document installation profiles.
7. Run full regression, module-import, migration, PWA, and operational verification.

## Quality Gates

- Migration application is ordered, repeatable, recorded, and data-preserving.
- SQLite foreign-key behavior is explicitly tested.
- Existing route contracts and full regression suite remain green after extraction.
- Service-worker tests prove old-cache cleanup and non-stale navigation behavior.
- Notification tests prove no repeated or automatic permission prompts.
- Base installation starts without OCR dependencies; OCR-unavailable behavior is safe.
- Backup restore verification and rollback guidance are documented.
- `python -m py_compile` and `git diff --check` pass.
