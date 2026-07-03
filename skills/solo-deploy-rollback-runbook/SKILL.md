---
name: solo-deploy-rollback-runbook
description: Plan and execute safe solo-product deployment and rollback runbooks. Use when deploying or preparing to deploy a web app with releases/current/shared, systemd, Nginx, Docker Compose, PM2, health checks, version verification, backups, audit records, or rollback triggers. 适用于部署、上线验证、回滚、发布记录.
---

# Solo Deploy Rollback Runbook

## Purpose

Make deployment verifiable and reversible. A command succeeding is not a successful release; assertions passing is a successful release.

## Default Server Model

```text
/srv/apps/<app>/
  releases/
  current -> releases/<release>
  previous -> releases/<previous>
  shared/
    .env
    uploads/
    logs/
    backups/
    tmp/
  audit/
    deployments/
    rollbacks/
    checks/
  locks/
```

## Deployment Workflow

1. Confirm host, app root, operator, and target release.
2. Acquire deploy lock.
3. Record current release and version.
4. Verify artifact checksum.
5. Confirm artifact does not include real `.env`.
6. Back up `.env`, database, and other critical state.
7. Create new release directory.
8. Extract artifact and link shared files/directories.
9. Run migration only if the plan says to.
10. Update `previous`, then atomically switch `current`.
11. Restart exactly one process manager: systemd, Docker Compose, or PM2.
12. Verify:
    - service active/healthy/online.
    - PID exists.
    - process cwd points to new release/current.
    - `/version` matches expected SHA/release.
    - `/health/ready` passes.
    - core smoke flow passes.
    - logs show no sustained ERROR/FATAL.
13. Write deployment record.

## Rollback Triggers

Default to rollback when:

- `/health/ready` fails repeatedly.
- `/version.git_sha` is not the expected SHA.
- process cwd points to the old release or unknown path.
- core smoke flow fails.
- errors rise quickly after release.
- migration or config breaks core read/write paths.
- duplicate process managers, ports, or app directories appear and cannot be stabilized quickly.

## Deployment Record Template

```markdown
# Deployment Record

## Basic Info
- App:
- Environment:
- Time:
- Operator:
- Version:
- Git SHA:
- Release ID:

## Before
- Current release:
- PID:
- Port:
- Process manager:

## Steps
| Step | Command / Action | Result | Evidence |
|---|---|---|---|

## Verification
- [ ] current points to new release
- [ ] PID cwd correct
- [ ] /version matches
- [ ] /health/ready passes
- [ ] Smoke passes
- [ ] Logs acceptable

## Result
success / rollback / failed
```

## Quality Gate

Do not declare success until version, health, cwd, smoke, and logs have been checked. If any check is skipped, record why.

