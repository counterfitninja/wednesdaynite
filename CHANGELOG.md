# Changelog

All notable changes to this project should be documented in this file.

This project loosely follows Keep a Changelog format and Semantic Versioning principles.

## [Unreleased]
### Changed
- Attendance percentage now uses `playing / responded` games (responses with any status), excluding abandoned matches.
- Leaderboard attendance calculations are year-based and use the same responded-games denominator.

## [2026-02-19.1] - Sortable Leaderboards Patch
### Added
- Client-side sortable columns for Win Leaderboard (`Player`, `Wins`, `Draws`, `Losses`, `Games`, `Win %`).
- Client-side sortable columns for Attendance Leaderboard (`Player`, `Games Played`, `Attendance %`).

### Changed
- Rank display (medals / `#n`) now recalculates after sorting in both leaderboard tables.

## [2026-02-19] - Core Update: Abandoned Matches + Docs + Repo Hygiene
### Added
- New game state: abandoned.
- Admin controls to mark/restore abandoned games.
- Admin filter by game status.
- Expanded project documentation for setup, operations, troubleshooting, and maintenance.
- Added `RELEASE_CHECKLIST.md` and `CHANGELOG.md`.
- Added `.gitignore` rules for local runtime artifacts.

### Changed
- Stats calculations now ignore abandoned games.
- README now aligned with real app architecture and workflows.
- Final-score shortcut now skips abandoned matches.

### Fixed
- Documentation mismatch (old Node/React content replaced with Flask app docs).
- Stopped tracking local `football.db` and `.cache` files in git.

---

## How to use this file
- Keep new work under `[Unreleased]` while developing.
- On release, move items into a dated section like `[YYYY-MM-DD]`.
- Keep entries concise and user-impact focused.
- Group entries under: `Added`, `Changed`, `Fixed`, `Removed`, `Security` as applicable.
