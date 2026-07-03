---
name: solo-ops-observability-backup
description: Set up low-cost observability, logs, backups, and early operations for solo products. Use after or before launch to define health checks, /version, Sentry, Prometheus, external HTTP monitoring, journalctl/log review, backup cadence, restore verification, disk/port checks, and observation period. 适用于监控、日志、备份、上线观察.
---

# Solo Ops Observability Backup

## Purpose

Give a solo project enough operational visibility to notice failure, diagnose quickly, and recover without heavyweight infrastructure.

## Minimum Observability Stack

| Area | Minimum |
|---|---|
| Liveness | `/health/live` |
| Readiness | `/health/ready` |
| Version | `/version` with version, git SHA, release ID |
| Process | systemd / Docker Compose / PM2 status |
| Logs | journald, app logs, Nginx logs |
| Errors | Sentry or equivalent |
| External check | HTTP uptime check |
| Disk | `df -h` |
| Port | `ss -lntp` |
| Database | `select 1` and backup age |
| Cron/jobs | heartbeat or Sentry Crons |

## Workflow

1. Identify critical user flows and dependencies.
2. Define live, ready, and version endpoint behavior.
3. Define log locations and commands.
4. Define backup objects: database, `.env`, uploads, configs, release artifacts.
5. Define backup cadence and retention.
6. Define restore verification:
   - `pg_restore --list` or equivalent.
   - sample file restore for uploads.
   - checksum for config backups.
7. Create an observation checklist for the first 24-72 hours after launch.

## Backup Table

```markdown
| Object | Frequency | Retention | Verification |
|---|---|---|---|
| Database | daily | 7-14 days | restore/list check |
| .env/config | before change | last 10 | checksum |
| Uploads | daily/weekly | depends on size | sample restore |
| Release artifact | each release | last 10 | SHA256 |
```

## Quality Gate

Before calling a product "launched", the operator must know where logs are, how to check health, where backups are, and how to prove a backup is usable.

## Persistence

Save to:

```text
docs/ops/monitoring.md
docs/ops/backup.md
docs/changes/REQ-YYYY-NNN/observation-log.md
```

