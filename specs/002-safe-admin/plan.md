# Implementation Plan: Safe and Verifiable Administration

## Technical Context

- Existing Flask application and routes remain the integration point in `app.py`.
- SQLite remains the database; tests use isolated temporary databases.
- Jinja templates under `templates/` receive CSRF fields and safe error pages.
- Structured logging uses Python's standard `logging` module.
- Focused tests use Flask's test client and pytest-compatible fixtures.

## Project Structure

- `app.py`: authentication, CSRF integration, logging, error handlers, database setup, and route behavior.
- `templates/`: login, error, and state-changing forms.
- `tests/`: isolated authentication, CSRF, rules, imports, uploads, observability, and health tests.
- `requirements.txt`: test and CSRF dependencies if required.
- `README.md`: security and operational documentation.

## Delivery Strategy

1. Establish isolated test database fixtures.
2. Add security configuration and CSRF protection.
3. Add safe logging and error handling.
4. Preserve and cover existing game/payment/import rules.
5. Validate upload and health-check behavior.
6. Run the complete focused test suite and syntax checks.

## Quality Gates

- Every covered admin mutation rejects unauthenticated and invalid-CSRF requests.
- No credentials appear in captured logs.
- Core game rules remain regression-tested.
- `python -m py_compile app.py` passes.
- `git diff --check` passes.
