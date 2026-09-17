# Implementation Plan: Wednesday Night FC Improvements

## Technical Context

- Existing application: Flask 3.0 server-rendered web application in `app.py`.
- Persistence: SQLite database with numbered, repeatable migrations and foreign-key enforcement on every connection.
- UI: Jinja templates under `templates/`, with shared styles extracted incrementally into `static/app.css`.
- Client assets: JavaScript and PWA files under `static/`; IndexedDB or an equivalent browser store for independent offline mutation records.
- Testing: pytest with Flask's test client and isolated temporary SQLite databases.
- Deployment: Gunicorn-compatible Flask application; OCR dependencies remain optional and must not load during ordinary startup.

## Project Structure

- `app.py`: current routes and compatibility surface; split database, auth, and domain services incrementally after regression coverage.
- `db.py`, `auth.py`, `services/`: extracted testable boundaries for persistence, shared-session security, statistics, payments, teams, and OCR.
- `templates/`: page templates and new reusable partials.
- `static/app.css`: shared visual system.
- `static/notifications.js`, `static/service-worker.js`: PWA and notifications.
- `tests/`: focused regression and workflow tests with isolated SQLite fixtures.
- `specs/001-wnfc-improvements/`: feature design artifacts.

## Constitution Check

- **Matchday Value First**: Pass — dashboard, game workflow, attendance, teams, and mobile paths are prioritized.
- **Data Integrity Over Convenience**: Pass — migrations, foreign keys, conflict metadata, abandoned-game rules, and delete/merge tests are required.
- **Secure by Default**: Pass — shared-session auth, CSRF, secure cookies, safe redirects, secret-free logs, and upload validation are required.
- **Tested, Observable, and Verifiable**: Pass — focused pytest coverage, health checks, smoke validation, and diagnostics are planned.
- **Simple, Accessible, and Maintainable**: Pass — incremental extraction, shared CSS, keyboard access, visible focus, and non-color status indicators avoid a rewrite.
- **Intentional exception**: The clarification requests automatic indefinite retries without user notification. The design preserves automatic retries but adds bounded backoff, independent queue progress, safe diagnostics, and visible conflict/rejection state to prevent silent data loss.

## Delivery Strategy

1. Complete security, observability, test, and query foundations.
2. Deliver the matchday dashboard and game-detail workflow.
3. Improve navigation, responsive UI, accessibility, and shared styling.
4. Improve mobile team assignment and attendance editing.
5. Refactor backend modules and migrations after behavior is covered by tests.
6. Finish PWA, notification, backup, and deployment improvements.

## Quality Gates

- Run focused regression tests for each story.
- Run `python -m py_compile app.py` and editor diagnostics.
- Run `git diff --check`.
- Validate primary workflows at desktop and mobile widths.
- Update user-facing documentation when behavior changes.

## Design Artifacts

- `research.md`: technology and implementation decisions.
- `data-model.md`: domain entities, synchronization metadata, and integrity rules.
- `contracts/matchday-workflow.md`: session, dashboard, offline synchronization, and health contracts.
- `quickstart.md`: automated, manual, and operational validation scenarios.
