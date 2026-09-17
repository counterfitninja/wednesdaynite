# Feature Specification: Maintainable Platform and Reliable PWA

**Feature Branch**: `006-maintainable-platform-pwa`

**Created**: 2026-09-17

**Status**: Draft

**Input**: User Story 5 from `specs/001-wnfc-improvements/spec.md`.

## User Scenarios & Testing

### User Story 1 - Maintainable Platform and Reliable PWA (Priority: P3)

As a maintainer, I need separable domain code, explicit migrations, reliable offline/cache behavior, and dependable notifications so the application is safer to evolve and operate.

**Why this priority**: These changes reduce long-term risk after the user-facing workflows are stabilized.

**Independent Test**: Run the regression suite, apply migrations repeatedly to a copy of the database, inspect importable module boundaries and optional dependencies, exercise backup/restore documentation, and validate service-worker cache replacement and notification behavior with browser-compatible tests or a documented manual harness.

**Acceptance Scenarios**:

1. **Given** a schema change, **when** the application starts, **then** a versioned, repeatable migration applies without data loss and does not reapply an already-recorded migration.
2. **Given** a new deployment, **when** the service worker activates, **then** old caches are removed, current assets are available, and navigations do not remain unexpectedly stale.
3. **Given** notifications are disabled, unsupported, denied, or not yet explicitly enabled, **when** the app runs, **then** it does not repeatedly prompt, throw unhandled errors, or schedule reminders.
4. **Given** the application is installed with the base dependency profile, **when** it starts without OCR packages, **then** non-OCR routes remain importable and usable.
5. **Given** a maintainer follows the backup procedure, **when** a backup is restored into an isolated database, **then** the documented verification steps confirm schema and representative records are intact.
6. **Given** the backend is divided into domain modules, **when** the application starts and tests import those modules, **then** route behavior remains backward-compatible and module dependencies do not create import cycles.

## Edge Cases

- A migration is interrupted and then resumed.
- The database already contains the migration version being applied.
- A migration encounters an incompatible or partially-created legacy table.
- A service-worker cache contains assets from a prior release and the network is unavailable.
- A navigation request receives an HTML response while an older HTML page is cached.
- Notification permission is `default`, `denied`, unsupported, or revoked after previously being granted.
- The notification settings endpoint is unavailable or returns malformed JSON.
- OCR is requested when optional OCR dependencies are not installed.
- A backup is missing, corrupt, from an older schema, or restored over the wrong database.
- A refactoring accidentally changes a route's response status, redirect, or transaction behavior.

## Requirements

### Functional Requirements

- **FR-001**: System MUST represent schema changes as ordered, versioned, repeatable migrations with an application-recorded migration state.
- **FR-002**: System MUST apply pending migrations transactionally where supported and MUST NOT silently discard existing data.
- **FR-003**: System MUST enforce and test foreign-key behavior while preserving historical attendance, payment, score, and assignment records.
- **FR-004**: System MUST keep domain modules importable without requiring optional OCR/deployment-heavy dependencies for non-OCR routes.
- **FR-005**: System MUST preserve existing route behavior while separating database access, authentication, statistics, payments, OCR, and team logic into understandable modules.
- **FR-006**: System MUST version service-worker caches and delete caches belonging to previous application versions during activation.
- **FR-007**: System MUST use a network-first strategy for navigations or another documented strategy that prevents unexpectedly stale HTML after deployment.
- **FR-008**: System MUST provide a usable offline fallback for navigation when the network is unavailable and no current response can be fetched.
- **FR-009**: System MUST request notification permission only after explicit user opt-in and MUST persist enough state to avoid repeated prompts.
- **FR-010**: System MUST treat unsupported, denied, disabled, unavailable, and malformed notification states as no-op or recoverable conditions.
- **FR-011**: System MUST document backup, restore, verification, and rollback procedures for maintainers.
- **FR-012**: System MUST isolate optional OCR dependencies in a documented installation profile and provide a safe user-facing unavailable response.

### Key Entities

- **Migration Record**: An applied migration identified by an immutable version and recorded application timestamp.
- **Domain Module**: An importable unit containing database, authentication, statistics, payment, team, or OCR responsibilities with explicit dependencies.
- **Cache Manifest**: A release-specific service-worker asset set identified by a cache version.
- **Notification Preference**: Persisted user/admin opt-in state and last-prompt/notification metadata.
- **Backup Artifact**: A database export with schema/version metadata and documented restore verification.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Running startup migration twice produces no duplicate migration records and preserves representative existing records.
- **SC-002**: Foreign-key and migration tests pass against an isolated SQLite database.
- **SC-003**: Service-worker update tests show old caches deleted and navigation loading current HTML rather than stale cached HTML.
- **SC-004**: Notification tests show zero permission prompts when disabled, unsupported, denied, or already opted out.
- **SC-005**: The base dependency profile imports and starts the application without installing OCR-only packages; OCR requests return a documented safe response when unavailable.
- **SC-006**: Backup and restore verification succeeds on a copy of the database using the documented release procedure.
- **SC-007**: Full regression tests pass after module extraction with no route contract regressions.

## Assumptions

- Flask, SQLite, Jinja, and the existing server-rendered architecture remain in place.
- Existing database records and route URLs remain backward-compatible unless a migration or compatibility note explicitly says otherwise.
- SQLite is the primary deployment database for this increment.
- Browser notification delivery remains best-effort and does not require introducing a provider-specific Web Push backend.
- Heavy OCR packages remain optional rather than part of the minimum runtime profile.
