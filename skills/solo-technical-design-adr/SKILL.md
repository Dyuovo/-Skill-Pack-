---
name: solo-technical-design-adr
description: Invoke when user designs architecture, database, API, or needs technical ADR. Produce technical designs and ADRs for solo-product changes. Use when a feature affects architecture, APIs, database schema, auth, files, jobs, environment variables, health/version endpoints, deployment, rollback, or operational risk. 适用于技术方案、ADR、数据库、接口、回滚设计.
---

# Solo Technical Design ADR

## Purpose

Turn product scope into a safe implementation approach before coding. Focus on decisions that would be expensive to discover during deployment.

## Inputs

- PRD or acceptance criteria.
- Existing repository and stack.
- Current deployment model.
- Known data, API, auth, file, job, or ops risks.

## Workflow

1. Inspect the existing codebase and deployment patterns before inventing new ones.
2. Identify impacted modules: frontend, backend, database, jobs, config, logs, monitoring, deployment.
3. Describe the proposed design and data flow.
4. Record meaningful alternatives and why they were rejected.
5. Specify DB migrations and compatibility strategy.
6. Specify environment variables and `.env.example` changes.
7. Specify `/health`, `/version`, logs, audit events, and monitoring changes.
8. Define release, verification, rollback, and data recovery considerations.
9. For Releasable products, produce an Architecture Hardening Review before Operable promotion.
10. Write an ADR when a decision changes architecture, storage, external dependencies, or operational behavior.

## Technical Design Template

```markdown
# Technical Design

## Current State

## Change Scope

## Proposed Design

## Frontend Changes

## Backend Changes

## API Changes

## Database Changes

## Environment Variables

## Health / Version / Logs / Monitoring

## Release Plan

## Rollback Plan

## Risks

## Open Questions
```

## ADR Template

```markdown
# ADR-00X <Title>

## Context

## Options

## Decision

## Rationale

## Consequences

## Rollback Conditions

## Decision Date
```

## Architecture Hardening Template

Save this review as `docs/changes/REQ-YYYY-NNN/architecture-hardening.md`. Each dimension must be checked with `[x] PASS` or `[x] N/A` and include evidence.

```markdown
## Review Evidence

## Search Scale

- [ ] PASS or N/A:
- Evidence:
- Follow-up:

## Sync Accuracy

- [ ] PASS or N/A:
- Evidence:
- Follow-up:

## Dependency Fallback

- [ ] PASS or N/A:
- Evidence:
- Follow-up:

## Migration

- [ ] PASS or N/A:
- Evidence:
- Follow-up:

## Config Consistency

- [ ] PASS or N/A:
- Evidence:
- Follow-up:

## Real Sample Verification

- [ ] PASS or N/A:
- Evidence:
- Follow-up:
```

## Quality Gate

Do not start risky implementation until the design names migrations, env vars, verification checks, and rollback limits. If there is no rollback path, say that explicitly.

For Architecture Hardening Review, do not mark the product Operable until `workflow_gate.py architecture-hardening` writes `Status: PASS`.

## Persistence

Save to:

```text
docs/changes/REQ-YYYY-NNN/technical-design.md
docs/changes/REQ-YYYY-NNN/architecture-hardening.md
docs/adr/ADR-00X-title.md
```
