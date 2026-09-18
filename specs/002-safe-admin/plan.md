# Implementation Plan: Safe and Verifiable Administration

**Branch**: `002-safe-admin` | **Date**: 2026-09-17 | **Spec**: `specs/002-safe-admin/spec.md`

## Summary

Harden the existing Flask/SQLite administration surface without changing the
server-rendered architecture. The implementation will first close authorization
and CSRF gaps, then centralize safe validation/logging/error behavior, preserve
game and payment rules, harden imports/uploads and health checks, and prove the
result with isolated Flask test-client regressions.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: Flask 3.1, Werkzeug 3.1, Pillow 11, pytest 8; existing `itsdangerous` serializer
**Storage**: SQLite file database with per-connection `PRAGMA foreign_keys = ON`
**Testing**: pytest, Flask test client, temporary SQLite databases, `caplog`
**Target Platform**: Local Windows development and Linux/Azure-style production
**Project Type**: Server-rendered Flask web application
**Performance Goals**: Security validation must occur before mutation; health checks should remain lightweight; no new blocking service dependency
**Constraints**: Preserve existing routes and business rules where compatible; keep production dependencies minimal; do not expose secrets, tokens, paths, or raw exception details
**Scale/Scope**: Small-group football tracker; one application process/database file and the complete current admin mutation surface

## Constitution Check

*GATE: Must pass before Phase 0 research and after Phase 1 design.*

- **Matchday Value First**: PASS — security work protects attendance, teams,
	payments, and results without changing the weekly workflow.
- **Data Integrity Over Convenience**: PASS — validation, transaction boundaries,
	foreign keys, and explicit merge/delete semantics are design requirements.
- **Secure by Default**: PASS — authenticated mutations, strict session-bound
	CSRF, secure cookies, safe redirects, redacted logs, and bounded uploads.
- **Tested, Observable, and Verifiable**: PASS — focused regression tests,
	structured events, safe health responses, syntax checks, and diff checks.
- **Simple, Accessible, and Maintainable**: PASS — retain Flask/Jinja and the
	application-local CSRF mechanism; avoid a framework migration or unnecessary
	dependency.
- **Operational constraints**: PASS — production secrets remain environment
	configured, SQLite behavior is explicit, and README/release documentation is
	updated.

No constitution violations require a complexity exception.

## Research Summary

Research is recorded in `research.md`. The repository already contains partial
security infrastructure, so implementation must harden and complete it rather
than duplicate it. Key decisions are strict session-bound CSRF, route-by-route
authorization auditing, generic user-facing import errors, atomic validated
upload replacement, bounded imports, and a minimal database-aware health
contract.

## Design: Phase 0 and Phase 1 Outputs

- `research.md`: existing behavior, identified gaps, decisions, and rejected
	alternatives.
- `data-model.md`: security/session, game/player relationship, upload, log-event,
	import, and health response invariants.
- `contracts/security-behavior.md`: protected-request, CSRF, redirect, error,
	upload, log, and health contracts.
- `quickstart.md`: runnable isolated validation scenarios and expected outcomes.

## Project Structure

```text
app.py                         # auth, CSRF, validation, logging, health, routes
templates/                     # CSRF-bearing forms and safe error/login views
static/                        # AJAX requests carrying CSRF headers/tokens
tests/conftest.py              # isolated app/database fixtures
tests/test_auth.py             # auth and authorization matrix
tests/test_csrf.py             # token lifecycle and cross-session rejection
tests/test_game_rules.py       # attendance, teams, scores, payments, abandoned games
tests/test_imports.py          # bounded and transactional CSV/import behavior
tests/test_uploads.py          # image/SVG validation and atomic replacement
tests/test_player_data_integrity.py # merge/delete/foreign-key behavior
tests/test_observability.py    # logs and health contract
tests/test_errors.py           # safe 403/404/500 responses
README.md                      # configuration, backup, and operational behavior
RELEASE_CHECKLIST.md           # deployment verification
CHANGELOG.md                   # user-visible security changes
```

**Structure Decision**: Keep the current single Flask application and server-
rendered templates. Add focused test modules rather than introducing blueprints
or service layers during this security increment; refactoring remains a later
maintainability feature.

## Delivery Strategy

1. Correct the test fixture seam and inventory every mutation.
2. Close authorization, CSRF, session, redirect, and AJAX-token gaps.
3. Add shared validation, redacted structured logging, and safe error handling.
4. Harden foreign-key/delete/merge behavior while preserving documented rules.
5. Harden CSV/image/SVG upload processing and make health responses database-aware.
6. Run focused tests, full tests, syntax/diagnostic checks, and `git diff --check`.

## Quality Gates

- Every state-changing route is authenticated where administrative and rejects
	missing, invalid, expired, or cross-session CSRF before database writes.
- Rejected requests leave database rows and existing upload files unchanged.
- Attendance, scores, payments, teams, imports, and abandoned-game rules have
	passing regression coverage.
- Captured logs contain no password, secret, token, session cookie, contact data,
	or raw exception details.
- Upload and health contracts pass, including dependency failure behavior.
- `pytest`, `python -m py_compile app.py`, editor diagnostics, and `git diff --check`
	pass.

## Post-Design Constitution Re-check

PASS. The design retains the documented Flask/SQLite architecture, adds no
unjustified complexity, makes security and data-integrity invariants testable,
and identifies operational/documentation validation as completion gates.
