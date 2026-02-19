# Release Checklist

Use this checklist before shipping updates to another machine or to Azure.

## 1) Code + Docs
- [ ] Confirm scope is complete and no unrelated edits are included.
- [ ] Update [CHANGELOG.md](CHANGELOG.md) under `Unreleased`.
- [ ] Update [README.md](README.md) if setup, behavior, or routes changed.

## 2) Local Validation
- [ ] App starts locally (`python app.py`).
- [ ] Login works with configured `ADMIN_PASSWORD`.
- [ ] Core pages load: `/`, `/admin/games`, `/admin/players`, `/leaderboard`.
- [ ] Health endpoint returns OK: `/healthz` or `/status`.

## 3) Feature Smoke Tests
- [ ] Add/edit player works.
- [ ] Add/edit game works.
- [ ] Attendance (single + bulk) works.
- [ ] Team generation/manual teams works.
- [ ] Score entry updates leaderboard as expected.

## 4) Abandoned Match Checks
- [ ] Marking a game abandoned works.
- [ ] Abandoned game scores are cleared.
- [ ] Abandoned games are excluded from attendance and win stats.
- [ ] Final-score quick link targets next non-abandoned game.
- [ ] Admin filter (`All / Active / Abandoned`) works.

## 5) Data Safety
- [ ] Backup `football.db` before release/deploy.
- [ ] Avoid destructive schema changes.
- [ ] New DB changes are additive migrations in `init_db()`.

## 6) Environment + Secrets
- [ ] `SECRET_KEY` is set in target environment.
- [ ] `ADMIN_PASSWORD` is set in target environment (required in Azure).
- [ ] Python dependencies are installed from `requirements.txt`.
- [ ] If using Gunicorn, confirm it is installed.

## 7) Azure Deploy Readiness (if applicable)
- [ ] `Procfile` entry is valid (`web: gunicorn app:app`).
- [ ] Confirm DB persistence path behavior (`/home/football.db`).
- [ ] Restart app and verify first-run migration succeeds.

## 8) Post-Deploy Verification
- [ ] Open app and verify login/session behavior.
- [ ] Create a test game/player and remove if needed.
- [ ] Check leaderboard and players stats still compute correctly.
- [ ] Confirm no obvious errors in logs.

## 9) Release Notes
- [ ] Move completed `Unreleased` items into a dated section in [CHANGELOG.md](CHANGELOG.md).
- [ ] Tag or otherwise record release identifier/date.
