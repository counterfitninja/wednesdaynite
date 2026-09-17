# Contract: Maintainable Platform and Reliable PWA

## Startup and Migrations

- Application startup invokes the migration runner before serving requests.
- Pending migrations execute in ascending version order.
- Applied migration versions are recorded once in `schema_migrations`.
- A failed migration returns a startup failure with an actionable safe error; it does not claim success or discard data.

## Backup and Restore

- Backup operation produces a copy/export with migration version metadata.
- Restore is performed only against a selected target database or isolated copy.
- Verification reports schema readability, migration state, expected tables, and representative record counts.
- Existing source data is never overwritten until verification succeeds.

## Service Worker

- Cache names include a release version.
- `activate` deletes caches not belonging to the current version and calls `clients.claim()`.
- Navigation requests prefer current network HTML; if unavailable, the worker returns the cached current shell/offline fallback.
- Static assets may use the current versioned cache with network fallback.

## Notifications

- Page load does not call `Notification.requestPermission()`.
- An explicit user action starts permission flow only when settings allow notifications.
- `unsupported`, `default`, `denied`, disabled settings, malformed settings responses, and registration failures are handled without unhandled exceptions or retry loops.

## Optional OCR

- Non-OCR application imports do not require OCR-only packages.
- OCR service returns a typed unavailable/error result when optional dependencies are absent.
- UI presents a safe actionable message without a traceback or dependency path.

## Compatibility

- Existing public/admin route paths, accepted methods, response statuses, redirects, and core data rules remain unchanged unless separately documented.
