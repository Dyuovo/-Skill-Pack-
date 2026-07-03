---
name: solo-task-breakdown-kanban
description: Break solo-product work into tasks and a lightweight kanban flow. Use when a PRD or technical design needs execution tasks, issue templates, dependencies, estimates, weekly board columns, blockers, or ready/done definitions. 适用于任务拆解、看板、周计划、阻塞管理.
---

# Solo Task Breakdown Kanban

## Purpose

Turn scope and technical design into small executable tasks that can move through a solo workflow without losing status.

## Workflow

1. Split by user-visible flow, data change, integration, operation, and test need.
2. Keep each task small enough to finish or make visible progress in one focused work block.
3. Add acceptance criteria or a done signal to each task.
4. Mark dependencies and blockers.
5. Place tasks into the board:
   - Backlog
   - This Week
   - Doing
   - Blocked
   - Review/Test
   - Ready to Deploy
   - Observing
   - Done
6. Enforce WIP: keep `Doing` to 1-2 items.

## Task Template

```markdown
# Task: <Title>

## Background

## Goal

## Scope

## Inputs / Outputs

## Acceptance

## Risk

## Dependencies

## Branch

## Estimate

## Linked Milestone
```

## Quality Gate

A task is not ready if "done" cannot be checked without asking the original author what they meant.

## Persistence

Save to:

```text
docs/changes/REQ-YYYY-NNN/task-list.md
docs/projects/weekly-kanban.md
```

