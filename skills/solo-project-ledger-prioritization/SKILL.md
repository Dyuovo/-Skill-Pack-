---
name: solo-project-ledger-prioritization
description: Maintain a solo-product project ledger, priorities, WIP limits, milestones, and decisions. Use when the user manages multiple projects, experiments, maintenance tasks, or needs a single truth source for status and next actions. 适用于项目台账、优先级、WIP、周/月路线.
---

# Solo Project Ledger Prioritization

## Purpose

Keep multiple solo projects from turning into attention debt. The ledger should make status, priority, risk, owner, repo, server, and next action visible.

## Workflow

1. Inventory active, parked, maintenance, and experiment work.
2. Normalize each item into a ledger row.
3. Score value, urgency, strategic fit, feasibility, and cost from 1-5.
4. Calculate priority:

```text
priority_total = value*0.30 + urgency*0.20 + strategy*0.25 + feasibility*0.25 - cost*0.20
```

5. Apply WIP limits:
   - 1 main build project.
   - 1 maintained production project.
   - 1 low-intensity experiment.
6. Set the next action as a concrete verb phrase.
7. Mark decision: continue, pause, park, archive, or kill.

## Ledger Fields

```csv
project_id,name,type,stage,status,priority,value_score,urgency_score,strategy_score,feasibility_score,cost_score,priority_total,owner,repo,prod_url,server,service_name,current_version,next_milestone,start_date,target_date,last_update,next_action,blocker,decision
```

## Stage Values

Use:

```text
Idea / Discovery / Definition / Design / Dev / Test / Ready / Deploying / Observing / Operate / Paused / Archived
```

## Quality Gate

A project without a next action is not active. Move it to parked or paused rather than letting it silently consume attention.

## Persistence

Save or update:

```text
docs/projects/project-ledger.md
docs/projects/roadmap.md
docs/projects/weekly-kanban.md
```

