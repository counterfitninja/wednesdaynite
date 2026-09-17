---

description: "Actionable tasks for Maintainable Platform and Reliable PWA"
---

# Tasks: Maintainable Platform and Reliable PWA

**Input**: Design documents from `/specs/006-maintainable-platform-pwa/`

**Parent story**: User Story 5 from `specs/001-wnfc-improvements/spec.md`

**Prerequisites**: `spec.md`, `plan.md`, `data-model.md`, `contracts/platform-pwa.md`, `quickstart.md`, and completed/stable behavior from `specs/002-safe-admin/`, `specs/003-matchday-dashboard/`, `specs/004-responsive-accessible-ui/`, and `specs/005-mobile-team-attendance/`

**Tests**: Included because the feature specification explicitly requires migration, PWA, module-boundary, backup/restore, optional-dependency, and full regression coverage.

**Organization**: This feature isolates the parent US5 increment as local User Story 1 so it can be implemented and tested independently.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish fixtures, test entry points, and operational references without changing runtime behavior.

- [ ] T001 Create isolated application/database fixtures and representative legacy records for platform tests in `tests/conftest.py`
- [ ] T002 [P] Add migration, service-worker, notification, module-boundary, backup/restore, and optional-OCR test commands in `pytest.ini` and `README.md`
- [ ] T003 [P] Add the platform validation scenarios and release assumptions to `specs/006-maintainable-platform-pwa/quickstart.md`
- [ ] T004 [P] Add a versioned static asset manifest/offline fallback entry point in `templates/base.html` and `static/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define compatibility, persistence, transaction, and dependency guardrails required by every US1 task.

**⚠️ CRITICAL**: Complete this phase before implementing User Story 1 behavior.

- [ ] T005 Add characterization tests for representative route paths, methods, statuses, redirects, and core records before module extraction in `tests/test_route_compatibility.py`
- [ ] T006 [P] Add SQLite connection helpers that enable foreign keys before use and expose transaction boundaries in `db.py`
- [ ] T007 [P] Define migration record schema and ordered migration runner interfaces in `db.py` and `migrations/runner.py`
- [ ] T008 [P] Define guarded optional-OCR adapter interfaces and unavailable-result behavior in `services/ocr.py`
- [ ] T009 [P] Define service-worker cache version, navigation strategy, notification states, and backup/restore compatibility rules in `specs/006-maintainable-platform-pwa/contracts/platform-pwa.md`
- [ ] T010 Add test helpers for database snapshots, migration records, cache messages, and sensitive optional-dependency imports in `tests/helpers.py`

**Checkpoint**: Compatibility baselines, database invariants, migration interfaces, and dependency boundaries are ready.

---

## Phase 3: User Story 1 - Maintainable Platform and Reliable PWA (Priority: P3) 🎯 MVP

**Goal**: Improve maintainability and operational reliability without changing existing user-facing route contracts.

**Independent Test**: Apply migrations twice to a database copy, verify foreign-key behavior and representative records, import extracted modules without cycles, run the base profile without OCR packages, verify service-worker update/offline behavior, exercise explicit notification opt-in states, and complete backup/restore verification.

### Tests for User Story 1

- [ ] T011 [P] [US1] Add migration ordering, repeatability, interruption/retry, recorded-version, and data-preservation tests in `tests/test_migrations.py`
- [ ] T012 [P] [US1] Add SQLite foreign-key enforcement and historical attendance/payment/score/team-record preservation tests in `tests/test_migrations.py`
- [ ] T013 [P] [US1] Add module import, dependency-direction, route compatibility, and no-cycle smoke tests in `tests/test_platform.py` and `tests/test_route_compatibility.py`
- [ ] T014 [P] [US1] Add service-worker install, activation cleanup, version replacement, network-first navigation, offline fallback, and current-HTML tests in `tests/test_service_worker.py`
- [ ] T015 [P] [US1] Add notification disabled, unsupported, default, denied, explicit-opt-in, malformed-settings, and no-repeat-prompt tests in `tests/test_notifications.py`
- [ ] T016 [P] [US1] Add base-profile startup and OCR-unavailable behavior tests without OCR-only packages in `tests/test_optional_dependencies.py`
- [ ] T017 [P] [US1] Add backup creation, isolated restore, schema/version verification, corrupt-backup rejection, and rollback-safety tests in `tests/test_backup_restore.py`

### Implementation for User Story 1

- [ ] T018 [US1] Implement application-owned migration records, ordered pending migration execution, transactional failure handling, and startup integration in `db.py`, `migrations/runner.py`, `migrations/001_initial_platform.py`, and `app.py`
- [ ] T019 [US1] Enable SQLite foreign keys on every connection and preserve/test historical delete/update behavior in `db.py` and `app.py`
- [ ] T020 [US1] Extract database connection, transaction, query, and backup helpers from `app.py` into `db.py` while retaining compatibility imports and route behavior
- [ ] T021 [US1] Extract authentication/session helpers into `auth.py` and route registration into `routes/` without changing protected-route contracts
- [ ] T022 [US1] Extract statistics, payment, and team domain operations into `services/statistics.py`, `services/payments.py`, and `services/teams.py` with explicit dependency direction
- [ ] T023 [US1] Add guarded OCR loading and a safe unavailable response when OCR dependencies are absent in `services/ocr.py`, `app.py`, `templates/`, `requirements.txt`, and `requirements-ocr.txt`
- [ ] T024 [US1] Add explicit backup/export, isolated restore, schema/version verification, and safe failure handling in `db.py`, `app.py`, `templates/`, and `README.md`
- [ ] T025 [US1] Replace fixed service-worker cache behavior with release-versioned caches, old-cache cleanup, `clients.claim()`, network-first navigation, static-asset fallback, and offline fallback in `static/service-worker.js`
- [ ] T026 [US1] Add a readable offline fallback page and ensure current HTML is not permanently served from an old cache in `templates/offline.html`, `templates/base.html`, and `static/service-worker.js`
- [ ] T027 [US1] Change notification permission flow to explicit user opt-in, persist prompt/notification state, and treat unsupported/denied/disabled/malformed settings as recoverable no-ops in `static/notifications.js` and `templates/base.html`
- [ ] T028 [US1] Add notification and service-worker registration feedback that does not create retry loops or unhandled promise errors in `static/notifications.js` and `templates/base.html`
- [ ] T029 [US1] Document default and OCR dependency profiles, migration startup behavior, backup/restore verification, rollback, PWA updates, and notification support in `requirements.txt`, `requirements-ocr.txt`, `README.md`, `HOW_IT_WORKS.md`, and `RELEASE_CHECKLIST.md`

**Checkpoint**: US1 is complete when focused platform tests and the full regression suite pass, startup is repeatable, route behavior remains compatible, PWA updates are not stale, notification permission is opt-in, and backup/restore is verified.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validate the maintainability increment across code, browser behavior, dependencies, and operations.

- [ ] T030 [P] Run migration, foreign-key, module-boundary, PWA, notification, optional-dependency, backup/restore, and parent regression tests from `tests/`
- [ ] T031 [P] Run `python -m py_compile app.py db.py auth.py services/*.py routes/*.py migrations/*.py` and review editor diagnostics
- [ ] T032 [P] Run the service-worker, offline, notification, and base-profile/OCR manual checks in `specs/006-maintainable-platform-pwa/quickstart.md`
- [ ] T033 [P] Run `git diff --check` and review migration, delete behavior, route compatibility, secret handling, and rollback safety against the feature contracts
- [ ] T034 Update `CHANGELOG.md`, `README.md`, `HOW_IT_WORKS.md`, and `RELEASE_CHECKLIST.md` with shipped platform and PWA behavior

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies; establishes fixtures, test commands, and asset entry points.
- **Phase 2 Foundational**: Depends on Phase 1 and blocks User Story 1.
- **User Story 1**: Depends on Phase 2 and on stable behavior from the parent US1–US4 increments; tests should characterize behavior before extraction.
- **Polish**: Depends on completed User Story 1 implementation; validation tasks can then run in parallel.

### User Story Dependencies

- **US1 (local, parent US5 P3)**: Depends on the application behavior and security protections delivered by the earlier parent stories, but is independently testable using isolated databases and compatibility tests.

### Parallel Opportunities

- T002–T004 can run in parallel after T001.
- T006–T009 can run in parallel after compatibility assumptions are agreed.
- T011–T017 can run in parallel because they cover separate focused test concerns.
- T020–T023 can be developed in parallel once module boundaries are agreed; coordinate shared imports.
- T025–T028 can be developed in parallel after the service-worker/notification contract is stable.
- T030–T033 can run in parallel after implementation is complete.

## Parallel Example: User Story 1

```text
Task: "Add migration and foreign-key tests in tests/test_migrations.py"
Task: "Add module-boundary and route-compatibility tests in tests/test_platform.py and tests/test_route_compatibility.py"
Task: "Add service-worker lifecycle tests in tests/test_service_worker.py"
Task: "Add notification state tests in tests/test_notifications.py"
Task: "Add optional-dependency tests in tests/test_optional_dependencies.py"
Task: "Add backup/restore tests in tests/test_backup_restore.py"

After contracts are stable:
Task: "Implement ordered migrations and startup integration in db.py, migrations/, and app.py"
Task: "Extract domain services in services/ and preserve route compatibility"
Task: "Implement versioned service-worker lifecycle in static/service-worker.js"
Task: "Implement explicit notification opt-in in static/notifications.js and templates/base.html"
```

## Implementation Strategy

### MVP First (Parent User Story 5 Only)

1. Complete Phase 1 Setup.
2. Complete Phase 2 Foundational.
3. Complete Phase 3 User Story 1.
4. **STOP and VALIDATE**: run isolated migration/backup tests, import the base profile without OCR, run full regression, and review service-worker/notification behavior.
5. Complete Phase 4 polish and documentation.

### Incremental Delivery

1. Establish characterization tests and data invariants.
2. Deliver repeatable migrations, foreign-key enforcement, and backup/restore verification.
3. Extract backend modules without route contract changes.
4. Deliver reliable service-worker cache updates and offline navigation fallback.
5. Deliver explicit notification opt-in and recoverable unsupported states.
6. Isolate OCR dependencies and document release/rollback procedures.

## Notes

- Every task follows the required `- [ ] T### [P?] [US1?] Description with exact file path` checklist format.
- `[P]` marks tasks that can be performed in parallel without incomplete-file dependencies.
- `[US1]` is the local story label and maps to parent User Story 5.
- The feature directory is `specs/006-maintainable-platform-pwa/` because the existing numbered feature directories end at `005-mobile-team-attendance/`.
