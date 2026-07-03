---
name: solo-product-definition-prd
description: Create lean PRDs for solo and small-team products. Use when the user needs to turn a researched idea into goals, non-goals, users, scenarios, scope, acceptance criteria, risks, metrics, and a buildable product definition. 适用于 PRD、产品定义、需求说明、验收口径.
---

# Solo Product Definition PRD

## Purpose

Convert a validated or plausible idea into a lightweight PRD that is clear enough to design, build, test, and release.

## Inputs

- Idea intake or discovery notes.
- Target user and scenario.
- Desired outcome.
- Constraints and timeline.
- Existing repo, product, or operational context.

## Workflow

1. Define the user, scenario, and trigger.
2. State the problem and why now.
3. Name goals and non-goals.
4. Define inputs, outputs, and core user flow.
5. Specify acceptance criteria using observable behavior.
6. Capture risks, dependencies, and assumptions.
7. Identify metrics or proof of success.
8. Decide whether the next step is MVP scoping, technical design, or rejection.

## PRD Template

```markdown
# PRD: <Feature / Product>

## Background

## User And Scenario

## Problem

## Goals

## Non-Goals

## Scope

## User Flow

## Inputs And Outputs

## Acceptance Criteria
- [ ] 

## Metrics / Success Signals

## Risks And Dependencies

## Open Questions

## Next Skill
```

## Quality Gate

Do not move to technical design until the PRD makes it clear what is not being built. Missing non-goals are a common source of solo-project sprawl.

## Persistence

Save to:

```text
docs/changes/REQ-YYYY-NNN/prd.md
```

If the work is exploratory, save a shorter version to:

```text
docs/experiments/EXP-YYYY-NNN/prd.md
```

