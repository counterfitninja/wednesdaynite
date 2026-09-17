# Implementation Plan: Mobile Team and Attendance Management

## Technical Context

- Existing application: Flask server-rendered web application in `app.py`.
- Persistence: SQLite tables for `games`, `players`, `attendance`, and `team_assignments`.
- UI: Jinja templates under `templates/`, with shared styles in `static/app.css`.
- Client assets: progressive-enhancement JavaScript under `static/`.
- Testing: pytest-compatible Flask test client with an isolated SQLite database; browser review at 390px.
- Security: preserve authentication and CSRF protections from `specs/002-safe-admin/`.

## Project Structure

- `app.py`: validate and persist explicit team moves/swaps and attendance mutations transactionally.
- `templates/teams_manual.html`: server-rendered team lists, explicit destination controls, swap controls, and balance summary.
- `templates/game_detail.html`: touch-friendly attendance controls and accessible workflow feedback.
- `static/team-assignment.js`: optional live draft updates, totals, swap affordance, and progressive enhancement.
- `static/attendance.js`: optional attendance control feedback and count updates; native forms remain the fallback.
- `static/app.css`: mobile layout, touch target, focus, status, and balance-summary styles.
- `tests/test_team_assignment.py`: move, unassign, swap, validation, persistence, and balance tests.
- `tests/test_attendance_ui.py`: attendance rendering, persistence, counts, accessibility, and no-JavaScript fallback tests.
- `specs/005-mobile-team-attendance/data-model.md`: persistence invariants and validation rules.
- `specs/005-mobile-team-attendance/contracts/mobile-team-attendance.md`: route/form contract.
- `specs/005-mobile-team-attendance/quickstart.md`: focused automated and manual validation.

## Design Decisions

1. Use explicit native buttons/forms for assignment and attendance; JavaScript only improves draft feedback and never becomes a requirement.
2. Treat unassigned as absence of a `team_assignments` row, preserving the existing schema and historical data model.
3. Validate the complete submitted assignment set before writing and use one transaction so duplicate or invalid input cannot create partial state.
4. Keep swap explicit and opt-in; a swap must identify two distinct assigned players and their current teams.
5. Render balance totals from server data and recalculate them client-side after draft changes; the server remains authoritative on save.
6. Use readable labels such as “Team 1”, “Team 2”, “Unassigned”, “Playing”, “Maybe”, and “Not Playing” in addition to color or icons.

## Delivery Strategy

1. Add data-model invariants, route/form contract, and failing focused tests.
2. Implement transactional explicit assignment operations and server-rendered controls.
3. Add optional live draft totals and swap feedback.
4. Replace or supplement attendance multi-select controls with explicit touch-friendly controls.
5. Validate mobile, keyboard, no-JavaScript, security, and regression behavior.

## Quality Gates

- Focused assignment and attendance tests pass with an isolated database.
- Invalid, unauthorized, CSRF-invalid, and abandoned mutations create no partial writes.
- Team totals and balance difference match server calculations after reload.
- Primary controls are usable at 390px and with keyboard navigation.
- JavaScript-disabled server-rendered forms still complete the workflows.
- `python -m py_compile app.py` and `git diff --check` pass.