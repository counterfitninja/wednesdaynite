# Matchday Dashboard Quickstart

1. Configure a test secret/admin credential and an isolated temporary SQLite database.
2. Seed one future non-abandoned game with a location, playing/maybe/not-playing attendance, and paid/unpaid players.
3. Load `/` anonymously and verify the next-match card shows date, location, attendance counts, payment status, and public actions.
4. Load `/` as an administrator and verify attendance, teams, result, leaderboard, and help actions are reachable in at most two interactions.
5. Load `/games/<id>` as an administrator and verify distinct Attendance, Payments, Teams, and Result sections.
6. Verify a game with no attendance shows a clear empty state, and an abandoned game disables or explains unavailable actions.
7. Verify a successful and failed mutation returns clear feedback while preserving the game context.
8. Review `/` and `/games/<id>` at desktop width and 390px width; confirm no horizontal scrolling and usable touch targets.
9. Run the focused dashboard/detail tests, `python -m py_compile app.py`, and `git diff --check`.
