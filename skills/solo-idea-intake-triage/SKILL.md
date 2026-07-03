---
name: solo-idea-intake-triage
description: Capture and triage solo-product ideas. Use when the user has a rough idea, many possible projects, unclear priority, or asks whether an idea should enter discovery, MVP planning, backlog, parking, or rejection. 适用于 idea 收集、项目池入口、是否值得做、下一步判断.
---

# Solo Idea Intake Triage

## Purpose

Turn a fuzzy idea into a clear intake decision without prematurely writing a PRD or building code.

## Inputs

- Idea statement or rough product concept.
- Target user or operator, if known.
- Trigger or pain point.
- Current constraints: time, skills, money, existing repo, deadlines.
- Evidence available: user request, personal pain, market signal, competitor, incident, revenue clue.

## Workflow

1. Restate the idea in one sentence: "For [user], solve [problem] by [approach]."
2. Classify the idea type: MVP, maintenance, experiment, automation, content/tooling, or learning project.
3. Identify the strongest reason to continue and the strongest reason to stop.
4. Score the idea from 1-5 on value, urgency, strategic fit, feasibility, and cost.
5. Decide one of five outcomes:
   - `discover`: problem is interesting but evidence is thin.
   - `define`: problem and user are clear enough for PRD.
   - `build-small`: scope is tiny and low-risk.
   - `park`: not now, but keep in backlog.
   - `reject`: not worth tracking.
6. Write the next action as a concrete verb phrase.

## Checklist

- [ ] User or operator named.
- [ ] Pain, job, or trigger named.
- [ ] Desired outcome named.
- [ ] Constraint named.
- [ ] Decision recorded.
- [ ] Next skill selected.

## Output Template

```markdown
# Idea Intake

## Idea

## User / Operator

## Problem Signal

## Classification

## Scores
| Factor | Score | Note |
|---|---:|---|
| Value |  |  |
| Urgency |  |  |
| Strategic fit |  |  |
| Feasibility |  |  |
| Cost |  |  |

## Decision
discover / define / build-small / park / reject

## Next Action

## Next Skill
```

## Persistence

Save accepted or parked ideas to:

```text
docs/projects/idea-ledger.md
```

If the idea becomes an active change, create:

```text
docs/changes/REQ-YYYY-NNN/idea-intake.md
```

## Quality Gate

Do not promote an idea to PRD unless the user, problem, success signal, and next action are clear enough to explain in under one minute.

