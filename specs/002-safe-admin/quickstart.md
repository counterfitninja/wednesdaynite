# Safe Administration Quickstart

1. Configure a test secret and admin credential in the test environment.
2. Run the isolated test suite with a temporary SQLite database.
3. Verify anonymous access redirects from `/admin`, `/admin/games`, and representative mutation routes.
4. Submit a state-changing form without a CSRF token and verify no data changes.
5. Submit a valid CSRF-protected form and verify the intended data change.
6. Exercise attendance, payment, score, team, import, upload, and abandoned-game rules.
7. Capture logs during login and mutation requests; verify credentials and tokens are absent.
8. Request 403, 404, 500, and `/healthz`; verify safe responses.
9. Run `python -m py_compile app.py` and `git diff --check`.
