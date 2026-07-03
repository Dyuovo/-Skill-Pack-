---
name: solo-mvp-scope-roadmap
description: Cut MVP scope and build a lightweight solo-project roadmap. Use when the user needs to decide what belongs in v0/v1, defer features, define milestones, create release slices, or plan weekly/biweekly delivery. 适用于 MVP 取舍、路线图、里程碑、版本切片.
---

# Solo MVP Scope Roadmap

## Purpose

Turn a broad product definition into a small, shippable sequence that a solo developer can actually finish.

## Inputs

- PRD or feature description.
- Constraints: time, skill, budget, dependencies.
- Must-have workflow.
- Risk areas: data, auth, payment, file upload, external APIs, deployment.

## Workflow

1. Identify the smallest user outcome that deserves shipping.
2. Split scope into `v0`, `v1`, `later`, and `never/not now`.
3. Keep v0 focused on one primary workflow.
4. Pull risk forward: unknown integrations, migrations, deploy changes, compliance, or data loss risk.
5. Create milestones at weekly or biweekly granularity.
6. Define a release decision: what evidence makes this version "good enough to observe."

## Scope Table

```markdown
| Item | v0 | v1 | Later | Note |
|---|---:|---:|---:|---|
|  |  |  |  |  |
```

## Roadmap Template

```markdown
# MVP Roadmap

## v0 Outcome

## v0 Scope

## Explicitly Deferred

## Milestones
| Milestone | Target | Exit Criteria |
|---|---|---|

## Release Slice

## Biggest Risks

## Next Skill
```

## Quality Gate

The MVP is too large if it requires more than one primary workflow, more than one risky integration, or more than one unclear user segment before any learning can happen.

## Persistence

Save to:

```text
docs/changes/REQ-YYYY-NNN/mvp-roadmap.md
```

