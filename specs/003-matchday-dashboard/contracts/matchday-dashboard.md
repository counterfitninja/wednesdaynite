# Matchday Dashboard Contract

## Home Page Summary

The home page must expose a view model containing:

- `next_game`: nearest actionable upcoming game, or an explicit empty value;
- date, location, notes, and abandoned status;
- playing, maybe, and not-playing counts;
- chargeable, paid, and unpaid payment counts when available;
- role-aware action targets for attendance, teams, result, leaderboard, and help.

Summary counts must come from bounded aggregate queries rather than one query per player or card.

## Game Detail Sections

The game detail page must render identifiable sections with headings or landmarks for:

- Attendance: record and review attendance;
- Payments: review payment status and perform permitted payment actions;
- Teams: generate, view, or edit teams when applicable;
- Result: view or enter scores when applicable.

Unavailable actions for abandoned games or anonymous users must be explained rather than silently omitted when that would make the workflow ambiguous.

## Feedback

Success, error, empty, abandoned, and pending/loading feedback must be rendered in a consistent, accessible container. Feedback must not expose exception text, secrets, or database details.
