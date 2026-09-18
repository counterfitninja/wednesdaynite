# Safe Administration Quickstart

## Prerequisites

- Python 3.10+ and dependencies installed from `requirements.txt`.
- Test secret and admin credential configured by the test fixture.
- No production database is required; tests create isolated temporary SQLite files.

## Automated validation

From the repository root, run `pytest`. The suite must verify:

1. Anonymous access to `/admin`, `/admin/games`, and representative mutation
	routes redirects or returns 403 without changing rows.
2. Missing, invalid, expired, and cross-session CSRF tokens are rejected before
	writes; a valid form token and AJAX header token succeed.
3. Attendance, payment, score, team, import, upload, merge/delete, and
	abandoned-game rules preserve expected historical behavior.
4. Invalid, oversized, malformed, and unsupported uploads leave no unsafe file
	and preserve an existing valid replacement target.
5. Import failures roll back and return generic messages.
6. Captured logs contain no passwords, secrets, tokens, cookies, contact data,
	or raw exception text.
7. 403, 404, 500, `/healthz`, and `/status` responses are safe, with database
	failure represented by a stable non-sensitive degraded response.

## Manual/smoke validation

1. Submit a valid CSRF-protected admin form and verify the intended data change.
2. Open the login page with a malicious external `next` URL and verify login
	lands on the safe admin page rather than the external host.
3. Exercise a representative matchday flow: attendance, payment, teams, score,
	then abandoned-game behavior.
4. Run `python -m py_compile app.py` and `git diff --check`.

See `contracts/security-behavior.md` for response and request contracts and
`data-model.md` for persistence and relationship invariants.
