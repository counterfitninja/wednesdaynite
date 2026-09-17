# Data Model: Maintainable Platform and Reliable PWA

## Migration Record

- Source table: `schema_migrations`.
- `version`: required immutable migration identifier; unique primary key.
- `applied_at`: required UTC timestamp.
- A migration is recorded only after its changes complete successfully.
- Re-running startup skips a version already recorded.

## Foreign-Key Invariants

- Every database connection enables SQLite foreign keys before queries execute.
- Existing historical attendance, payment, score, and team-assignment records MUST NOT be silently deleted by refactoring.
- Any changed delete/update action must specify and test its cascade, restrict, or preservation behavior.

## Notification Preference

- `enabled`: explicit application/admin setting controlling whether reminders may be scheduled.
- `opted_in`: explicit browser/user consent state; permission is requested only after a user action.
- `last_prompted_at` and `last_notified_at`: metadata used to avoid repeated prompts or duplicate reminders.
- Unsupported, denied, disabled, or malformed states are safe no-ops.

## Cache Manifest

- `cache_version`: release-specific identifier.
- `precache_urls`: assets safe to cache for the current release.
- HTML navigations are not treated as permanently immutable cached data.
- Previous cache versions are deleted during activation.

## Backup Artifact

- Contains a SQLite database copy/export plus schema migration version metadata.
- Restore validation checks database readability, expected tables, migration state, and representative records.
- A failed restore must not overwrite the known-good source database.

## Domain Module Boundaries

- `db`: connections, transactions, migration state, foreign keys, backup/restore helpers.
- `auth`: login/session/authorization helpers; must not import route modules.
- `services.statistics`: attendance/game calculations.
- `services.payments`: payment rules and summaries.
- `services.teams`: team assignment rules.
- `services.ocr`: optional adapter with a safe unavailable result.
- `routes`: HTTP parsing/rendering and calls into domain services; no circular imports.
