# Implementation Plan: Consistent Responsive and Accessible UI

## Technical Context

- Existing application: Flask server-rendered web application in `app.py`.
- Persistence and route behavior remain unchanged; this increment is presentation-focused.
- UI: Jinja templates under `templates/`; shared styles move into `static/app.css`.
- Client assets: use small progressive-enhancement JavaScript only for mobile navigation or other interactions that remain usable without JavaScript.
- Testing: pytest-compatible Flask test client for rendered markup and route visibility, plus browser review at desktop and 390px widths.
- Security: preserve authentication and CSRF behavior from `specs/002-safe-admin/`.

## Project Structure

- `app.py`: only add shared navigation context or accessibility-related data when existing route context cannot provide it.
- `templates/base.html`: shared landmarks, grouped navigation, mobile navigation controls, flash/feedback semantics, and asset loading.
- `templates/index.html`: responsive home-page content and status markup.
- `templates/game_detail.html`: responsive workflow content and accessible status/action markup.
- `templates/admin_games.html`: mobile-first game list and action presentation.
- `templates/leaderboard.html`: responsive leaderboard and non-color status indicators.
- `templates/teams_manual.html`: responsive team layout and explicit status labels.
- `templates/partials/`: reusable page-header, alert, empty-state, pagination, and badge components.
- `static/app.css`: shared design tokens, layout, controls, responsive rules, visible focus, and non-color status styles.
- `static/navigation.js`: optional progressive enhancement for mobile navigation; preserve no-JavaScript access.
- `tests/test_ui_rendering.py`: route/template assertions for navigation groups, landmarks, status labels, and feedback semantics.
- `specs/004-responsive-accessible-ui/quickstart.md`: manual desktop, mobile, keyboard, and non-color validation.

## Design Decisions

1. Keep route destinations and domain behavior unchanged; solve consistency at shared template and CSS layers first.
2. Use semantic HTML landmarks (`header`, `nav`, `main`, `footer`) and native buttons/links before adding JavaScript behavior.
3. Use a mobile menu button with an accessible name and state; when JavaScript is unavailable, retain a usable navigation fallback.
4. Use text labels, icons with accessible names, table/card structure, and badges to communicate states in addition to color.
5. Use responsive tables only where columns remain readable; otherwise render a card/list representation that preserves headings and values.
6. Keep helper text concise and place it below controls when a setting or action is not self-explanatory.

## Delivery Strategy

1. Add failing rendering/accessibility assertions and manual validation scenarios.
2. Establish shared CSS tokens, landmarks, feedback semantics, and reusable partials.
3. Group navigation and add progressive mobile navigation.
4. Convert representative data-heavy views to responsive layouts.
5. Add visible focus, keyboard behavior, and non-color status communication.
6. Run focused tests, syntax checks, `git diff --check`, and desktop/mobile review.

## Quality Gates

- Rendering tests verify navigation groups, role visibility, landmarks, feedback, and status text.
- Representative pages remain usable at desktop and 390px widths without layout-critical horizontal scrolling.
- Keyboard-only review reaches primary actions with visible focus.
- Status meanings remain understandable without color.
- Authentication, CSRF, and domain behavior are unchanged.
- `python -m py_compile app.py` and `git diff --check` pass.
