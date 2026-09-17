# Quickstart Validation: Wednesday Night FC Improvements

## Prerequisites

- Windows PowerShell.
- Python environment with `requirements.txt` and test dependencies installed.
- A temporary test database; do not run feature tests against `football.db`.

## Automated validation

From the repository root:

1. Run the focused feature tests with `pytest`.
2. Run `python -m py_compile app.py` and compile any new Python modules.
3. Run `git diff --check`.

Expected result: authentication, CSRF, migration integrity, attendance/payment rules, scores, abandoned games, imports, team assignment, dashboard behavior, and health checks pass against isolated SQLite data.

## Manual matchday validation

1. Log in using the shared administrator account.
2. Confirm anonymous requests cannot mutate protected routes.
3. Confirm every state-changing form and AJAX request rejects a missing or invalid CSRF token.
4. Create an upcoming game and verify the home page surfaces it as the primary card.
5. Open the game and verify attendance, payments, teams, and result actions are distinct.
6. At a 390px viewport, assign and unassign players using buttons or selectors rather than drag-and-drop.
7. Disable connectivity, submit attendance/payment changes, restore connectivity, and confirm independent synchronization, conflict warnings, retry behavior, and no data loss.
8. Log out and verify authenticated caches are cleared and private pages are not available to an unauthenticated browser.
9. Activate a new service-worker version and confirm old caches are deleted and current HTML is loaded.
10. Use keyboard-only navigation and confirm visible focus, labels, landmarks, and non-color status indicators.

## Operational validation

- Run migration tests against a copied legacy database and a fresh database.
- Confirm production configuration supplies a strong `SECRET_KEY` and `ADMIN_PASSWORD`.
- Confirm logs contain no passwords, secrets, tokens, or unnecessary personal data.
- Confirm OCR is not imported or initialized during ordinary web startup when unused.
