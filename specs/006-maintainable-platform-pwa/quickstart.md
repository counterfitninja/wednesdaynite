# Quickstart: Maintainable Platform and Reliable PWA

## Automated validation

1. Run migration repeatability, foreign-key, backup/restore, module-boundary, PWA, notification, and optional-OCR tests.
2. Start the application with the base dependency profile and verify non-OCR routes import and respond.
3. Apply migrations to a copy of an existing database twice; verify one record per version and unchanged representative records.
4. Restore a backup into an isolated target and verify schema, migration state, expected tables, and representative records before replacing anything.
5. Run the full regression suite and `python -m py_compile` for changed Python modules.

## Service-worker review

1. Install release cache version N and confirm the application shell loads.
2. Deploy/test version N+1 with changed HTML and assets.
3. Activate the new worker and verify caches for N are deleted.
4. Request a navigation while online and confirm current HTML is returned rather than stale cached HTML.
5. Request a navigation offline and confirm the current cached shell/offline fallback is readable.

## Notification review

1. Load the application with notifications disabled and verify no permission prompt occurs.
2. Load in an unsupported or denied-permission browser state and verify no unhandled error or repeated retry occurs.
3. Trigger the explicit opt-in control and verify permission is requested at most once according to stored preference state.
4. Make the settings endpoint unavailable or malformed and verify the client fails quietly with recoverable UI feedback.

## Operational checks

1. Follow the backup, restore, verification, and rollback procedure in `README.md` and `RELEASE_CHECKLIST.md`.
2. Install only `requirements.txt`; verify OCR routes show the documented unavailable response.
3. Install `requirements-ocr.txt`; verify OCR functionality remains isolated from ordinary startup.
4. Run `git diff --check` and review route compatibility against the parent feature regression suite.
