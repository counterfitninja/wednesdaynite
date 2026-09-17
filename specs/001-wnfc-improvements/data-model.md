# Data Model: Wednesday Night FC Improvements

## Existing domain entities

### Game

- **Identity**: integer `id`.
- **Attributes**: scheduled date, location, notes, team scores, and `is_abandoned` state.
- **Relationships**: has many attendance records and team assignments; may have payment transactions through player attendance/payment data.
- **Rules**: abandoned games remain distinguishable and are excluded from statistics wherever the product rules require it. Historical game data must not be silently changed by presentation logic.

### Player

- **Identity**: integer `id`.
- **Attributes**: name, alias, skill rating, attendance history, payment attributes, and optional face/image data.
- **Relationships**: participates in attendance records, team assignments, and payment transactions.
- **Rules**: deletion or merge must preserve historical assignments and payments according to an explicit, tested policy.

### Attendance

- **Identity**: game/player association.
- **Attributes**: attendance status and paid/payment state.
- **Relationships**: belongs to one Game and one Player.
- **Rules**: updates are protected by authentication and CSRF for online writes; offline writes carry an operation ID and synchronization metadata.

### Team Assignment

- **Identity**: game/player association, with team membership.
- **Attributes**: assigned team and any persisted balancing metadata used by current rules.
- **Relationships**: belongs to one Game and one Player.
- **Rules**: mobile assignment must support explicit move, unassign, and optional swap actions without drag-and-drop. Counts, skill totals, and balance difference update after changes.

### Payment Transaction

- **Identity**: existing transaction identifier or integer `id`.
- **Attributes**: player association, amount/status, date, and import/provider metadata.
- **Relationships**: associated with one Player and, where applicable, attendance/payment state for a game.
- **Rules**: imports and payment mutations require protected access and regression coverage; sensitive payment data must not be logged.

### Application Setting

- **Identity**: setting key.
- **Attributes**: persisted value for notifications, payment configuration, or operational behavior.
- **Rules**: settings mutations require protected access and CSRF validation.

## New synchronization metadata

Offline synchronization may be represented client-side in IndexedDB or an equivalent browser store:

- `operation_id`: unique client-generated identifier.
- `entity_type`: `attendance` or `payment`.
- `entity_id`: target record identifier.
- `operation_type`: explicit update operation.
- `payload`: validated update values.
- `created_at`: client timestamp.
- `attempt_count`: retry count.
- `next_attempt_at`: backoff scheduling timestamp.
- `status`: queued, syncing, succeeded, conflict, or rejected.
- `server_version` / `client_version`: conflict comparison metadata where available.
- `error`: safe, user-displayable rejection reason without secrets.

Conflicts use latest successful update wins and create a visible warning for administrator review. Server-rejected items retry automatically with bounded exponential backoff and do not block unrelated queue items; the final implementation must define a safe retention/observability policy during implementation.

## Referential integrity

- All SQLite connections enable foreign keys.
- Migrations are numbered and repeatable.
- Delete and merge behavior for Game, Player, Attendance, Team Assignment, and Payment Transaction is explicit and tested before deployment.
