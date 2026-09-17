# Quickstart: Mobile Team and Attendance Management

## Automated checks

1. Run `pytest tests/test_team_assignment.py tests/test_attendance_ui.py`.
2. Verify a move to Team 1, move to Team 2, and unassign each persist after reload.
3. Verify a valid swap exchanges team numbers and invalid swaps perform no writes.
4. Verify duplicate, overlapping, invalid-player, CSRF-invalid, unauthorized, and abandoned-game requests perform no partial writes.
5. Verify team counts, skill totals, and absolute balance difference match server calculations.
6. Verify Playing, Maybe, and Not Playing controls render and persist.

## Mobile review at 390px

1. Seed a game with at least four eligible players and mixed skill ratings.
2. Open `/games/<id>/teams/manual` at a 390px viewport.
3. Assign an unassigned player to Team 1 using the explicit control; repeat for Team 2.
4. Move a player to the other team, then unassign a player; confirm the visible counts and totals change immediately.
5. Use the explicit swap control for players on opposite teams and verify the proposed/current result is clear.
6. Save, reload, and confirm no duplicate membership or stale totals are shown.
7. Open the game detail page and set players to Playing, Maybe, and Not Playing using touch-friendly controls.
8. Confirm attendance counts, payment summaries, labels, focus, and feedback remain readable without horizontal scrolling.

## No-JavaScript and regression review

1. Disable JavaScript and complete a server-rendered team save and attendance update.
2. Confirm authentication and CSRF protections remain active.
3. Run `python -m py_compile app.py`.
4. Run the existing regression suite.
5. Run `git diff --check`.