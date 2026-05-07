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