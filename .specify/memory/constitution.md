<!--
Sync Impact Report
- Version change: template/unversioned -> 1.0.0
- Modified principles: placeholder principles -> five project principles below
- Added sections: Security and operational constraints; Development workflow and quality gates
- Removed sections: none
- Follow-up TODO: confirm the original ratification date
-->

# Wednesday Night FC Constitution

## Core Principles

### I. Matchday Value First
Every feature MUST improve a real weekly football workflow or provide a clearly
useful historical insight. The primary path for attendance, team selection,
payments, and results MUST remain understandable on a phone and usable with
minimal navigation. Nice-to-have features MUST NOT obscure the next match or
the actions needed to run it.

### II. Data Integrity Over Convenience
Attendance, teams, scores, payments, and player identities MUST have explicit,
consistent rules. Historical games MUST NOT be silently changed by presentation
logic. Abandoned games MUST remain distinguishable from played games and MUST
be excluded from statistics wherever the product rules require it. Destructive
operations MUST provide confirmation and a recoverable path where practical.

### III. Secure by Default
Administrative actions MUST require authenticated access and MUST protect
state-changing requests against cross-site request forgery. Credentials,
session secrets, tokens, and personal player data MUST NOT be written to logs.
Production deployments MUST use configured secrets rather than development
fallbacks, and uploaded files MUST be validated, size-limited, and safely
processed.

### IV. Tested, Observable, and Verifiable
Every change that affects calculations, persistence, authentication, imports,
or user workflows MUST include focused regression coverage. Changes MUST be
validated with the narrowest useful automated checks plus a production-relevant
smoke test when runtime behavior is affected. Failures MUST be diagnosable via
structured logs and health checks without exposing sensitive data.

### V. Simple, Accessible, and Maintainable
The simplest design that satisfies the requirement MUST be preferred over
framework or abstraction-heavy solutions. Shared UI patterns MUST be reused
rather than recreated with template-specific inline styling. Interfaces MUST
support keyboard navigation, visible focus, readable contrast, responsive
layouts, and information that is not conveyed by color alone. Code MUST be
organized so domain logic can be tested independently from HTTP and rendering.

## Security and Operational Constraints

- The application MUST continue to support the documented Flask, SQLite, and
	server-rendered template architecture unless a feature specification justifies
	a change.
- SQLite foreign-key behavior, migrations, and deletion semantics MUST be
	explicit and tested before schema changes are deployed.
- Production configuration MUST define a strong `SECRET_KEY` and
	`ADMIN_PASSWORD` or an equivalent secure authentication mechanism.
- Backups MUST be taken before risky data or schema operations, and restore
	procedures MUST be documented and periodically verified.
- Dependencies MUST be kept to the smallest practical production set; optional
	OCR dependencies SHOULD be isolated when they materially affect deployment
	size or startup time.

## Development Workflow and Quality Gates

- Non-trivial work MUST begin with a written specification or implementation
	plan that identifies affected routes, templates, data rules, and risks.
- Implementation tasks MUST be ordered by dependency and MUST identify their
	validation steps.
- A change MUST NOT be considered complete until focused tests, syntax checks,
	editor diagnostics, and `git diff --check` pass as applicable.
- UI changes MUST be checked at both desktop and mobile widths, including the
	primary matchday workflow and relevant empty, error, and loading states.
- Documentation MUST be updated when routes, workflows, configuration,
	deployment behavior, or user-facing terminology changes.
- Reviews MUST check constitution compliance, data integrity, security impact,
	accessibility, and whether the implementation introduces unnecessary
	complexity.

## Governance

This constitution governs feature specifications, plans, tasks, implementation,
and reviews for Wednesday Night FC. When another document conflicts with it,
the conflict MUST be resolved in favor of this constitution unless the
constitution is formally amended first.

Amendments MUST document the reason for change, affected principles, migration
or compatibility impact, and updated validation expectations. Amendments use
Semantic Versioning: MAJOR for incompatible governance changes or principle
removals, MINOR for new or materially expanded principles, and PATCH for
clarifications that do not change obligations. Every amendment MUST update the
version and last-amended date and MUST include a temporary sync impact report
for review.

Compliance MUST be reviewed during planning and before completion. Any
intentional exception MUST be recorded in the relevant plan or specification,
including its rationale, scope, owner, and an expiry or review condition.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): confirm original adoption date | **Last Amended**: 2026-09-17
