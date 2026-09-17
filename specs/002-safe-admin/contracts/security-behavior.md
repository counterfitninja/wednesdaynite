# Security Behavior Contract

## Protected Requests

- Anonymous requests to administrative pages and state-changing routes must redirect to `/login` or return `403`.
- Rejected requests must not mutate game, player, attendance, payment, team, import, upload, or settings records.

## CSRF

- Every covered state-changing form emits a session-bound hidden token.
- Covered POST requests without a valid token are rejected with a safe client response before mutation.
- Valid tokens permit the intended mutation and preserve existing route behavior.

## Login Redirect

- A local relative `next` target may be honored after successful login.
- Absolute or scheme-relative external targets must resolve to the safe admin landing page.

## Errors and Health

- 403, 404, and 500 responses use safe templates or bodies without stack traces, filesystem paths, secrets, or database exception details.
- `/healthz` returns a stable health status without credentials or raw dependency errors.

## Uploads and Logs

- Unsupported, malformed, or oversized uploads are rejected before processing/storage.
- Structured logs contain event metadata only and never passwords, secret values, CSRF tokens, session cookies, or unnecessary personal data.
