# Changelog

All notable changes to this project should be documented in this file.

This project loosely follows Keep a Changelog format and Semantic Versioning principles.

## [Unreleased]
### Added
- Added abandoned match support (`is_abandoned`) with admin toggle.
- Added admin game status filter (`All / Active / Abandoned`).
- Rewrote and expanded project README for accurate setup and operations.
- Added operational docs: release checklist and changelog.
- Added client-side sortable columns for wins and attendance leaderboard tables.

### Changed
- Excluded abandoned games from leaderboard and attendance statistics.
- Final-score shortcut now skips abandoned matches.

### Fixed
- Documentation mismatch (old Node/React content replaced with Flask app docs).

## [2026-02-19] - Docs + Abandoned Matches
### Added
- New game state: abandoned.
- Admin controls to mark/restore abandoned games.
- Admin filter by game status.

### Changed
- Stats calculations now ignore abandoned games.
- README now aligned with real app architecture and workflows.

---

## How to use this file
- Keep new work under `[Unreleased]` while developing.
- On release, move items into a dated section like `[YYYY-MM-DD]`.
- Keep entries concise and user-impact focused.
- Group entries under: `Added`, `Changed`, `Fixed`, `Removed`, `Security` as applicable.
