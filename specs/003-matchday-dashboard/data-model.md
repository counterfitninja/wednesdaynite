# Data Model: Matchday Dashboard and Workflow

## Game

Existing `games` rows provide the scheduled match date, location, notes, scores, and abandoned state. The dashboard must select the nearest actionable upcoming game without changing historical records or treating an abandoned game as actionable.

## Attendance Summary

A derived, read-only view model for one game:

- `playing_count`: attendance rows with `status = 'playing'`;
- `maybe_count`: attendance rows with `status = 'maybe'`;
- `not_playing_count`: attendance rows with `status = 'not_playing'`;
- payment counts derived from playing players, excluding `payment_exempt` players from chargeable totals.

Summary fields are presentation data only and must not replace persisted attendance or payment rules.

## Matchday Action

A role-aware action contains a label, destination, availability state, and optional explanation. Actions include attendance, payments, teams, result, leaderboard, and help. Anonymous users receive public/read-only destinations; administrators receive protected mutation destinations.

## Workflow Feedback

A safe message with a category such as success, error, empty, abandoned, or pending. It may include a next action but must not contain exception text, secrets, tokens, filesystem paths, or sensitive database details.
