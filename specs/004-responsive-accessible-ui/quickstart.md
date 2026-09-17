# Quickstart: Responsive and Accessible UI

## Automated checks

1. Run `pytest tests/test_ui_rendering.py`.
2. Confirm representative routes render with Matchday, Stats, and Admin navigation groups.
3. Confirm anonymous users do not receive admin mutation links.
4. Confirm status, empty, success, and error content includes readable text or semantic labels.

## Desktop review

1. Open `/`, `/games/<id>`, `/admin/games`, `/leaderboard`, and `/teams/manual` at a desktop width.
2. Confirm the shared header, navigation groups, page header, main content, and footer are consistent.
3. Tab through the page and verify every primary action has a visible focus indicator.
4. Confirm status and team meanings remain understandable when color is ignored.

## Mobile review at 390px

1. Set the viewport to 390px wide.
2. Open the same representative pages.
3. Open and close navigation using the keyboard and touch; confirm the control has an accessible name and state.
4. Confirm primary content, actions, long labels, tables/cards, and feedback do not require unintended horizontal scrolling.
5. Verify empty and error states remain readable and actionable.

## Regression checks

1. Run `python -m py_compile app.py`.
2. Run the focused UI tests and the existing regression suite.
3. Run `git diff --check`.
4. Confirm authentication, CSRF, attendance, payment, team, score, import, and abandoned-game workflows remain unchanged.
