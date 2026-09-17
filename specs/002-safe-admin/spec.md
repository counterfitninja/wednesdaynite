# Feature Specification: Safe and Verifiable Administration

**Feature Branch**: `002-safe-admin`

**Created**: 2026-09-17

**Status**: Draft

**Input**: User Story 1 from `specs/001-wnfc-improvements/spec.md`.

## User Scenarios & Testing

### User Story 1 - Safe and Verifiable Administration (Priority: P1)

As an administrator, I need protected, observable, and tested administrative
workflows so attendance, payments, scores, imports, and player records cannot
be corrupted or exposed accidentally.

**Why this priority**: Security and data integrity are prerequisites for every
other application improvement.

**Independent Test**: Use an isolated SQLite database and Flask test client to
exercise login, protected routes, state-changing requests, representative game
mutations, import validation, abandoned-game calculations, and health checks.

**Acceptance Scenarios**:

1. **Given** an unauthenticated request, **when** an admin route or mutation is
  requested, **then** access is denied or redirected without changing data.
2. **Given** a state-changing form without a valid CSRF token, **when** it is
  submitted, **then** the request is rejected without changing data.
3. **Given** valid attendance, score, payment, team, import, and abandoned-game
  data, **when** statistics are calculated, **then** documented business rules
  are applied consistently.
4. **Given** a production-like request, **when** diagnostics are emitted,
  **then** passwords, secrets, tokens, and unnecessary personal data are absent
  from logs.
5. **Given** an invalid or oversized upload, **when** it is submitted, **then**
  it is rejected with a safe user-facing message and no unsafe file is stored.

## Edge Cases

- Login receives an incorrect or missing password.
- Login receives a malicious external `next` URL.
- A valid admin session expires while a form is open.
- A POST request has no CSRF token, an invalid token, or a token from another session.
- A game is abandoned after attendance, teams, payments, or scores exist.
- A player is merged or deleted while historical records reference that player.
- An import contains unknown, duplicate, malformed, or excessively long names.
- An uploaded image is malformed, oversized, or has an unsupported format.
- A health check is requested while the database is unavailable.

## Requirements

### Functional Requirements

- **FR-001**: System MUST require authentication for all administrative routes and state-changing actions.
- **FR-002**: System MUST reject state-changing requests without a valid CSRF token.
- **FR-003**: System MUST preserve existing attendance, score, payment, team, import, and abandoned-game rules.
- **FR-004**: System MUST prevent external open redirects from the login `next` parameter.
- **FR-005**: System MUST configure secure session cookie behavior for production deployments.
- **FR-006**: System MUST NOT log passwords, secrets, tokens, or unnecessary personal data.
- **FR-007**: System MUST use structured logging for authentication, mutation, import, and error events.
- **FR-008**: System MUST return safe 403, 404, and 500 responses without exposing implementation details.
- **FR-009**: System MUST validate uploaded files by type and size before processing or storage.
- **FR-010**: System MUST enforce SQLite foreign keys and document deletion/migration behavior.
- **FR-011**: System MUST provide isolated regression tests for authentication, CSRF, core game rules, imports, uploads, observability, and health checks.
- **FR-012**: System MUST keep health-check responses free of secrets and sensitive database details.

### Key Entities

- **Admin Session**: Authenticated browser session with secure cookie settings and a bounded lifetime.
- **Game Record**: Match data including attendance, teams, scores, payments, and abandoned state.
- **Player Record**: Player identity and related historical attendance, assignment, and payment records.
- **Upload**: User-submitted import or image data subject to validation and size limits.
- **Application Log Event**: Structured operational event that excludes sensitive values.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every covered administrative mutation has automated authentication and CSRF tests.
- **SC-002**: Unauthorized and invalid-CSRF requests change zero database records in tests.
- **SC-003**: Regression tests cover authentication, attendance, scores, payments, teams, imports, uploads, and abandoned-game calculations.
- **SC-004**: Automated log assertions find no password, secret, token, or raw credential values in covered request logs.
- **SC-005**: Invalid and oversized uploads are rejected without creating unsafe stored data.
- **SC-006**: 403, 404, 500, and health-check responses are safe and test-covered.

## Assumptions

- The existing Flask, SQLite, Jinja, and server-rendered architecture remains in place.
- Existing valid admin workflows and database records remain backward-compatible.
- A lightweight Flask-compatible CSRF solution may be added as a dependency if no existing mechanism is available.
- The application remains a small-group football tracker rather than a multi-tenant service.
