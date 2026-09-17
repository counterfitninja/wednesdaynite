---

description: "Actionable tasks for Safe and Verifiable Administration"
---

# Tasks: Safe and Verifiable Administration

**Input**: Design documents from `/specs/002-safe-admin/`

**Prerequisites**: `spec.md`, `plan.md`, `quickstart.md`, and `.specify/memory/constitution.md`

**Tests**: Included because the feature specification requires isolated regression coverage.

**Organization**: Tasks are grouped by the single User Story 1 increment.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish isolated testing and dependency foundations.

- [ ] T001 Create a temporary SQLite Flask test fixture and test application configuration in `tests/conftest.py`
- [ ] T002 [P] Add pytest and CSRF dependency requirements in `requirements.txt`
- [ ] T003 [P] Document the safe-administration test workflow in `specs/002-safe-admin/quickstart.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Provide shared security, logging, database, and error-handling infrastructure.

**⚠️ CRITICAL**: Complete this phase before User Story 1 implementation tasks.

- [ ] T004 Remove password-length, password-match, and credential debug output from the login route in `app.py`
- [ ] T005 Add structured logging configuration and sensitive-value filtering for authentication, mutations, imports, uploads, and errors in `app.py`
- [ ] T006 Add CSRF protection middleware and token generation/validation integration in `app.py`, `templates/base.html`, and `templates/`
- [ ] T007 Configure secure session cookie settings from environment-aware configuration in `app.py`
- [ ] T008 Validate the login `next` parameter as a local URL before redirecting in `app.py`
- [ ] T009 Add safe 403, 404, and 500 error handlers and templates in `app.py` and `templates/`
- [ ] T010 Enable SQLite foreign keys and document deletion/migration behavior in `app.py` and `README.md`

**Checkpoint**: Shared security and observability infrastructure is ready.

---

## Phase 3: User Story 1 - Safe and Verifiable Administration (Priority: P1) 🎯 MVP

**Goal**: Protect administrative workflows and prove core data rules remain correct without exposing secrets.

**Independent Test**: Run all US1 tests against an isolated SQLite database; verify unauthenticated and invalid-CSRF requests change no data, valid requests preserve business rules, logs contain no sensitive values, invalid uploads are rejected, and error/health responses are safe.

### Tests for User Story 1

- [ ] T011 [P] [US1] Add authentication, session, protected-route, and local-redirect tests in `tests/test_auth.py`
- [ ] T012 [P] [US1] Add missing-token, invalid-token, cross-session-token, and valid-token tests in `tests/test_csrf.py`
- [ ] T013 [P] [US1] Add attendance, score, payment, team, abandoned-game, and statistics regression tests in `tests/test_game_rules.py`
- [ ] T014 [P] [US1] Add CSV/import name validation and unknown/duplicate input tests in `tests/test_imports.py`
- [ ] T015 [P] [US1] Add malformed, oversized, unsupported-format, and safe-processing tests in `tests/test_uploads.py`
- [ ] T016 [P] [US1] Add secret-free log assertions and health-check response tests in `tests/test_observability.py`
- [ ] T017 [P] [US1] Add safe 403, 404, and 500 response tests in `tests/test_errors.py`

### Implementation for User Story 1

- [ ] T018 [US1] Add CSRF fields to every state-changing form and ensure AJAX-style mutations send CSRF credentials in `templates/` and static JavaScript files
- [ ] T019 [US1] Update all administrative mutation routes to reject invalid requests before database writes in `app.py`
- [ ] T020 [US1] Preserve existing attendance, payment, score, team, import, upload, and abandoned-game rules while routing diagnostics through structured logging in `app.py`
- [ ] T021 [US1] Add safe user-facing error and validation messages without stack traces or credentials in `templates/login.html`, `templates/`, and `app.py`
- [ ] T022 [US1] Ensure health endpoints return only safe status/version information and handle database failures predictably in `app.py`
- [ ] T023 [US1] Add regression coverage for player merge/delete behavior and foreign-key cleanup semantics in `tests/test_player_data_integrity.py`

**Checkpoint**: User Story 1 is complete when all tests pass and protected workflows preserve existing data rules.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validate the increment and update operational documentation.

- [ ] T024 [P] Run `python -m py_compile app.py` and editor diagnostics for changed Python files in the repository
- [ ] T025 [P] Run the complete focused US1 test suite from `tests/`
- [ ] T026 [P] Run the manual verification steps in `specs/002-safe-admin/quickstart.md`
- [ ] T027 [P] Run `git diff --check` and review compliance against `.specify/memory/constitution.md`
- [ ] T028 Update `README.md`, `RELEASE_CHECKLIST.md`, and `CHANGELOG.md` with security configuration, testing, and operational behavior

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies.
- **Phase 2 Foundational**: Depends on Phase 1 and blocks all US1 implementation.
- **Phase 3 US1**: Depends on Phase 2; tests precede implementation where practical.
- **Phase 4 Polish**: Depends on completed US1 behavior.

### User Story Dependencies

- **US1 (P1)**: This is the only story in this feature and is independently testable after Phase 2.

### Parallel Opportunities

- T002 and T003 can run in parallel after T001.
- T011–T017 can run in parallel once the test fixture exists.
- T024–T027 can run in parallel after implementation is complete.

## Implementation Strategy

### MVP First

1. Complete Phase 1 Setup.
2. Complete Phase 2 Foundational.
3. Complete Phase 3 User Story 1.
4. Stop and validate with the US1 independent test criteria.
5. Complete Phase 4 polish and documentation.

### Notes

- Every task follows `- [ ] T### [P?] [US1?] Description with exact file path`.
- `[P]` is used only for tasks that can be performed in parallel without incomplete-file dependencies.
- No extension hooks are configured in `.specify/extensions.yml`.
