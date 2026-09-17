# Contract: Mobile Team and Attendance Management

## Manual Team Save

`POST /games/<game_id>/teams/manual`

- Authentication: administrator required.
- CSRF: valid token required.
- Content type: form encoded.
- Fields:
  - `team1_players`: zero or more player IDs.
  - `team2_players`: zero or more player IDs.
- Semantics: the submitted lists replace the game's current assignments; omitted eligible players become unassigned.
- Validation: game must exist and not be abandoned; IDs must be eligible; IDs cannot overlap; `team_number` is only `1` or `2`.
- Success: one transactional save, redirect to the manual team page, accessible success feedback.
- Failure: zero partial writes, redirect or render with accessible error feedback.

## Explicit Move

`POST /games/<game_id>/teams/move`

- Authentication: administrator required.
- CSRF: valid token required.
- Fields: `player_id`, `destination` where destination is `team1`, `team2`, or `unassigned`.
- Success: player has exactly the requested membership after the transaction.
- Failure: zero writes and an accessible error message.

## Explicit Swap

`POST /games/<game_id>/teams/swap`

- Authentication: administrator required.
- CSRF: valid token required.
- Fields: `player_a_id`, `player_b_id`.
- Validation: IDs are distinct and both players are assigned to different teams in the game.
- Success: assignments exchange team numbers in one transaction.
- Failure: zero writes and an accessible error message.

## Attendance Update

`POST /games/<game_id>/attendance`

- Authentication: administrator required for administrative editing.
- CSRF: valid token required.
- Fields: `player_id`, `status` (`playing`, `maybe`, or `not_playing`), and existing supported payment fields.
- Success: the player's attendance status is persisted and the page shows updated counts.
- Failure: zero partial writes and accessible feedback.