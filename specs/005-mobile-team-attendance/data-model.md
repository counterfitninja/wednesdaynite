# Data Model: Mobile Team and Attendance Management

## Existing Records

### Game

- Source table: `games`.
- Required reference for every assignment and attendance record.
- Mutations are rejected when the game is abandoned.

### Player

- Source table: `players`.
- Player identity is resolved by database ID, never by an untrusted display name.
- Existing skill-rating behavior must be reused. Null ratings use the current application default, verified by tests before implementation.

### Attendance

- Source table: `attendance`.
- One player/game record stores one status: `playing`, `maybe`, or `not_playing`.
- Attendance updates must preserve the existing payment fields and business rules.

### Team Assignment

- Source table: `team_assignments`.
- Invariant: at most one row exists for each `(game_id, player_id)`.
- `team_number` MUST be `1` or `2`.
- Unassigned players have no row for the game.
- A player not valid for the selected game cannot be assigned.

## Derived Values

For a game assignment draft:

- `team_1_count`: number of players assigned to Team 1.
- `team_2_count`: number of players assigned to Team 2.
- `team_1_skill_total`: sum of each Team 1 player's effective skill rating.
- `team_2_skill_total`: sum of each Team 2 player's effective skill rating.
- `balance_difference`: `abs(team_1_skill_total - team_2_skill_total)`.
- `unassigned_count`: eligible players with no team assignment.

Derived values are display data and must be recalculated from the submitted or persisted membership set; clients cannot set authoritative totals.

## Validation Rules

- A submitted player ID must be an existing eligible player ID.
- A player ID MUST NOT occur in both team lists.
- Duplicate IDs in a team list are rejected or normalized before persistence; tests must document the selected behavior.
- Team lists may omit eligible players, which means those players become unassigned.
- A swap requires two distinct player IDs, both currently assigned to different valid teams.
- Assignment and attendance writes for an abandoned game are rejected.
- Invalid input causes zero assignment/attendance writes for that request.