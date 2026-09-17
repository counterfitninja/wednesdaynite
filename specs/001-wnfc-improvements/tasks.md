---
description: "Actionable tasks for Wednesday Night FC improvements"
---

# Tasks: Wednesday Night FC Improvements

**Input**: Design documents from `specs/001-wnfc-improvements/`

**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/matchday-workflow.md`, and `quickstart.md`

**Organization**: Tasks are grouped by user story so each increment can be implemented and validated independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish isolated testing, dependency, and asset foundations.

- [x] T001 [P] Add pytest and test-environment dependencies to `requirements.txt` and document the test command in `README.md`.
- [x] T002 Create an isolated Flask test fixture with a temporary SQLite database and seeded domain helpers in `tests/conftest.py`.
- [x] T003 [P] Create the shared stylesheet entry point and load it from `templates/base.html` via `static/app.css`.
- [x] T004 [P] Record the desktop, mobile, offline, and operational validation scenarios in `specs/001-wnfc-improvements/quickstart.md`.

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish security, persistence, observability, and regression foundations before user stories.

**⚠️ CRITICAL**: Complete this phase before implementing user stories.

- [x] T005 Add safe application configuration, production secret validation, and secret-free structured logging in `app.py`.
- [x] T006 Implement shared-session CSRF generation and validation for HTML forms and same-origin AJAX in `app.py`.
- [x] T007 Configure secure, HTTP-only, SameSite session cookies and same-origin validation for login redirects in `app.py`.
- [x] T008 Protect every state-changing route, including player add/edit, game add, stickers, team generation, imports, payments, and OCR, in `app.py`.
- [x] T009 Add safe 403, 404, and 500 error responses and templates without exposing raw exception or credential data in `app.py` and `templates/error.html`.
- [x] T010 [P] Enable `PRAGMA foreign_keys = ON` for every SQLite connection and document delete/merge behavior in `app.py` and `README.md`.
- [x] T011 [P] Replace homepage and admin-game attendance N+1 queries with grouped aggregate queries in `app.py`.
- [x] T012 Add shared test helpers for authenticated sessions and CSRF tokens in `tests/conftest.py`.

**Checkpoint**: Security, database integrity, diagnostics, and isolated test execution are ready.

## Phase 3: User Story 1 - Safe and Verifiable Administration (Priority: P1) 🎯 MVP

**Goal**: Protect administrative mutations and prove attendance, payment, score, team, import, and abandoned-game rules.

**Independent Test**: Run the US1 tests against isolated SQLite data; anonymous mutations and invalid CSRF requests fail, while valid mutations and calculations preserve documented rules without sensitive log output.

### Tests for User Story 1

- [x] T013 [P] [US1] Add login, logout, protected-route, failed-login, session, and same-origin redirect tests in `tests/test_auth.py`.
- [x] T014 [P] [US1] Add missing, invalid, and valid CSRF tests for forms and AJAX mutations in `tests/test_csrf.py`.
- [ ] T015 [P] [US1] Add attendance, payment, score, abandoned-game, statistics, and foreign-key behavior tests in `tests/test_game_rules.py`.
- [ ] T016 [P] [US1] Add CSV, PayPal, OCR upload validation, and player merge/delete preservation tests in `tests/test_imports.py`.
- [ ] T017 [P] [US1] Assert passwords, secrets, tokens, and unnecessary personal data are absent from diagnostics in `tests/test_observability.py`.

### Implementation for User Story 1

- [ ] T018 [US1] Add CSRF fields to every state-changing form and CSRF headers to AJAX requests in `templates/` and `static/`.
- [ ] T019 [US1] Remove authentication debug prints and replace unsafe exception output with safe diagnostics in `app.py`.
- [ ] T020 [US1] Add upload type, size, and malformed-file validation before OCR or image processing in `app.py` and `services/ocr.py`.
- [ ] T021 [US1] Preserve and document attendance, payment, score, team, import, and abandoned-game calculations in `services/stats.py` and `app.py`.

**Checkpoint**: US1 is independently complete when its security, mutation, calculation, import, and observability tests pass.

## Phase 4: User Story 2 - Matchday Dashboard and Workflow (Priority: P1)

**Goal**: Make the next match and attendance, payment, team, and result actions obvious.

**Independent Test**: Seed upcoming, completed, abandoned, and empty-attendance games; verify `/` and `/games/<id>` render the correct summaries and distinct workflow sections at desktop and 390px widths.

### Tests for User Story 2

- [ ] T022 [P] [US2] Add next-game selection, no-game, abandoned-game, attendance-count, payment-status, and primary-action tests in `tests/test_matchday_dashboard.py`.
- [ ] T023 [P] [US2] Add game-detail tests for separate attendance, payments, teams, result, loading, error, and empty states in `tests/test_game_detail.py`.

### Implementation for User Story 2

- [x] T024 [US2] Add a next-upcoming non-abandoned game summary with grouped attendance and payment aggregates in `app.py`.
- [x] T025 [US2] Render the next-match card, date, location, counts, payment status, and primary actions in `templates/index.html`.
- [ ] T026 [US2] Separate attendance, payments, teams, and result sections while preserving existing route contracts in `templates/game_detail.html`.
- [ ] T027 [US2] Add explicit success, error, loading, and empty-state text to matchday workflows in `templates/base.html`, `templates/game_detail.html`, and `templates/partials/`.
- [x] T028 [US2] Add responsive match summary and primary-action styles in `static/app.css` and `templates/game_detail.html`.

**Checkpoint**: A user can reach and understand the weekly matchday workflow from the home page in at most two interactions.

## Phase 5: User Story 3 - Consistent Responsive and Accessible UI (Priority: P2)

**Goal**: Provide consistent navigation, readable layouts, keyboard access, visible focus, and non-color status communication.

**Independent Test**: Review home, game detail, admin games, leaderboard, and team pages at desktop and 390px widths using keyboard navigation and without relying on color alone.

### Tests for User Story 3

- [ ] T029 [P] [US3] Add rendered-template assertions for Matchday, Stats, and Admin navigation groups and status text in `tests/test_ui_rendering.py`.
- [ ] T030 [P] [US3] Add keyboard, focus, landmark, responsive, and non-color validation scenarios to `specs/001-wnfc-improvements/quickstart.md`.

### Implementation for User Story 3

- [ ] T031 [US3] Regroup shared navigation into Matchday, Stats, and Admin sections with accessible names in `templates/base.html`.
- [ ] T032 [US3] Extract shared styles and add responsive breakpoints, visible focus, contrast-safe status indicators, and table/card rules in `static/app.css`.
- [ ] T033 [P] [US3] Convert key data-heavy views to readable cards or usable responsive tables in `templates/index.html`, `templates/admin_games.html`, and `templates/leaderboard.html`.
- [ ] T034 [P] [US3] Add semantic landmarks, labels, live regions, and keyboard-reachable controls in `templates/base.html`, `templates/game_detail.html`, and `templates/teams_manual.html`.
- [ ] T035 [P] [US3] Add reusable page-header, alert, empty-state, pagination, and badge partials in `templates/partials/` and adopt them in representative pages.

**Checkpoint**: Representative public and admin pages are consistent, responsive, keyboard-usable, and understandable without color alone.

## Phase 6: User Story 4 - Mobile Team and Attendance Management (Priority: P2)

**Goal**: Provide touch-friendly explicit team movement and attendance controls without drag-and-drop or difficult multi-select behavior.

**Independent Test**: At 390px, assign, move, unassign, and optionally swap players; verify saved assignments plus immediate counts, skill totals, and balance difference.

### Tests for User Story 4

- [ ] T036 [P] [US4] Add move, unassign, swap, count, skill-total, and balance-difference tests in `tests/test_team_assignment.py`.
- [ ] T037 [P] [US4] Add mobile attendance control, CSRF, validation, and feedback tests in `tests/test_attendance_ui.py`.

### Implementation for User Story 4

- [ ] T038 [US4] Add authenticated explicit move-to-team, unassign, and optional swap handlers with CSRF validation in `app.py` and `services/teams.py`.
- [ ] T039 [US4] Render touch-friendly player selectors and explicit assignment actions without requiring drag-and-drop in `templates/teams_manual.html`.
- [ ] T040 [US4] Render accessible attendance controls with explicit status labels and preserved unsaved input in `templates/game_detail.html`.
- [ ] T041 [US4] Implement live counts, skill totals, balance difference, request feedback, and retry-safe UI updates in `static/team-assignment.js` and `static/attendance.js`.

**Checkpoint**: Team and attendance management works reliably by touch, mouse, and keyboard.

## Phase 7: User Story 5 - Maintainable Platform and Reliable PWA (Priority: P3)

**Goal**: Add explicit migrations, maintainable boundaries, secure offline synchronization, reliable caches, notifications, backups, and optional OCR deployment.

**Independent Test**: Apply migrations to fresh and legacy databases, run regression tests, inspect module boundaries, and verify service-worker replacement, authenticated cache clearing, offline queue behavior, and notification opt-in.

### Tests for User Story 5

- [ ] T042 [P] [US5] Add fresh-database, legacy-database, repeatability, foreign-key, and delete-semantics tests in `tests/test_migrations.py`.
- [ ] T043 [P] [US5] Add service-worker version cleanup, network-first HTML, authenticated-cache clearing, and offline fallback tests in `tests/test_service_worker.py`.
- [ ] T044 [P] [US5] Add independent offline queue, bounded-backoff retry, conflict warning, rejection, and queue-progress tests in `tests/test_offline_sync.py`.
- [ ] T045 [P] [US5] Add module-boundary and optional-OCR-import smoke tests in `tests/test_platform.py`.

### Implementation for User Story 5

- [ ] T046 [US5] Extract persistence and numbered migrations into `db.py` and `migrations/`, preserving backward-compatible route behavior in `app.py`.
- [ ] T047 [US5] Extract shared authentication and domain services into `auth.py` and `services/` with tests remaining independent of HTTP rendering.
- [ ] T048 [US5] Implement versioned service-worker caches, old-cache cleanup, network-first HTML, authenticated cache partitioning, logout clearing, and offline fallback in `static/service-worker.js`.
- [ ] T049 [US5] Implement independent IndexedDB queue records with `operation_id`, `entity_type`, `entity_id`, `operation_type`, `payload`, `created_at`, `attempt_count`, `next_attempt_at`, `status`, conflict metadata, and safe error fields in `static/attendance.js` and `static/notifications.js`.
- [ ] T050 [US5] Implement latest-successful-update-wins conflict handling, visible administrator warnings, bounded exponential backoff, and independent retry progress in `app.py`, `services/sync.py`, and `static/attendance.js`.
- [ ] T051 [US5] Require explicit notification opt-in and avoid repeated prompts when disabled or permission is absent in `static/notifications.js` and `templates/base.html`.
- [ ] T052 [US5] Separate OCR dependencies into `requirements-ocr.txt`, avoid ordinary-startup OCR imports in `services/ocr.py`, and document installation profiles in `README.md`.
- [ ] T053 [US5] Add backup/export and restore-verification procedures in `app.py`, `templates/`, `README.md`, and `RELEASE_CHECKLIST.md`.

**Checkpoint**: Migrations, module boundaries, PWA behavior, synchronization, notifications, backups, and deployment guidance are independently verifiable.

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Validate the complete increment and update documentation.

- [ ] T054 [P] Run `python -m py_compile app.py` and compile all changed Python files.
- [ ] T055 [P] Run focused story tests and the full pytest suite from `tests/`.
- [ ] T056 [P] Validate desktop and mobile workflows, including empty, error, loading, offline, conflict, and retry states, using `specs/001-wnfc-improvements/quickstart.md`.
- [ ] T057 [P] Run `git diff --check` and review security, accessibility, data-integrity, and maintainability compliance against `.specify/memory/constitution.md`.
- [ ] T058 Update user-facing behavior and operational documentation in `README.md`, `HOW_IT_WORKS.md`, `CHANGELOG.md`, and `RELEASE_CHECKLIST.md`.

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 has no dependencies.
- Phase 2 depends on Phase 1 and blocks all user stories.
- US1 and US2 depend on Phase 2; both are P1 and form the recommended MVP.
- US3 and US4 depend on Phase 2; US4 may reuse US2/US3 UI patterns.
- US5 depends on regression coverage from US1–US4 before broad extraction and PWA changes.
- Polish depends on the stories selected for release.

### User Story Dependencies

- US1: Phase 2 only; independently testable.
- US2: Phase 2 only; uses secured routes and grouped query foundations.
- US3: Phase 2 only; may share stylesheet and templates with US2.
- US4: Phase 2 only; shares game/team domain behavior but has independent tests.
- US5: Best completed after US1–US4 behavior is covered, especially migrations and refactoring.

### Parallel Execution Examples

- After T001–T002: T003 and T004 can run in parallel.
- After Phase 2 security interfaces are agreed: T013–T017 can run in parallel.
- Within US2: T022 and T023 can run in parallel.
- Within US3: T029–T030 can run in parallel; T033–T035 can run in parallel after shared navigation/style decisions.
- Within US4: T036 and T037 can run in parallel.
- Within US5: T042–T045 can run in parallel; implementation tasks then proceed from migrations and service boundaries to PWA synchronization.
- Final validation T054–T057 can run in parallel; T058 follows the validated results.

## Implementation Strategy

### MVP First

1. Complete Phase 1 Setup.
2. Complete Phase 2 Foundational.
3. Complete US1 Safe and Verifiable Administration.
4. Complete US2 Matchday Dashboard and Workflow.
5. Validate the weekly matchday workflow independently before expanding scope.

### Incremental Delivery

1. Deliver security, persistence, and regression foundations.
2. Deliver the dashboard and game-detail workflow.
3. Deliver responsive and accessible UI improvements.
4. Deliver touch-friendly team and attendance management.
5. Deliver maintainability, migrations, PWA synchronization, and deployment improvements.
6. Run cross-cutting validation and update documentation.

## Notes

- All tasks use `- [ ] T###` checklist syntax.
- `[P]` marks only tasks that can run in parallel without incomplete dependencies.
- User-story tasks include exactly one `[US#]` label.
- Every task includes at least one concrete file path.
- Tests are included because the specification and constitution require focused regression coverage.
