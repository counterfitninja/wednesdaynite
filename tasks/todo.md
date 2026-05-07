# Sticker Packet Feature

- [x] Add sticker player data model and image storage helpers.
- [x] Build routes to manage uploads and open a six-player packet.
- [x] Create the sticker packet page with upload form and reveal UI.
- [x] Link the feature from navigation/help text.
- [x] Run focused validation and note results.

## Review

- Added `/stickers` for uploads and album management, backed by a new `sticker_players` table.
- Added `/stickers/open` to generate a six-card packet with one guaranteed shiny and random stats.
- Validation: editor diagnostics clean for touched files; `python -m py_compile app.py` passed.

# Season Momentum Stat

- [x] Add reusable momentum calculator using last 8 weeks vs season win rate.
- [x] Add `/stats/momentum` route with leaderboard-style trend table and highlights.
- [x] Add a "Hot right now" stat card and row badge to main wins leaderboard.
- [x] Link momentum page from base nav and all stats quick-nav bars.
- [x] Run focused validation and note results.

## Review

- Added `build_momentum_table(...)` to compute season and recent form deltas for each player.
- Added `/stats/momentum` page with top hot/cooling highlights and per-player momentum table.
- Added leaderboard integration: top momentum card + `🔥 Hot` badge on players trending up.
- Validation: `python -m py_compile app.py` passed; editor diagnostics show no errors on touched files.