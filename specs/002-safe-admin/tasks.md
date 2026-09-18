---
description: "Actionable tasks for Safe and Verifiable Administration"
---

# Tasks: Safe and Verifiable Administration

**Input**: Design documents from `/specs/002-safe-admin/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/security-behavior.md`, and `quickstart.md`

**Tests**: Included because FR-011 and the feature specification explicitly
require isolated regression coverage.

**Organization**: Tasks are grouped by the single P1 user story so the story
can be implemented and tested as one independently verifiable increment.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish reliable isolated test and documentation seams.

- [X] T001 Correct the temporary SQLite Flask fixture to set the application database path before initialization and expose a working connection helper in `tests/conftest.py`
- [X] T002 [P] Add a route/mutation inventory test helper that records database snapshots before and after rejected requests in `tests/conftest.py`
- [X] T003 [P] Document the isolated test commands, environment assumptions, and expected security outcomes in `specs/002-safe-admin/quickstart.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Complete shared security and persistence behavior before story work.

**⚠️ CRITICAL**: Complete this phase before Phase 3 implementation tasks.

- [X] T004 Remove the signed-token fallback from CSRF validation so only an exact current-session token match is accepted, while preserving form and `X-CSRFToken` sources in `app.py`
- [X] T005 [P] Protect `edit_player` and audit every administrative mutation for `@login_required`, including GET routes that write state, in `app.py`
- [X] T006 [P] Rotate authentication-related session/CSRF state after successful login and emit redacted authentication outcome events in `app.py`
- [X] T007 [P] Replace CSRF diagnostics that include unnecessary request metadata or session keys with structured event fields that exclude tokens, cookies, contact data, and raw request values in `app.py`
- [X] T008 Add safe local redirect validation to every mutation redirect that currently trusts `request.referrer`, including PayPal transaction assignment, in `app.py`
- [X] T009 [P] Add explicit safe handling for malformed score/status/ID inputs before database writes while preserving documented attendance values `playing`, `maybe`, and `not_playing` in `app.py`
- [X] T010 [P] Define shared bounded upload and import limits for bytes, rows, field counts, and field lengths in `app.py`, keeping the existing 8 MB global request limit
- [X] T011 [P] Document SQLite foreign-key enforcement, merge/delete relationship behavior, backup, and restore expectations in `README.md`

**Checkpoint**: Authentication, session-bound CSRF, validation boundaries,
redirect safety, and persistence policy are ready for story implementation.

---

## Phase 3: User Story 1 - Safe and Verifiable Administration (Priority: P1)

**Goal**: Protect administrative workflows and prove attendance, payment,
score, team, import, upload, logging, health, and abandoned-game rules remain
correct without exposing sensitive data.

**Independent Test**: Run the complete focused suite against an isolated SQLite
database; anonymous and invalid-CSRF requests change zero rows, valid requests
preserve business rules, unsafe uploads are rejected, logs are redacted, and
health/error responses are safe.

### Tests for User Story 1

- [X] T012 [P] [US1] Add authentication and authorization matrix tests for anonymous admin access, `edit_player`, state-changing routes, session cookies, failed login, successful login, logout, and malicious local/external `next` values in `tests/test_auth.py`
- [X] T013 [P] [US1] Add CSRF tests for missing, invalid, expired, cross-session, valid form, and valid `X-CSRFToken` requests, asserting rejected requests change zero rows in `tests/test_csrf.py`
- [X] T014 [P] [US1] Add AJAX payment regression coverage that sends the CSRF header and verifies missing/invalid headers are rejected without changing payment state in `tests/test_csrf.py` and `templates/game_detail.html`
- [X] T015 [P] [US1] Add attendance, payment, score, team generation/manual assignment, abandoned-game, and statistics regression tests with zero-change assertions for invalid inputs in `tests/test_game_rules.py`
- [ ] T016 [P] [US1] Add import tests for byte/row/field limits, required headers, unknown and duplicate names, malformed values, transactional rollback, and generic user-facing failures in `tests/test_imports.py`
- [ ] T017 [P] [US1] Add upload tests for invalid magic bytes, oversized files, unsupported formats, malformed SVG, decompression-bomb defenses, and preservation of an existing valid asset after failed replacement in `tests/test_uploads.py`
- [ ] T018 [P] [US1] Add player merge/delete tests covering attendance, team assignments, payments, share tokens, foreign keys, duplicate relationships, self-merge, and nonexistent IDs in `tests/test_player_data_integrity.py`
- [X] T019 [P] [US1] Add observability tests asserting passwords, secrets, CSRF/session/share tokens, contact data, filenames, and raw exception details are absent from captured logs; test healthy and unavailable-database health responses in `tests/test_observability.py`
- [ ] T020 [P] [US1] Add safe 403, 404, 500, CSRF-failure, malformed-mutation, and database-failure response tests with no paths, SQL, stack traces, or secrets in `tests/test_errors.py`

### Implementation for User Story 1

- [X] T021 [US1] Add or correct hidden CSRF fields in every state-changing template and add the current token to the payment AJAX request body or `X-CSRFToken` header in `templates/` and `static/`
- [X] T022 [US1] Convert team generation from a state-changing GET into an authenticated CSRF-protected mutation while retaining a safe read-only team display route in `app.py` and `templates/teams.html`
- [ ] T023 [US1] Remove or isolate public homepage auto-creation side effects so public reads do not create game records unexpectedly, while preserving the weekly game workflow in `app.py`
- [X] T024 [US1] Add structured authentication, mutation, import, upload, and error events with redacted metadata and replace remaining security-relevant `print()` diagnostics in `app.py`
- [X] T025 [US1] Implement strict score, attendance-status, referenced-record, duplicate-player, and malformed-input validation before commits, returning safe actionable messages in `app.py` and affected templates
- [X] T026 [US1] Make CSV and PayPal imports bounded, schema-validated, transactional, and generic on user-facing failure while logging controlled diagnostic events in `app.py` and import templates
- [X] T027 [US1] Validate image content and size before processing, reject unsafe SVG content or rasterize it, and atomically replace player/face/sticker/shield assets only after successful validation in `app.py`
- [X] T028 [US1] Implement explicit merge/delete relationship handling for attendance, team assignments, payment transactions, and share tokens under SQLite foreign keys in `app.py`
- [X] T029 [US1] Make `/healthz` and `/status` probe database availability and return only the documented stable status/build contract, including a non-sensitive 503 failure response, in `app.py`
- [X] T030 [US1] Ensure 403, 404, 500, import, upload, and malformed mutation responses use safe user-facing messages and never expose implementation details in `app.py` and `templates/error.html`

**Checkpoint**: User Story 1 passes its independent test criteria and all
covered administrative mutations are authenticated, CSRF-protected, validated,
observable, and regression-tested.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Validate the completed increment and update operational records.

- [X] T031 [P] Run the focused Safe Administration suite and the full pytest suite from the repository root, recording failures and fixes in `tests/`
- [X] T032 [P] Run `python -m py_compile app.py` and editor diagnostics for changed Python files
- [X] T033 [P] Run `git diff --check` and review changed routes, templates, logs, and persistence behavior against `.specify/memory/constitution.md`
- [ ] T034 [P] Execute every automated and manual scenario in `specs/002-safe-admin/quickstart.md` and confirm the contract in `specs/002-safe-admin/contracts/security-behavior.md`
- [X] T035 Update `README.md`, `RELEASE_CHECKLIST.md`, and `CHANGELOG.md` with secure configuration, health behavior, upload/import limits, tests, and deletion/restore operations

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies.
- **Phase 2 Foundational**: Depends on Phase 1 and blocks User Story 1.
- **Phase 3 User Story 1**: Depends on Phase 2; tests should be written before or alongside each implementation slice.
- **Phase 4 Polish**: Depends on the completed User Story 1 implementation and tests.

### User Story Dependencies

- **US1 (P1)**: The only story; independently testable after Phase 2.

### Parallel Opportunities

- After T001, T002 and T003 can run in parallel.
- After T004, T005 through T011 can be split among security, validation, and documentation work when edits do not overlap.
- After T001–T011, T012–T020 can run in parallel because each owns a focused test module or template seam.
- After the corresponding tests exist, T021–T030 can be parallelized by CSRF/templates, imports, uploads, data integrity, observability, and error handling, with `app.py` changes coordinated to avoid conflicts.
- T031–T034 can run in parallel after implementation; T035 follows the verified behavior.

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Deliver T012–T014 and T021–T024 first to close authentication, CSRF, session, and logging risks.
3. Deliver T015–T020 with T025–T030 to cover data integrity, imports, uploads, health, and errors.
4. Stop and validate the User Story 1 independent test criteria.
5. Complete Phase 4 documentation and release checks.

### Format Validation

All 35 tasks use the required `- [ ] T###` checklist format. Setup,
foundational, and polish tasks have no story label; every User Story 1 task has
the `[US1]` label. Parallel tasks include `[P]` only where file ownership and
dependencies permit parallel work. Every task names an exact repository path.
