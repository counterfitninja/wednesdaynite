# Feature Specification: Matchday Dashboard and Workflow

**Feature Branch**: `003-matchday-dashboard`

**Created**: 2026-09-17

**Status**: Draft

**Input**: User Story 2 from `specs/001-wnfc-improvements/spec.md`.

## User Scenarios & Testing

### User Story 1 - Matchday Dashboard and Workflow (Priority: P1)

As a player or administrator, I need the next match and its key actions to be obvious so I can record attendance, manage teams, handle payments, and enter the result quickly from a phone.

**Why this priority**: This is the app's main recurring user journey and the largest direct usability improvement.

**Independent Test**: Seed an upcoming game with representative attendance and payment records, load `/` and `/games/<id>` through the Flask test client, and review the rendered pages at desktop and 390px mobile widths. Verify the next-match summary, counts, quick actions, separated workflow sections, and safe empty/error states.

**Acceptance Scenarios**:

1. **Given** an upcoming game exists, **when** the home page loads, **then** it presents the next game as the primary card with date, location, attendance, payment status, and clear actions.
2. **Given** no upcoming game exists, **when** the home page loads, **then** it shows a useful empty state and a clear path to view or create a game without failing.
3. **Given** an admin opens a game, **when** the detail page loads, **then** Attendance, Payments, Teams, and Result actions are clearly separated.
4. **Given** a mobile viewport, **when** the game detail page is used, **then** the match summary and primary actions remain visible, touch-friendly, and usable without horizontal scrolling.
5. **Given** a game has no attendance, payment, team, or result data, **when** the relevant workflow section loads, **then** it communicates the empty state and next action clearly.
6. **Given** a matchday mutation succeeds or fails, **when** the next page is rendered, **then** the user receives clear success or error feedback without losing the workflow context.

## Edge Cases

- No upcoming game exists, or the next game has no attendance yet.
- The next game is abandoned or has an incomplete location/notes value.
- A game has attendance but no payment records, or payment-exempt players.
- A game has enough players for teams but no generated/manual team assignments.
- A result is incomplete, tied, or not entered yet.
- A mobile user has a narrow 390px viewport and long player/location names.
- A mutation redirect includes a stale, invalid, or missing flash message.

## Requirements

### Functional Requirements

- **FR-001**: The home page MUST identify the next upcoming non-abandoned game and present it as the primary matchday card.
- **FR-002**: The next-match card MUST show date, location, playing/maybe/not-playing attendance counts, and payment status/count when available.
- **FR-003**: The next-match card MUST provide clear primary actions for attendance, teams, result, leaderboard, and help, with actions appropriate to the user's role.
- **FR-004**: The game-detail page MUST separate Attendance, Payments, Teams, and Result workflows with clear headings and action hierarchy.
- **FR-005**: The game-detail page MUST provide a persistent or readily available mobile match summary and primary action area at 390px width.
- **FR-006**: Empty, abandoned, success, error, and loading states MUST be understandable without relying on color alone.
- **FR-007**: Existing attendance, payment, team, score, and abandoned-game rules MUST remain unchanged by presentation changes.
- **FR-008**: Matchday pages MUST avoid avoidable N+1 attendance/payment queries by using grouped or joined aggregates for summary data.
- **FR-009**: State-changing actions MUST continue to use the authentication and CSRF protections defined by `specs/002-safe-admin/`.
- **FR-010**: Primary matchday actions MUST be reachable from the home page in at most two interactions for an administrator.

## Key Entities

- **Game**: Scheduled match with date, location, notes, scores, and abandoned state.
- **Attendance Summary**: Counts of playing, maybe, not-playing, and payment-relevant players for a game.
- **Matchday Action**: Role-aware link or button to attendance, payments, teams, result, leaderboard, or help.
- **Workflow Feedback**: Safe success, error, empty, abandoned, or pending/loading message associated with a matchday action.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An administrator reaches the next game's attendance workflow from `/` in at most two interactions.
- **SC-002**: Automated rendering tests verify next-match date, location, attendance counts, payment status, and primary actions.
- **SC-003**: Automated rendering tests verify game-detail headings and links for Attendance, Payments, Teams, and Result.
- **SC-004**: Primary home and game-detail content remains usable at a 390px-wide viewport without horizontal scrolling.
- **SC-005**: Empty and abandoned states provide a clear next action and do not expose exceptions.
- **SC-006**: Focused tests demonstrate summary data uses bounded aggregate queries rather than per-player/per-section N+1 queries.

## Assumptions

- Flask, SQLite, Jinja, and the existing server-rendered architecture remain in place.
- The safe-administration security foundation is implemented or available before matchday state-changing UI work.
- Existing routes are reused where their behavior is correct; new routes are added only when needed to make a result or payment action clear.
- Desktop and mobile validation uses the existing UI with shared CSS moved incrementally into `static/app.css`.
