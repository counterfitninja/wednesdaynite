# Feature Specification: Wednesday Night FC Improvements

**Feature Branch**: `001-wnfc-improvements`

**Created**: 2026-09-17

**Status**: Draft

**Input**: Prioritized improvement backlog in `tasks/todo.md`.

## Clarifications

### Session 2026-09-17

- Q: Which authentication model should the application use for administrative workflows? → A: One shared administrator login using Flask sessions.
- Q: When a mobile attendance or payment update loses connectivity, what should the application do? → A: Queue the update locally and synchronize automatically when online.
- Q: How should conflicting offline updates be resolved when queued changes synchronize? → A: Latest successful update wins, with a visible conflict warning.
- Q: Which data should remain available offline for the PWA? → A: Cache all authenticated admin pages and data for offline use.
- Q: What should happen when a queued offline update cannot be synchronized because the server rejects it? → A: Automatically retry indefinitely without user notification.

## User Scenarios & Testing

### User Story 1 - Safe and Verifiable Administration (Priority: P1)

As an administrator, I need protected, observable, and tested administrative
workflows so attendance, payments, scores, imports, and player records cannot
be corrupted or exposed accidentally.

**Why this priority**: Security and data integrity are prerequisites for every
other improvement.

**Independent Test**: Exercise login, protected POST routes, representative
attendance/payment/game mutations, abandoned-game calculations, and health
checks using an isolated test database.

**Acceptance Scenarios**:

1. **Given** an unauthenticated request, **when** an admin route or mutation is
   requested, **then** access is denied or redirected without changing data.
2. **Given** a state-changing form without a valid CSRF token, **when** it is
   submitted, **then** the request is rejected.
3. **Given** valid attendance, score, payment, and abandoned-game data,
   **when** statistics are calculated, **then** the documented business rules
   are applied consistently.
4. **Given** a production-like request, **when** diagnostics are emitted,
   **then** secrets and password values are absent from logs.

### User Story 2 - Matchday Dashboard and Workflow (Priority: P1)

As a player or administrator, I need the next match and its key actions to be
obvious so I can record attendance, manage teams, handle payments, and enter
the result quickly from a phone.

**Why this priority**: This is the app's main recurring user journey and the
largest direct usability improvement.

**Independent Test**: Load the home page with an upcoming game and verify the
next-match summary, attendance/payment counts, quick actions, and navigation to
the game workflow on desktop and mobile widths.

**Acceptance Scenarios**:

1. **Given** an upcoming game exists, **when** the home page loads, **then** it
   presents the next game as the primary card with date, location, attendance,
   and clear actions.
2. **Given** an admin opens a game, **when** the detail page loads, **then**
   attendance, payments, teams, and result actions are clearly separated.
3. **Given** a mobile viewport, **when** the game detail page is used, **then**
   the match summary and primary actions remain visible and usable.

### User Story 3 - Consistent Responsive and Accessible UI (Priority: P2)

As a user on desktop or mobile, I need consistent navigation, readable layouts,
accessible controls, and clear status communication across the application.

**Why this priority**: Consistency reduces learning cost and makes the existing
feature set easier to use.

**Independent Test**: Review representative public, admin, stats, and team
pages at desktop and mobile widths using keyboard navigation and without relying
on color alone.

**Acceptance Scenarios**:

1. **Given** any primary page, **when** the shared navigation is opened,
   **then** links are grouped by Matchday, Stats, and Admin purpose.
2. **Given** a narrow viewport, **when** a data-heavy page loads, **then** key
   content is presented as readable cards or a usable responsive table.
3. **Given** keyboard navigation, **when** a user moves through controls,
   **then** focus is visible and all actions remain reachable.

### User Story 4 - Mobile Team and Attendance Management (Priority: P2)

As an administrator on matchday, I need touch-friendly team assignment and
attendance controls that do not depend on drag-and-drop or difficult
multi-select interactions.

**Why this priority**: Team assignment and attendance are frequent mobile tasks.

**Independent Test**: Manage a sample game from a mobile viewport using explicit
team movement and attendance controls, then verify saved assignments and counts.

**Acceptance Scenarios**:

1. **Given** players available for a game, **when** an admin assigns them on
   mobile, **then** players can be moved, unassigned, and optionally swapped
   without drag and drop.
2. **Given** teams with skill ratings, **when** assignments change, **then**
   player counts, skill totals, and balance difference update immediately.

### User Story 5 - Maintainable Platform and Reliable PWA (Priority: P3)

As a maintainer, I need separable domain code, explicit migrations, reliable
offline/cache behavior, and dependable notifications so the application is
safer to evolve and operate.

**Why this priority**: These changes reduce long-term risk after user-facing
workflows are stabilized.

**Independent Test**: Run the full regression suite, exercise migrations and
backup/restore documentation, inspect module boundaries, and validate service
worker updates without stale HTML after a deployment.

**Acceptance Scenarios**:

1. **Given** a schema change, **when** the application starts, **then** a
   versioned, repeatable migration applies without data loss.
2. **Given** a new deployment, **when** the service worker activates, **then**
   old caches are removed and HTML does not remain unexpectedly stale.
3. **Given** notifications are disabled or permission is absent, **when** the
   app runs, **then** it does not repeatedly prompt or fail noisily.

## Edge Cases

- No upcoming game exists, or the next game has no attendance yet.
- A game is abandoned after attendance, teams, payments, or scores were entered.
- A mobile user loses connectivity during an attendance or payment update.
- Offline attendance and payment updates are queued locally and synchronized automatically when connectivity returns; synchronization failures must remain visible for retry.
- When queued offline changes conflict with newer server data, the latest successful update wins and the application displays a visible conflict warning for administrator review.
- The PWA may cache all authenticated admin pages and data for offline use; cached data must be protected from unauthenticated access and cleared on logout or cache-version change.
- Server-rejected queued updates are retried automatically without user notification; the retry mechanism must avoid blocking other queued updates.
- A player is deleted or merged while historical assignments and payments exist.
- A service-worker cache contains assets from a previous application version.
- OCR or uploaded image processing receives an invalid, oversized, or malformed
  file.

## Requirements

### Functional Requirements

- **FR-001**: System MUST protect admin state changes with one shared
  administrator login using Flask session authentication and CSRF validation;
  individual administrator accounts are out of scope for this increment.
- **FR-002**: System MUST avoid logging passwords, secrets, tokens, or
  unnecessary personal data.
- **FR-003**: System MUST preserve and test attendance, payment, score, team,
  import, and abandoned-game rules.
- **FR-004**: System MUST provide focused regression tests and health/smoke
  validation for changed workflows.
- **FR-005**: System MUST present the next match, attendance, payment status,
  and primary actions on the home page.
- **FR-006**: System MUST provide clearly separated attendance, payments, teams,
  and result sections on game details.
- **FR-007**: System MUST provide responsive navigation and layouts for desktop
  and mobile viewports.
- **FR-008**: System MUST provide keyboard-accessible controls, visible focus,
  and non-color status indicators.
- **FR-009**: System MUST provide non-drag-and-drop controls for mobile team
  assignment.
- **FR-010**: System MUST support explicit, repeatable database migrations and
  reviewed foreign-key behavior.
- **FR-011**: System MUST manage service-worker cache versions and avoid
  unintentionally stale HTML.
- **FR-012**: System MUST isolate optional OCR/deployment-heavy dependencies
  when practical.

### Key Entities

- **Game**: A scheduled match with date, location, attendance, teams, scores,
  notes, and abandoned state.
- **Player**: A participant with identity, aliases, skill rating, attendance,
  and payment attributes.
- **Attendance**: A player's status and payment state for a game.
- **Team Assignment**: A player's saved team membership for a game.
- **Application Setting**: A persisted feature or operational setting such as
  notifications or payment configuration.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An administrator can reach the next game's attendance workflow
  from the home page in at most two interactions.
- **SC-002**: All covered state-changing routes reject missing or invalid CSRF
  tokens in automated tests.
- **SC-003**: Focused regression tests cover authentication, attendance,
  scores, payments, teams, imports, and abandoned-game calculations.
- **SC-004**: Primary home, game detail, admin games, leaderboard, and team pages
  remain usable at a 390px-wide viewport.
- **SC-005**: Keyboard-only review reaches every primary action and shows a
  visible focus indicator.
- **SC-006**: A service-worker version update removes prior caches and loads
  current HTML and static assets.

## Assumptions

- The existing Flask, SQLite, Jinja, and server-rendered architecture remains
  in place for this increment.
- Existing routes and database records remain backward-compatible unless a task
  explicitly documents a migration.
- The application is used primarily by a small football group, so heavyweight
  multi-tenant architecture is out of scope.
- Browser notifications may require a later server-side or Web Push
  implementation; this backlog includes the operational design work but does
  not assume a provider.
