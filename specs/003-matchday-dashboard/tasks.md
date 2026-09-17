---

description: "Actionable tasks for Matchday Dashboard and Workflow"
---

# Tasks: Matchday Dashboard and Workflow

**Input**: Design documents from `/specs/003-matchday-dashboard/`

**Prerequisites**: `spec.md`, `plan.md`, `data-model.md`, `contracts/`, `research.md`, and project constitution

**Tests**: Included because the feature specification requires focused rendering, workflow, and regression coverage.

**Organization**: Tasks are grouped by the single user story so the increment can be implemented and validated independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the test and asset foundations needed for the dashboard without changing behavior.

- [ ] T001 Create isolated Flask test-client fixtures and temporary SQLite seed helpers in tests/conftest.py
- [ ] T002 [P] Add dashboard/detail quickstart scenarios and viewport validation notes in specs/003-matchday-dashboard/quickstart.md
- [ ] T003 [P] Add shared stylesheet entry/loading support for matchday UI in static/app.css and templates/base.html

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared query, feedback, and security integration prerequisites before story implementation.

**⚠️ CRITICAL**: Complete this phase before User Story 1 work.

- [ ] T004 Add a bounded next-game and grouped attendance/payment summary helper in app.py, preserving non-abandoned and payment-exempt business rules
- [ ] T005 [P] Add shared flash-message/feedback rendering and safe empty-state hooks in templates/base.html
- [ ] T006 [P] Verify dashboard state-changing links/forms use the authentication and CSRF foundation from specs/002-safe-admin/ in app.py, templates/, and tests/test_matchday_security.py

**Checkpoint**: Summary data, feedback presentation, and security integration are ready for the matchday increment.

---

## Phase 3: User Story 1 - Matchday Dashboard and Workflow (Priority: P1) 🎯 MVP

**Goal**: Make the next match and its attendance, payment, team, result, leaderboard, and help actions obvious on desktop and mobile.

**Independent Test**: Seed an upcoming non-abandoned game with attendance and payment records, load `/` and `/games/<id>` through the Flask test client, and verify the summary, counts, actions, separated sections, feedback, and 390px-safe markup without changing existing game rules.

### Tests for User Story 1

- [ ] T007 [P] [US1] Add home-page tests for next-game selection, date/location, attendance counts, payment counts, role-aware quick actions, empty state, and abandoned-game handling in tests/test_matchday_dashboard.py
- [ ] T008 [P] [US1] Add grouped-query/query-count regression tests proving dashboard summary data avoids per-player N+1 queries in tests/test_matchday_dashboard.py
- [ ] T009 [P] [US1] Add game-detail rendering tests for Attendance, Payments, Teams, Result sections, action hierarchy, feedback, empty data, and abandoned state in tests/test_game_detail.py
- [ ] T010 [P] [US1] Add regression assertions for existing attendance, payment-exemption, team, score, and abandoned-game behavior in tests/test_matchday_workflows.py

### Implementation for User Story 1

- [ ] T011 [US1] Update the home route to select the nearest actionable upcoming game and expose one bounded summary view model in app.py
- [ ] T012 [US1] Redesign the primary home-page card with next-match date, location, attendance/payment status, and role-aware quick actions in templates/index.html
- [ ] T013 [US1] Add clear no-upcoming-game, no-attendance, and abandoned-match states with safe next actions in templates/index.html
- [ ] T014 [US1] Restructure game details into clearly identified Attendance, Payments, Teams, and Result sections while reusing existing routes and rules in templates/game_detail.html
- [ ] T015 [US1] Add a sticky or readily available mobile match summary and primary action area with long-content-safe responsive layout in templates/game_detail.html and static/app.css
- [ ] T016 [US1] Add accessible success, error, empty, abandoned, and pending/loading feedback for matchday workflows in templates/base.html, templates/index.html, templates/game_detail.html, and static/app.css
- [ ] T017 [US1] Ensure home and game-detail actions preserve authentication/CSRF behavior and do not expose admin mutations to anonymous users in app.py, templates/index.html, and templates/game_detail.html

**Checkpoint**: A player or administrator can reach the next-match workflow from the home page in at most two interactions, and the game page makes attendance, payments, teams, and result actions clear on mobile.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validate the independently deliverable dashboard increment and update documentation.

- [ ] T018 [P] Run focused dashboard, detail, and workflow regression tests from tests/test_matchday_dashboard.py, tests/test_game_detail.py, and tests/test_matchday_workflows.py
- [ ] T019 [P] Run python -m py_compile app.py and editor diagnostics for changed Python files
- [ ] T020 [P] Run git diff --check and review query bounds, security/CSRF integration, accessibility, and constitution compliance
- [ ] T021 [P] Validate / and /games/<id> at desktop and 390px widths, including empty, abandoned, success, and error states, using specs/003-matchday-dashboard/quickstart.md
- [ ] T022 Update README.md, HOW_IT_WORKS.md, and CHANGELOG.md with the matchday dashboard workflow and any changed user-facing actions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies; establish fixtures, quickstart, and asset entry points.
- **Phase 2 Foundational**: Depends on Phase 1 and blocks User Story 1.
- **User Story 1**: Depends on Phase 2; all story tests and implementation deliver the complete P1 increment.
- **Polish**: Depends on User Story 1; validation tasks may run in parallel after implementation.

### User Story Dependencies

- **US1 (P1)**: Depends only on the foundational summary, feedback, and security integration work. It reuses existing game, attendance, payment, team, result, leaderboard, and help routes rather than depending on later responsive/navigation stories.

### Parallel Opportunities

- Phase 1 tasks T002–T003 can run in parallel after T001.
- Phase 2 tasks T005–T006 can run in parallel with each other after T004's summary contract is agreed.
- US1 tests T007–T010 can run in parallel because they target separate test modules/concerns.
- US1 implementation tasks T012–T013 can run in parallel after T011's view-model contract; T014–T016 can proceed in parallel once the section/feedback markup contract is agreed.
- Final validation tasks T018–T021 can run in parallel after story implementation.

## Parallel Example: User Story 1

```text
Task: "Add home-page next-game and aggregate-count tests in tests/test_matchday_dashboard.py"
Task: "Add game-detail workflow rendering tests in tests/test_game_detail.py"
Task: "Add existing attendance/payment/team/score regression tests in tests/test_matchday_workflows.py"

After the view-model contract is stable:
Task: "Redesign templates/index.html with the next-match card and quick actions"
Task: "Restructure templates/game_detail.html into Attendance, Payments, Teams, and Result sections"
Task: "Add mobile and feedback styling in static/app.css and shared templates"
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 Setup.
2. Complete Phase 2 Foundational.
3. Complete User Story 1.
4. **STOP and VALIDATE**: run focused tests and review `/` plus `/games/<id>` at 390px width.
5. Deploy/demo only after security, query, and workflow quality gates pass.

### Incremental Delivery

1. Establish fixtures and the bounded summary contract.
2. Deliver the next-match dashboard card and quick actions.
3. Deliver separated game-detail workflow sections.
4. Deliver mobile summary, feedback, and empty/abandoned states.
5. Run cross-cutting validation and documentation updates.

## Notes

- Every task uses the required `- [ ] T###` checklist format.
- `[P]` marks tasks that can run in parallel without conflicting incomplete dependencies.
- `[US1]` maps story tasks to the source User Story 2 increment; this feature contains one local user story, so its phase label is `[US1]`.
- Tests are included because the specification explicitly requires focused automated coverage.
