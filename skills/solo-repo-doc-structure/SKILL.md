---
name: solo-repo-doc-structure
description: Set up or repair lightweight repo documentation for solo-product delivery. Use when a project needs README structure, docs/changes folders, PRD/design/test/release templates, ops runbooks, ADRs, incident records, or a consistent artifact layout. 适用于仓库文档结构、模板、运行手册.
---

# Solo Repo Doc Structure

## Purpose

Create a durable place for the minimum artifacts that make solo projects understandable, releasable, and recoverable.

## Recommended Structure

```text
docs/
  projects/
    project-ledger.md
    roadmap.md
    weekly-kanban.md
  changes/
    REQ-YYYY-NNN/
      idea-intake.md
      prd.md
      mvp-roadmap.md
      acceptance.md
      technical-design.md
      task-list.md
      self-test.md
      release-plan.md
      deployment-record.md
      rollback-record.md
      observation-log.md
  adr/
    ADR-00X-title.md
  ops/
    runbook.md
    deploy.md
    rollback.md
    backup.md
    monitoring.md
  incidents/
    INC-YYYY-NNN.md
  reviews/
    weekly/
    monthly/
```

## Workflow

1. Inspect the repository before adding structure.
2. Reuse existing conventions when they are coherent.
3. Add only directories that will be used soon.
4. Create a change folder for active work.
5. Keep templates short and executable.
6. Link artifacts from the README or project ledger.

## README Sections

Use these sections when the repo lacks a useful README:

```markdown
# <Project>

## Purpose

## Current Status

## Local Development

## Environment Variables

## Test

## Build

## Release And Deploy

## Operations

## Project Docs
```

## Quality Gate

Do not create documentation that no workflow will update. A stale template is worse than no template because it creates false confidence.

