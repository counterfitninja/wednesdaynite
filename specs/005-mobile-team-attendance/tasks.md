---

description: "Actionable tasks for Mobile Team and Attendance Management"
---

# Tasks: Mobile Team and Attendance Management

**Input**: Design documents from `/specs/005-mobile-team-attendance/`

**Prerequisites**: `spec.md`, `plan.md`, `data-model.md`, `contracts/`, `quickstart.md`, and existing security protections from `specs/002-safe-admin/`

**Tests**: Included because the feature specification explicitly requires focused regression coverage.

**Organization**: Tasks are grouped by the single local user story, which is User Story 4 from `specs/001-wnfc-improvements/spec.md`.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish focused fixtures and client-asset entry points without changing domain behavior.

- [ ] T001 Create isolated Flask game, player, attendance, and team-assignment fixtures in `tests/conftest.py`
- [ ] T002 [P] Add mobile, no-JavaScript, keyboard, and recovery scenarios in `specs/005-mobile-team-attendance/quickstart.md`
- [ ] T003 [P] Add assignment and attendance asset loading entry points in `templates/base.html`, `templates/teams_manual.html`, and `templates/game_detail.html`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish persistence invariants, shared mobile styles, and transaction/test helpers required by the user story.

**⚠️ CRITICAL**: Complete this phase before User Story 1 implementation.

- [ ] T004 Add transaction and database-count helpers for asserting zero partial writes in `tests/conftest.py` and `tests/helpers.py`
- [ ] T005 [P] Define mobile card, touch-target, focus, status, and balance-summary styles in `static/app.css`
- [ ] T006 [P] Document and enforce the `team_assignments` uniqueness and `team_number` invariants in `app.py` and `specs/005-mobile-team-attendance/data-model.md`
- [ ] T007 Verify authentication, CSRF, abandoned-game, and existing skill-default rules are reused by team and attendance mutations in `app.py` and `tests/test_team_assignment.py`

**Checkpoint**: Fixtures, persistence invariants, shared mobile styles, and security/domain guardrails are ready.

---

## Phase 3: User Story 1 - Mobile Team and Attendance Management (Priority: P2) 🎯 MVP

**Goal**: Make team assignment and attendance editing touch-friendly, explicit, transactional, and independently verifiable at a 390px viewport.

**Independent Test**: At 390px, assign, move, unassign, and swap players without drag-and-drop; save and reload; verify assignment uniqueness, counts, skill totals, balance difference, attendance states, and accessible feedback. Repeat with JavaScript disabled.

### Tests for User Story 1

- [ ] T008 [P] [US1] Add explicit move, unassign, save, duplicate, invalid-player, and abandoned-game tests in `tests/test_team_assignment.py`
- [ ] T009 [P] [US1] Add valid and invalid swap tests, including distinct players on different teams and zero partial writes, in `tests/test_team_assignment.py`
- [ ] T010 [P] [US1] Add team count, effective skill total, balance difference, and reload-persistence assertions in `tests/test_team_assignment.py`
- [ ] T011 [P] [US1] Add attendance control rendering and persistence tests for Playing, Maybe, and Not Playing in `tests/test_attendance_ui.py`
- [ ] T012 [P] [US1] Add 390px markup, touch-target, accessible-label, feedback, and JavaScript-disabled fallback assertions in `tests/test_attendance_ui.py`

### Implementation for User Story 1

- [ ] T013 [US1] Implement transactional validation and replacement persistence for `team1_players` and `team2_players` in `app.py`
- [ ] T014 [US1] Add explicit move-to-team and unassign request handling with zero-partial-write failures in `app.py`
- [ ] T015 [US1] Add validated explicit swap handling for two distinct players assigned to different teams in `app.py`
- [ ] T016 [US1] Render Team 1, Team 2, and Unassigned player groups with explicit native move, unassign, and swap controls in `templates/teams_manual.html`
- [ ] T017 [US1] Render server-authoritative player counts, effective skill totals, and absolute balance difference in `templates/teams_manual.html`
- [ ] T018 [US1] Add optional client-side draft movement, swap state, live totals, balance difference, and resilient save feedback in `static/team-assignment.js`
- [ ] T019 [US1] Replace or supplement attendance multi-select interactions with explicit touch-friendly Playing, Maybe, and Not Playing controls in `templates/game_detail.html`
- [ ] T020 [US1] Add optional attendance count/status feedback while preserving native form submission in `static/attendance.js` and `templates/game_detail.html`
- [ ] T021 [US1] Add accessible labels, live feedback, focus states, no-color status text, and 390px overflow protection in `static/app.css`, `templates/teams_manual.html`, and `templates/game_detail.html`

**Checkpoint**: US1 is independently complete when focused tests pass, the workflow works at 390px without drag-and-drop, and JavaScript-disabled forms remain usable.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validate security, domain preservation, mobile usability, and documentation.

- [ ] T022 [P] Run focused assignment and attendance tests plus the existing regression suite from `tests/test_team_assignment.py`, `tests/test_attendance_ui.py`, and `tests/`
- [ ] T023 [P] Run `python -m py_compile app.py` and editor diagnostics for changed Python files
- [ ] T024 [P] Run `git diff --check` and review authentication, CSRF, abandoned-game, payment, and historical-assignment behavior against `specs/002-safe-admin/` and `specs/005-mobile-team-attendance/spec.md`
- [ ] T025 [P] Validate touch, keyboard, no-JavaScript, empty, error, and recovery workflows at 390px using `specs/005-mobile-team-attendance/quickstart.md`
- [ ] T026 Update `README.md`, `HOW_IT_WORKS.md`, and `CHANGELOG.md` with explicit mobile assignment and attendance behavior in `README.md`, `HOW_IT_WORKS.md`, and `CHANGELOG.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies; establish fixtures, quickstart, and asset entry points.
- **Phase 2 Foundational**: Depends on Phase 1 and blocks User Story 1.
- **User Story 1**: Depends on Phase 2; tests and implementation deliver the complete mobile workflow.
- **Polish**: Depends on User Story 1; validation tasks may run in parallel after implementation.

### User Story Dependencies

- **US1 (P2)**: Depends on existing game/team/attendance routes and security protections, but is independently testable and maps to User Story 4 from `specs/001-wnfc-improvements/spec.md`.

### Parallel Opportunities

- T002–T003 can run in parallel after T001.
- T005–T007 can run in parallel after the persistence and markup contracts are agreed.
- T008–T012 can run in parallel because they cover separate focused test concerns; coordinate edits if implemented concurrently.
- T016–T017 and T019–T021 can be developed in parallel after the route/form contract is stable.
- T022–T025 can run in parallel after implementation is complete.

## Parallel Example: User Story 1

```text
Task: "Add move, unassign, duplicate, and abandoned-game tests in tests/test_team_assignment.py"
Task: "Add swap and zero-partial-write tests in tests/test_team_assignment.py"
Task: "Add balance and reload-persistence tests in tests/test_team_assignment.py"
Task: "Add attendance rendering and persistence tests in tests/test_attendance_ui.py"

After the route/form contract is stable:
Task: "Implement explicit assignment controls in templates/teams_manual.html"
Task: "Implement touch-friendly attendance controls in templates/game_detail.html"
Task: "Implement optional live draft totals in static/team-assignment.js"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 Setup.
2. Complete Phase 2 Foundational.
3. Complete Phase 3 User Story 1.
4. **STOP and VALIDATE**: run focused tests, reload saved assignments, review 390px touch/keyboard behavior, and repeat with JavaScript disabled.
5. Complete Phase 4 polish and documentation.

### Incremental Delivery

1. Establish fixtures, invariants, and mobile style primitives.
2. Deliver transactional assignment save, move, unassign, and swap operations.
3. Deliver explicit team controls and live balance feedback.
4. Deliver explicit attendance controls and count feedback.
5. Run security, regression, mobile, no-JavaScript, and documentation validation.

## Notes

- Every task follows the required `- [ ] T### [P?] [US1?] Description with exact file path` checklist format.
- `[P]` marks tasks that can be performed in parallel without conflicting incomplete dependencies.
- `[US1]` maps this feature's local story to User Story 4 from the parent specification.
- The local story is numbered US1 because this feature isolates one parent story; the mapping is stated explicitly above.