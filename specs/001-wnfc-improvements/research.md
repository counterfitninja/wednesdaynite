# Research: Wednesday Night FC Improvements

## Decision: Preserve the Flask, SQLite, Jinja architecture

- **Rationale**: The existing application is a single Flask module with server-rendered templates and a small-group operating model. Incremental extraction reduces regression risk while preserving route and data compatibility.
- **Alternatives considered**: A SPA rewrite or multi-tenant service split would add complexity without supporting the stated matchday goals.

## Decision: Use shared-password Flask sessions with application-level CSRF

- **Rationale**: The specification selects one shared administrator login. A small signed-token helper can protect HTML forms and same-origin AJAX without introducing a framework migration. Session cookies should be secure in production, HTTP-only, and SameSite=Lax.
- **Alternatives considered**: Individual accounts are out of scope; a third-party authentication provider is disproportionate for this increment.

## Decision: Add explicit, numbered SQLite migrations

- **Rationale**: Existing startup `ALTER TABLE` calls and broad exception handling can hide failures. A schema version table plus idempotent numbered migrations makes upgrades repeatable and testable. Every connection must enable `PRAGMA foreign_keys = ON`.
- **Alternatives considered**: A full ORM migration framework was rejected to avoid replacing the current parameterized SQLite access pattern.

## Decision: Use network-first HTML and versioned static caches

- **Rationale**: HTML must not remain stale after deployment. Static assets can use versioned caches, while authenticated navigation should require a valid session and logout must clear private caches. Cache activation must delete old versions.
- **Alternatives considered**: Cache-first navigation was rejected because it can expose stale authenticated pages and old HTML.

## Decision: Model offline writes as independent queue records

- **Rationale**: Attendance and payment updates need durable queue IDs, timestamps, operation payloads, retry metadata, and conflict metadata. Each item retries independently so one rejected operation cannot block the queue. Latest successful update wins and a visible conflict warning is recorded.
- **Alternatives considered**: Indefinite blind retries without backoff or observability are unsafe; implementation must include bounded exponential backoff, a retry state, and diagnostics while preserving the clarified automatic retry behavior.

## Decision: Keep OCR dependencies optional

- **Rationale**: Torch, TorchVision, and EasyOCR substantially increase deployment size and startup risk. Normal web startup should not import them unless OCR is requested.
- **Alternatives considered**: Keeping all dependencies in the default production install preserves convenience but increases operational cost and failure surface.

## Decision: Use pytest with isolated temporary SQLite databases

- **Rationale**: The feature requires focused regression coverage and the current app has no project-owned test suite. Fixtures must override the database path and avoid mutating `football.db`.
- **Alternatives considered**: Manual-only validation cannot reliably cover authentication, CSRF, migrations, and abandoned-game calculations.
