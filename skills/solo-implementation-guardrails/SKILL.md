---
name: solo-implementation-guardrails
description: Invoke when writing/modifying any code. Apply implementation guardrails for solo-product changes. Use while coding or reviewing a feature to ensure migrations, env examples, health/version endpoints, logs, tests, secrets, deployment assumptions, and rollback constraints are handled before release. 适用于开发守门、上线前代码安全检查.
---

# Solo Implementation Guardrails

## Purpose

Keep implementation aligned with release safety. This skill is especially useful when the user is building alone and may forget operational details.

## Workflow

1. Inspect the codebase and follow existing conventions.
2. Implement only the scoped change unless a supporting change is required.
3. Check data changes:
   - migration exists.
   - migration is additive or compatibility is explained.
   - already-run migrations are not rewritten.
4. Check configuration:
   - `.env.example` updated.
   - no real `.env`, secrets, backups, logs, or uploads are added to Git.
5. Check operational endpoints:
   - `/health/live` or equivalent exists when relevant.
   - `/health/ready` checks dependencies when relevant.
   - `/version` exposes version, git SHA, or release ID when relevant.
6. Check logs and audit:
   - errors are visible.
   - key state changes are traceable.
   - sensitive data is not logged.
7. Check tests and self-test notes.
8. Check API/UI contracts when both exist: frontend payload shape must match backend parameters, and response fields used by UI must exist.
9. Check search/index behavior with positive non-empty fixture data; for Chinese/chat products, verify Chinese text search or explicitly document why exact-token search is acceptable.
10. Check secrets handling: keys and tokens must not travel in query strings, logs, URLs, or browser history.
11. Check backup behavior for SQLite WAL or similar multi-file persistence; use checkpoint or the database backup API instead of copying only the main file when the service can be live.
12. When the intent is `architecture-hardening`, check Search Scale, Sync Accuracy, Dependency Fallback, Migration, Config Consistency, and Real Sample Verification, then update `docs/changes/REQ-YYYY-NNN/architecture-hardening.md`.
13. Update the change folder with implementation notes when useful.

## Guardrail Checklist

```markdown
# Implementation Guardrails

- [ ] Existing patterns inspected
- [ ] Scope respected
- [ ] Migration created or not needed
- [ ] Migration compatibility considered
- [ ] `.env.example` updated or not needed
- [ ] No secrets committed
- [ ] Health/version endpoints updated or not needed
- [ ] Logs/audit added for risky flows
- [ ] Tests/self-test updated
- [ ] Positive non-empty data path tested
- [ ] API/UI contract checked
- [ ] Search/tokenization behavior checked when relevant
- [ ] Secrets are not passed through URLs or logs
- [ ] SQLite WAL/live backup behavior checked when relevant
- [ ] Architecture hardening dimensions checked when intent is `architecture-hardening`
- [ ] Release and rollback impact known
```

## Quality Gate

Do not mark implementation done if a production operator could not answer: what changed, how to verify it, and how to reverse or contain it.
