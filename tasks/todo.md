# Wednesday Night FC Improvement Backlog

Prioritized backlog based on the codebase and UI review. Work from top to bottom unless a task is intentionally deferred.

## Phase 1 — Safety and foundations

- [ ] Remove password-related debug logging from the login flow.
- [ ] Add CSRF protection to all state-changing forms and POST routes.
- [ ] Configure secure session cookies and validate the login `next` URL.
- [ ] Replace `print()` diagnostics with structured application logging.
- [ ] Add basic error pages for 403, 404, and 500 responses.
- [ ] Add focused automated tests for authentication, attendance, scores, payments, teams, imports, and abandoned games.
- [ ] Replace homepage/admin game-list N+1 attendance queries with grouped aggregate queries.

## Phase 2 — Matchday experience

- [ ] Redesign the home page as a matchday dashboard centered on the next game.
- [ ] Add next-match details, attendance counts, payment status, and primary matchday actions.
- [ ] Add quick actions for attendance, teams, final score, leaderboard, and help.
- [ ] Restructure the game detail page into clear Attendance, Payments, Teams, and Result sections.
- [ ] Add a sticky mobile match summary and action bar to the game detail page.
- [ ] Add clear success, error, loading, and empty-state feedback to admin workflows.

## Phase 3 — Navigation and responsive UI

- [ ] Simplify the main navigation into Matchday, Stats, and Admin groups.
- [ ] Rename or fix confusing navigation labels, especially the visible `Teams` link.
- [ ] Add a mobile-friendly navigation pattern for Home, Games, Stats, and Admin.
- [ ] Replace key mobile tables with responsive cards where appropriate.
- [ ] Improve the admin games view for mobile-first scanning and actions.
- [ ] Add visible focus states, semantic landmarks, keyboard support, and accessible form errors.
- [ ] Ensure status and team colors are not the only way information is communicated.

## Phase 4 — Shared visual system

- [ ] Move repeated inline styles from templates into `static/app.css`.
- [ ] Define shared color, spacing, typography, button, badge, card, table, and form styles.
- [ ] Create reusable template partials for page headers, alerts, pagination, empty states, and status badges.
- [ ] Standardize button hierarchy and terminology across public and admin pages.
- [ ] Add concise helper text below settings and controls where behavior is not obvious.

## Phase 5 — Team and attendance workflows

- [ ] Make manual team assignment usable without drag and drop on mobile.
- [ ] Add explicit move-to-team, unassign, and optional swap controls.
- [ ] Show live team player counts, skill totals, and balance difference.
- [ ] Add attendance editing controls that are easier to use than large multi-select lists.
- [ ] Add undo or safer recovery for destructive player/game actions.

## Phase 6 — Backend maintainability

- [ ] Split `app.py` into blueprints, database helpers, route modules, and service modules.
- [ ] Extract team balancing, statistics, OCR, payment, and image-processing logic into services.
- [ ] Introduce a lightweight versioned migration system instead of growing `init_db()` conditionals.
- [ ] Enable SQLite foreign keys and review cascade/delete behavior.
- [ ] Add an application factory and test database configuration.
- [ ] Add request and database timing instrumentation for slow pages.

## Phase 7 — PWA, notifications, and deployment

- [ ] Replace browser-only timer reminders with reliable scheduled or Web Push notifications.
- [ ] Request notification permission only after an explicit user action.
- [ ] Improve service-worker cache versioning, activation cleanup, and offline fallback behavior.
- [x] Remove server-side OCR and heavyweight OCR model dependencies; keep image extraction browser-only with text fallback.
- [ ] Add an admin backup/export workflow and document restore verification.

## Review checklist

- [ ] Run focused regression tests after each feature group.
- [ ] Test desktop and mobile layouts at representative widths.
- [ ] Run `python -m py_compile app.py` and editor diagnostics.
- [ ] Run `git diff --check`.
- [ ] Update `README.md`, `HOW_IT_WORKS.md`, and `CHANGELOG.md` when behavior changes.

## Completed work archive

- Admin games unpaid count.
- Sticker packet feature.
- Season momentum statistic.
- Leaderboard form guide for the last five games.