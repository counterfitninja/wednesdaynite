# How This App Works (Simple Guide)

This app helps you run weekly Wednesday football games:
- add/manage players
- record attendance
- create teams
- save scores
- track wins and attendance over time

---

## 1) What each page is for

- `/` (Home): Shows recent games. Also auto-creates the next Wednesday game if missing.
- `/login`: Admin login page.
- `/admin/games`: Main game management page.
- `/games/<id>`: Game details page (attendance + team actions).
- `/games/<id>/teams`: View or generate balanced teams.
- `/games/<id>/teams/manual`: Manually drag/split teams.
- `/admin/players`: Manage players and view attendance percentages.
- `/players`: Public player list (name-only, no admin actions).
- `/leaderboard`: Win/loss/draw leaderboard + attendance leaderboard.
- `/import`: Import attendance from CSV.
- `/admin/settings`: Toggle notifications setting.

---

## 2) Weekly routine (recommended order)

Use this every week to avoid getting lost:

1. **Go to Admin Games** (`/admin/games`) and open the current game.
2. **Record attendance** on the game page:
   - Quick paste player names (bulk), or
   - Add individual player status (`playing`, `maybe`, `not_playing`).
3. **Generate teams** when enough players are marked `playing`:
   - Auto balanced teams (`/games/<id>/teams`), or
   - Manual teams (`/games/<id>/teams/manual`).
4. **After the match**, edit the game (`/games/<id>/edit`) and set the score.
5. **If the game was cancelled/stopped**, mark it **abandoned** instead of entering scores.
6. **Check `/leaderboard`** to confirm wins/attendance updated.

---

## 3) Core concepts (important)

### A) Game statuses that matter

- A game can be **normal** or **abandoned**.
- Abandoned games are excluded from win and attendance stats.
- If a game is marked abandoned, scores are cleared automatically.

### B) Attendance statuses

Each player can be marked as:
- `playing`
- `maybe`
- `not_playing`

Only `playing` counts as attendance for percentage stats.

### C) How attendance % is calculated

Attendance uses this denominator:
- all **past** games
- that are **not abandoned**

Formula:

`attendance % = (player playing count / total past non-abandoned games) * 100`

So if someone didn’t play in one counted game, they won’t be 100%.

### D) Teams and leaderboard logic

- Team generator uses players marked `playing` and balances by `skill_rating`.
- Wins/losses/draws come from saved team assignments + final scores.
- Leaderboard is filtered to the **current year**.

---

## 4) First-time setup checklist

1. Add players in `/admin/players`.
2. Confirm next game exists in `/admin/games` (home page usually auto-creates Wednesday).
3. Open game details and record attendance.
4. Generate teams.
5. Enter final score after playing.

---

## 5) Safe admin habits

- Prefer marking games **abandoned** over deleting historical data.
- Avoid deleting players unless necessary (it removes related attendance records).
- Use player aliases carefully for CSV import matching.
- Back up `football.db` before major edits/imports.

---

## 6) Quick troubleshooting

- **Can’t access admin pages**: Log in at `/login`.
- **Teams button not working**: Need at least 2 players marked `playing`.
- **Stats look wrong**: Check if a game is accidentally marked abandoned.
- **Attendance seems low**: Remember denominator is all past non-abandoned games.
- **Import didn’t map names**: Check player name/alias consistency.

---

## 7) Fast "where do I click?" map

- Manage this week: `/admin/games` → open game → attendance/teams
- Enter result: `/games/<id>/edit`
- View season standings: `/leaderboard`
- Fix player records: `/admin/players`
- Bulk historical import: `/import`

---

If helpful, I can also create a **one-page “matchday cheat sheet”** version with only 8–10 steps and no technical detail.