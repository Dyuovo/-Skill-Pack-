---
name: solo-self-test-quality-gate
description: Invoke when user needs testing, quality checks, or release readiness verification. Create and run self-test quality gates for solo-product changes. Use before release readiness to cover normal flows, boundary values, error states, permissions, regression, migration, env vars, health/version checks, and smoke tests. 适用于自测清单、质量门禁、回归测试.
---

# Solo Self Test Quality Gate

## Purpose

Make "I tested it" concrete enough to trust. The output should prove the change is ready for release or clearly say why not.

## Workflow

1. Start from acceptance criteria.
2. Cover four required classes:
   - normal flow.
   - boundary values.
   - exception/error flow.
   - permission flow.
3. Add release-risk checks for migrations, env vars, files, jobs, external services, and health endpoints.
4. Add at least one positive data-path test that proves the core workflow works with non-empty fixture data.
5. For API + UI products, verify the frontend request payload matches the backend route contract.
6. For Python projects, run `py -3 -m pytest -q` or explicitly place smoke scripts outside `tests/test_*.py` when they are not pytest tests.
7. For search/index products, test real hit behavior; for Chinese/chat products, include Chinese/domain text search.
8. Record test data, environment, Git SHA, exact commands, and result.
9. Mark blocking failures separately from follow-up improvements.

## Self-Test Template

```markdown
# Self-Test

## Basic Info
- Feature:
- Branch:
- Git SHA:
- Tester:
- Time:

## Normal Flow
- [ ] 
- [ ] Positive fixture/data path returns a non-empty expected result
- [ ] Primary workflow completes end to end

## Boundary Cases
- [ ] Empty / null
- [ ] Minimum / maximum
- [ ] Long input
- [ ] Special characters
- [ ] Duplicate submit

## Error States
- [ ] Invalid params
- [ ] Missing data
- [ ] Dependency failure
- [ ] Database failure
- [ ] Upload/job failure

## Permissions
- [ ] Anonymous
- [ ] Normal user
- [ ] Admin/operator
- [ ] Cross-tenant or other-user data

## Contract Checks
- [ ] UI request body/query/path matches backend API signature
- [ ] Response fields used by UI exist and have expected types
- [ ] Secrets or keys are not sent in query strings, logs, or browser history

## Domain Checks
- [ ] Domain-language search/tokenization works when relevant
- [ ] Chinese/CJK text search works when relevant
- [ ] External/local data-source failure has a clear user-visible result

## Automated Commands
```text
<exact command>
<summary output>
```
- [ ] `py -3 -m pytest -q` passes, or non-pytest smoke script is intentionally outside `tests/test_*.py`

## Release Checks
- [ ] Migration handled
- [ ] `.env.example` handled
- [ ] `/version` handled
- [ ] `/health` handled
- [ ] Logs checked
- [ ] Backup and restore verified
- [ ] SQLite WAL/checkpoint or backup API verified when relevant

## Result
pass / blocked / needs-fix
```

## Quality Gate

The change cannot move to release preparation if normal flow, a positive non-empty data path, a meaningful error path, contract compatibility, and permissions were not checked.

Do not count a pure empty-database smoke test as release evidence for a search/index/data product.

Do not place a standalone script with top-level HTTP calls and `sys.exit()` under `tests/test_*.py`; pytest will import it and fail collection. Put it under `scripts/smoke_test.py`, or rewrite it as real pytest tests.

## Persistence

Save to:

```text
docs/changes/REQ-YYYY-NNN/self-test.md
```
