---

description: "Actionable tasks for Consistent Responsive and Accessible UI"
---

# Tasks: Consistent Responsive and Accessible UI

**Input**: Design documents from `/specs/004-responsive-accessible-ui/`

**Prerequisites**: `spec.md`, `plan.md`, `quickstart.md`, and `.specify/memory/constitution.md`

**Tests**: Included because the feature specification requires focused rendering and accessibility coverage.

**Organization**: Tasks are grouped by the single local user story, which is User Story 3 from `specs/001-wnfc-improvements/spec.md`.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish shared UI, test, and validation foundations without changing domain behavior.

- [ ] T001 Create isolated Flask rendering fixtures and representative route helpers in tests/conftest.py
- [ ] T002 [P] Add desktop, 390px mobile, keyboard, and non-color validation scenarios in specs/004-responsive-accessible-ui/quickstart.md
- [ ] T003 [P] Create the shared stylesheet entry point and asset loading contract in static/app.css and templates/base.html

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared markup, styling, and feedback primitives required by all responsive/accessibility changes.

**⚠️ CRITICAL**: Complete this phase before User Story 1 implementation.

- [ ] T004 Add semantic page landmarks and a stable skip-to-content target in templates/base.html
- [ ] T005 [P] Define shared CSS tokens, typography, spacing, buttons, badges, cards, responsive containers, and visible focus styles in static/app.css
- [ ] T006 [P] Create reusable page-header, alert, empty-state, pagination, and status-badge partials in templates/partials/
- [ ] T007 [P] Add accessible flash/status semantics with appropriate live-region behavior in templates/base.html and templates/partials/alert.html
- [ ] T008 Verify existing authentication, CSRF, and role checks remain the source of truth for navigation visibility in app.py, templates/base.html, and tests/test_ui_rendering.py

**Checkpoint**: Shared landmarks, styling primitives, feedback semantics, and security integration are ready.

---

## Phase 3: User Story 1 - Consistent Responsive and Accessible UI (Priority: P2) 🎯 MVP

**Goal**: Make representative public, admin, stats, and team pages consistent, responsive, keyboard-usable, and understandable without relying on color alone.

**Independent Test**: Review `/`, `/games/<id>`, `/admin/games`, `/leaderboard`, and `/teams/manual` at desktop and 390px widths; use keyboard navigation and inspect status meaning without color. Run the focused rendering tests against an isolated database.

### Tests for User Story 1

- [ ] T009 [P] [US1] Add rendering tests for Matchday, Stats, and Admin navigation groups, landmarks, skip link, and role-appropriate links in tests/test_ui_rendering.py
- [ ] T010 [P] [US1] Add responsive markup assertions for home, game detail, admin games, leaderboard, and manual teams pages in tests/test_ui_rendering.py
- [ ] T011 [P] [US1] Add accessibility assertions for visible focus hooks, semantic controls, labels, feedback associations, and non-color status text in tests/test_ui_rendering.py

### Implementation for User Story 1

- [ ] T012 [US1] Regroup shared navigation into Matchday, Stats, and Admin sections while preserving existing route destinations and role visibility in templates/base.html
- [ ] T013 [US1] Add a progressive mobile navigation control for Home, Games, Stats, and Admin with accessible name/state and no-hover access in templates/base.html and static/navigation.js
- [ ] T014 [P] [US1] Move repeated inline visual rules into shared responsive card, table, form, button, badge, and page-header styles in static/app.css and templates/index.html
- [ ] T015 [P] [US1] Convert the admin games and leaderboard layouts to readable mobile cards or explicitly usable responsive tables in templates/admin_games.html and templates/leaderboard.html
- [ ] T016 [P] [US1] Make home and game-detail summary/action layouts wrap safely at 390px and preserve readable long labels in templates/index.html and templates/game_detail.html
- [ ] T017 [P] [US1] Make manual team layout responsive and expose team/status meanings through text or semantic labels in templates/teams_manual.html
- [ ] T018 [US1] Add visible focus, keyboard-order, reduced-motion, overflow, and non-color status styles in static/app.css
- [ ] T019 [US1] Apply reusable page headers, alerts, empty states, pagination, and status badges to representative pages in templates/index.html, templates/game_detail.html, templates/admin_games.html, templates/leaderboard.html, templates/teams_manual.html, and templates/partials/
- [ ] T020 [US1] Associate form errors and status messages with relevant controls/content without changing mutation behavior in templates/base.html, templates/game_detail.html, templates/admin_games.html, and templates/partials/

**Checkpoint**: Representative pages satisfy the independent test at desktop and 390px widths, all primary actions are keyboard reachable with visible focus, and status meanings do not depend on color.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validate the independently deliverable UI increment and document the review results.

- [ ] T021 [P] Run focused UI rendering and existing regression tests from tests/test_ui_rendering.py and tests/
- [ ] T022 [P] Run python -m py_compile app.py and editor diagnostics for changed Python files
- [ ] T023 [P] Run git diff --check and review constitution compliance, route preservation, security/CSRF behavior, and accessibility criteria
- [ ] T024 [P] Validate representative pages at desktop and 390px widths with keyboard and touch using specs/004-responsive-accessible-ui/quickstart.md
- [ ] T025 Update README.md, HOW_IT_WORKS.md, and CHANGELOG.md with navigation terminology, responsive behavior, and accessibility improvements

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies; establish fixtures, quickstart, and asset entry points.
- **Phase 2 Foundational**: Depends on Phase 1 and blocks User Story 1.
- **User Story 1**: Depends on Phase 2; tests and implementation deliver the complete UI increment.
- **Polish**: Depends on User Story 1; validation tasks may run in parallel after implementation.

### User Story Dependencies

- **US1 (P2)**: Depends only on shared UI foundations and existing route/security behavior. It maps to User Story 3 from `specs/001-wnfc-improvements/spec.md` and does not require User Story 4 or User Story 5.

### Parallel Opportunities

- T002–T003 can run in parallel after T001.
- T005–T008 can run in parallel after the shared markup contract is agreed.
- T009–T011 can run in parallel because they target separate test concerns in the same test module; coordinate edits if implemented concurrently.
- T014–T017 can run in parallel because they target separate representative templates.
- T021–T024 can run in parallel after implementation is complete.

## Parallel Example: User Story 1

```text
Task: "Add navigation and landmark rendering assertions in tests/test_ui_rendering.py"
Task: "Add responsive page markup assertions in tests/test_ui_rendering.py"
Task: "Add keyboard, focus, feedback, and non-color assertions in tests/test_ui_rendering.py"

After the shared markup contract is stable:
Task: "Convert admin games and leaderboard layouts in templates/admin_games.html and templates/leaderboard.html"
Task: "Make home and game-detail layouts responsive in templates/index.html and templates/game_detail.html"
Task: "Make manual teams responsive in templates/teams_manual.html"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 Setup.
2. Complete Phase 2 Foundational.
3. Complete Phase 3 User Story 1.
4. **STOP and VALIDATE**: run focused tests and review representative pages at desktop and 390px widths.
5. Complete Phase 4 polish and documentation.

### Incremental Delivery

1. Establish shared landmarks, CSS, partials, and feedback semantics.
2. Deliver grouped navigation and mobile navigation.
3. Deliver responsive representative page layouts.
4. Deliver keyboard, focus, semantic feedback, and non-color status improvements.
5. Run cross-cutting validation and documentation updates.

## Notes

- Every task follows the required `- [ ] T### [P?] [US1?] Description with exact file path` format.
- `[P]` marks tasks that can run in parallel without conflicting incomplete dependencies.
- `[US1]` maps this feature's local story to User Story 3 from the parent specification.
- Tests are included because the specification explicitly requires automated rendering/accessibility coverage.
