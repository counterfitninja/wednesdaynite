# Implementation Plan: Matchday Dashboard and Workflow

## Technical Context

- Existing application: Flask server-rendered web application in `app.py`.
- Persistence: SQLite database in `football.db`; use existing schema and query helpers.
- UI: Jinja templates under `templates/`; shared styles currently in `templates/base.html` and page-local styles.
- Client assets: add focused matchday styles to `static/app.css`; use small JavaScript only where it improves feedback without becoming required for navigation.
- Testing: pytest-compatible Flask test client with isolated temporary SQLite databases; render assertions and query-count checks.
- Security: state-changing forms and endpoints depend on the authentication/CSRF foundation in `specs/002-safe-admin/`.

## Project Structure

- `app.py`: next-game selection, grouped attendance/payment summary data, flash feedback, and game-detail route context.
- `templates/index.html`: matchday dashboard and next-match card.
- `templates/game_detail.html`: separated workflow sections and mobile summary/action area.
- `templates/base.html`: shared flash/feedback rendering and asset loading.
- `static/app.css`: shared matchday card, action, responsive, and feedback styles.
- `tests/test_matchday_dashboard.py`: home-page summary, role-aware actions, empty/abandoned states, and query behavior.
- `tests/test_game_detail.py`: separated sections, action links, feedback, and mobile-oriented markup assertions.
- `specs/003-matchday-dashboard/quickstart.md`: manual desktop/mobile validation scenarios.

## Data and Route Decisions

1. Select the nearest game with `date >= date('now')`, preferring non-abandoned games; if all future games are abandoned, show a safe empty/exception state rather than misleadingly presenting an abandoned match as actionable.
2. Load the dashboard page using one game query and one grouped attendance/payment aggregate query for the primary card; preserve existing pagination behavior for the games list.
3. Reuse existing game routes for attendance, teams, score/result, leaderboard, and help. Role-aware links must not expose admin mutation controls to anonymous users.
4. Use Flask flash messages or the existing feedback mechanism for mutation results, rendered consistently in `base.html`.
5. Preserve existing business rules for attendance, payment exemptions, team generation, scores, and abandoned games.

## Delivery Strategy

1. Add focused failing render/query tests and fixtures.
2. Add bounded dashboard summary data and next-game selection.
3. Implement the home-page matchday card and role-aware quick actions.
4. Split game details into Attendance, Payments, Teams, and Result sections.
5. Add mobile summary/action styling and feedback/empty states.
6. Run focused tests, syntax checks, query-count checks, and desktop/mobile review.

## Quality Gates

- Dashboard tests pass with an upcoming game, no upcoming game, abandoned game, no attendance, and payment-exempt players.
- Game-detail tests find explicit Attendance, Payments, Teams, and Result sections and role-appropriate actions.
- Summary queries are bounded and do not regress into per-player N+1 queries.
- `python -m py_compile app.py` passes.
- `git diff --check` passes.
- Primary pages are usable at desktop and 390px mobile widths, including empty, abandoned, success, and error states.
- Existing attendance/payment/team/result behavior remains covered by regression tests.
