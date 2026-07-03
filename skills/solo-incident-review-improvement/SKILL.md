---
name: solo-incident-review-improvement
description: Run blameless incident and near-miss reviews for solo-product operations. Use after failed deploys, rollbacks, outages, data issues, missed backups, monitoring gaps, production surprises, or any event that should improve runbooks, tests, scripts, or checklists. 适用于事故复盘、回滚后复盘、流程改进.
---

# Solo Incident Review Improvement

## Purpose

Convert failures and near misses into better safeguards. For solo projects, the review must produce specific changes to tests, scripts, runbooks, monitoring, or scope decisions.

## Workflow

1. Record facts before analysis.
2. Build a timeline.
3. State impact in user, data, revenue, or operator terms.
4. Identify detection method.
5. Separate direct cause from systemic cause.
6. Ask why pre-release checks or monitoring did not catch it.
7. Decide recovery path: rollback, fix-forward, config change, data repair.
8. Create action items that update artifacts, not memory.
9. Update the relevant checklist or script.

## Incident Template

```markdown
# Incident Review

## Summary

## Impact

## Detection

## Timeline
| Time | Event |
|---|---|

## Direct Cause

## Systemic Cause

## Why Existing Checks Missed It

## Response Actions

## Recovery Result

## Improvements
| Action | Owner | Due | Artifact Updated |
|---|---|---|---|

## Follow-Up Verification
```

## Quality Gate

An incident review is not complete until at least one durable artifact is updated or the decision is made that no change is justified.

## Persistence

Save to:

```text
docs/incidents/INC-YYYY-NNN.md
```

