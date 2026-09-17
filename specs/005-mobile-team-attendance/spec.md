# Feature Specification: Mobile Team and Attendance Management

**Feature Branch**: `005-mobile-team-attendance`

**Created**: 2026-09-17

**Status**: Draft

**Input**: User Story 4 from `specs/001-wnfc-improvements/spec.md`.

## User Scenarios & Testing

### User Story 1 - Mobile Team and Attendance Management (Priority: P2)

As an administrator on matchday, I need touch-friendly team assignment and attendance controls that do not depend on drag-and-drop or difficult multi-select interactions.

**Why this priority**: Team assignment and attendance are frequent matchday tasks and must remain practical on a phone.

**Independent Test**: Seed a game with playing, maybe, and not-playing players plus skill ratings. At a 390px viewport, use explicit controls to assign, move, unassign, and optionally swap players; save the result; reload the page; and verify assignments, attendance states, counts, skill totals, and balance difference.

**Acceptance Scenarios**:

1. **Given** players are available for a game, **when** an administrator opens manual team management on mobile, **then** each player has an explicit accessible action to assign them to Team 1, Team 2, or Unassigned without drag-and-drop.
2. **Given** a player is assigned to a team, **when** the administrator chooses another destination, **then** the player moves or is unassigned without duplicate saved assignments.
3. **Given** two assigned players, **when** the administrator requests a swap, **then** their team memberships are exchanged and the proposed result is visible before saving or is safely persisted according to the workflow design.
4. **Given** teams have skill-rated players, **when** an assignment changes, **then** player counts, skill totals, and balance difference update immediately and are also correct after reload.
5. **Given** a mobile administrator edits attendance, **when** a player is marked Playing, Maybe, or Not Playing, **then** the control is touch-friendly, clearly labeled, and the saved state is reflected in the counts.
6. **Given** a save fails or the session expires, **when** the page returns, **then** the user receives an accessible error message and the unsaved or invalid state is not presented as successfully saved.

## Edge Cases

- A game has fewer than two playing players or no eligible players.
- A player is already assigned to the selected destination.
- A player appears in both submitted team lists or in neither list.
- A swap targets the same player, an unassigned player, or players from the same team.
- A player is deleted or merged while the assignment form is open.
- A skill rating is null, outside the expected range, or changed between render and save.
- The mobile viewport is 390px wide and player names or locations are long.
- JavaScript is disabled or a client-side request fails.
- A game is abandoned while the team or attendance page is open.
- A CSRF token is missing or invalid on a state-changing request.

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide explicit non-drag-and-drop controls to assign a player to Team 1, Team 2, or Unassigned.
- **FR-002**: System MUST provide an explicit move operation that results in at most one saved team assignment per player per game.
- **FR-003**: System MUST support an optional explicit swap operation with validation for distinct players and valid team membership.
- **FR-004**: System MUST show team player counts, skill totals, and absolute balance difference after each client-side assignment change.
- **FR-005**: System MUST calculate and persist team assignments using the existing game/player rules and preserve historical records.
- **FR-006**: System MUST provide touch-friendly attendance controls for Playing, Maybe, and Not Playing without requiring multi-select.
- **FR-007**: System MUST update attendance counts and payment-related summaries consistently after attendance changes.
- **FR-008**: System MUST reject unauthenticated, invalid-CSRF, invalid-player, duplicate, and abandoned-game mutations without partial writes.
- **FR-009**: System MUST remain usable at a 390px viewport without requiring horizontal scrolling or drag-and-drop.
- **FR-010**: System MUST remain usable with JavaScript disabled through server-rendered forms and native controls.
- **FR-011**: System MUST expose save, error, and recovery feedback through accessible text associated with the relevant workflow.

### Key Entities

- **Team Assignment**: A unique `(game_id, player_id)` membership with a `team_number` of `1` or `2`.
- **Assignment Draft**: Client-visible proposed team membership used to update counts and totals before persistence.
- **Team Balance Summary**: Counts, skill totals, and absolute difference for Team 1 and Team 2.
- **Attendance Status**: One of `playing`, `maybe`, or `not_playing` for a player/game pair.
- **Attendance Control**: An explicit accessible control that sets one attendance status.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An administrator can assign, move, unassign, and swap players at 390px width without drag-and-drop.
- **SC-002**: Reloading after a successful save shows no duplicate assignments and the intended team membership for every submitted player.
- **SC-003**: Automated tests verify counts, skill totals, and absolute balance difference after assignment changes and after reload.
- **SC-004**: Automated tests verify Playing, Maybe, and Not Playing controls persist and produce correct counts.
- **SC-005**: Invalid, unauthorized, CSRF-invalid, and abandoned-game mutations produce zero partial writes.
- **SC-006**: The workflow remains usable with JavaScript disabled and communicates save/error states with readable accessible text.

## Assumptions

- Flask, SQLite, Jinja, and the existing server-rendered architecture remain in place.
- Existing authentication and CSRF protections from `specs/002-safe-admin/` are available and remain authoritative.
- Existing team assignment rows use `team_number` values `1` and `2`; unassigned means no row exists.
- A null skill rating uses the application's existing default rating for balance calculations; the implementation must verify the current rule before changing it.
- This increment does not change team-balancing algorithms or payment business rules.