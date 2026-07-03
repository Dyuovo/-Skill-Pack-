---
name: solo-requirement-to-acceptance
description: Translate product requirements into buildable acceptance criteria and task-ready slices. Use when the user has a PRD, feature request, bug, or maintenance item and needs user stories, Given/When/Then criteria, edge cases, permissions, and release notes for implementation. 适用于需求拆成验收标准.
---

# Solo Requirement To Acceptance

## Purpose

Make a requirement precise enough that implementation and self-test can proceed without guessing.

## Inputs

- PRD, issue, bug report, or user story.
- Known user roles.
- Critical workflows.
- Data objects and side effects.

## Workflow

1. Extract actors, triggers, inputs, outputs, and state changes.
2. Write acceptance criteria in observable terms.
3. Include normal, edge, exception, and permission paths.
4. Identify data changes, background jobs, files, notifications, and logs.
5. Mark release-sensitive requirements: env vars, migrations, health checks, external dependencies.
6. Hand off to technical design or task breakdown.

## Acceptance Template

```markdown
# Acceptance Criteria

## Story
As a <user>, I want <capability>, so that <outcome>.

## Normal Flow
- Given ...
- When ...
- Then ...

## Edge Cases
- Given ...
- When ...
- Then ...

## Error States

## Permissions

## Data / Logging / Audit

## Release Implications
- [ ] DB migration
- [ ] Environment variable
- [ ] Background job
- [ ] File upload/storage
- [ ] External service
- [ ] Health/version impact

## Next Skill
```

## Quality Gate

Acceptance criteria must be testable by a human or automated test. Rewrite vague phrases like "works well", "fast", or "user-friendly" into visible behavior.

