# ⚽ Wednesday Night FC Tracker

Simple Flask app for managing weekly casual football games:
- track attendance
- generate/manual teams
- record scores
- view win + attendance leaderboards
- mark matches as abandoned (excluded from stats)

## Tech Stack
- Python + Flask
- SQLite (local file DB)
- Server-rendered HTML templates (Jinja)
- Optional Gunicorn for deployment

## Prerequisites
- Python 3.10+ (recommended)
- `pip`
- PowerShell (for Windows setup commands below)

## Project Layout
- `app.py` — main Flask app, routes, DB init/migrations
- `templates/` — HTML pages
- `static/` — service worker, manifest, client JS
- `requirements.txt` — Python dependencies
- `Procfile` — deployment entry (`gunicorn app:app`)

## Project Docs
- [CHANGELOG.md](CHANGELOG.md) — tracked release history and notable changes
- [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) — pre-release and post-deploy verification steps
- [HOW_IT_WORKS.md](HOW_IT_WORKS.md) — plain-English walkthrough of weekly app flow

## Local Setup (Windows / PowerShell)
1. Open terminal in project root.
2. Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Set environment variables (recommended):

```powershell
$env:ADMIN_PASSWORD = "choose-a-strong-password"
$env:SECRET_KEY = "choose-a-strong-secret-key"
```

5. Run app:

```powershell
python app.py
```

App runs on `http://localhost:5000` by default.

## Running in Production Mode (Local Test)
If you want to run closer to deployment behavior:

```powershell
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:5000
```

## Environment Variables
- `ADMIN_PASSWORD` — admin login password.
	- If missing locally, app falls back to default password (`football2026`).
	- In Azure, this **must** be set.
- `SECRET_KEY` — Flask session signing key.
	- Set this in all real environments.
- `WEBSITE_INSTANCE_ID` — set automatically by Azure (used for environment detection).

## Configuration Notes
- `HOST` and `PORT` are currently defined in `app.py` (`0.0.0.0:5000`).
- Admin session/auth uses Flask `session` with `SECRET_KEY`.
- Notifications toggle is stored in the `settings` table (`notifications_enabled`).

## Database Notes
- Local DB file: `football.db`.
- In Azure: DB path is `/home/football.db`.
- Schema is initialized and lightweight migrations run automatically on app startup.

### Core Tables
- `players` — player profiles and skill rating
- `games` — game metadata, scores, abandoned flag
- `attendance` — per-game player status
- `team_assignments` — generated/manual team splits
- `settings` — app-level toggles

## Key Features
- Auto-creates the next Wednesday game (9pm cadence logic in `index`).
- Attendance statuses: `playing`, `maybe`, `not_playing`.
- Team generation + manual team assignment.
- Score tracking for team 1/team 2.
- **Abandoned match support**:
	- Can be toggled in admin.
	- Scores are cleared when abandoned.
	- Excluded from attendance and win stats.
	- Final-score shortcut skips abandoned games.

## Admin Workflows
### Match day flow
1. Open game from `/admin/games`.
2. Record attendance (bulk or individual).
3. Generate teams or set manual teams.
4. After match, edit score.
5. If cancelled/stopped, mark game abandoned.

### Player management flow
1. Add/edit players in `/admin/players`.
2. Use merge if duplicates exist.
3. Keep aliases consistent for imports.

### Import flow
1. Use `/import` to upload CSV.
2. Confirm date/location before import.
3. Review imported game and clean up player names if needed.

## Useful Routes
- `/` — games list
- `/login` — admin login
- `/admin/games` — manage games
- `/admin/players` — manage players + attendance stats
- `/admin/settings` — notifications toggle
- `/leaderboard` — wins + attendance leaderboards
- `/import` — CSV import page
- `/healthz` or `/status` — health/version check

## Data Backup & Restore
### Backup (recommended before major admin changes)
- Stop the app (or ensure no active writes).
- Copy `football.db` to a safe location with date in filename.

### Restore
- Replace `football.db` with backup copy.
- Restart app so fresh connections read restored DB.

## Deployment
`Procfile` is set for Gunicorn:

```text
web: gunicorn app:app
```

If deploying with Gunicorn, ensure it is installed in the environment.

### Azure Notes
- App detects Azure using `WEBSITE_INSTANCE_ID`.
- In Azure, DB is stored under `/home/football.db` for persistence.
- In Azure, `ADMIN_PASSWORD` must be set or app startup will fail.

## First 5 Minutes (Quick Onboarding)
1. Open `http://localhost:5000`.
2. Click **Admin Login** and sign in.
	- If you did not set `ADMIN_PASSWORD`, use the local fallback: `football2026`.
3. Go to **Admin → Players** and add your regular players.
4. Go to **Admin → Manage Games** and confirm the next Wednesday game exists (auto-created), or add one manually.
5. Open a game with **Manage** and record attendance:
	- quick paste names in bulk, or
	- add individual status (`playing`, `maybe`, `not_playing`).
6. When enough players are marked `playing`, generate teams from the game page.
7. After the match, edit the game and enter scores (or mark as abandoned if it was cancelled/stopped).
8. Check **Leaderboard** to verify wins and attendance stats updated.

## Troubleshooting
- **App won’t start, password error in Azure:** set `ADMIN_PASSWORD` env var.
- **Session/login issues:** set a stable `SECRET_KEY`.
- **Port already in use:** change `PORT` in `app.py` or stop conflicting process.
- **`gunicorn` not found:** install it in the active environment (`pip install gunicorn`).
- **Template changes not visible:** hard refresh browser / restart app.
- **Stats look wrong after cancellation:** verify match is marked abandoned in admin.

## Maintenance
- Keep migrations additive in `init_db()`.
- Avoid destructive schema changes on live DB without backup.
- Prefer soft status changes (e.g., abandoned) over deleting historical games.
- Review and rotate admin credentials periodically.

## Good Practice Checklist
- Set `ADMIN_PASSWORD` and `SECRET_KEY` in every non-local environment.
- Back up `football.db` before major data/admin changes.
- Keep `app.py` migrations additive (new columns via guarded `ALTER TABLE`).
- Use the abandoned flag instead of deleting historically relevant cancelled matches.

## Future Improvements (Optional)
- Add automated tests for leaderboard and attendance calculations.
- Add structured logging for admin actions.
- Add export endpoint for backups from UI.
