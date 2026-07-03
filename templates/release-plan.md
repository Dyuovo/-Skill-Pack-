# Release Plan

> 用途：发布前确认版本、制品、验证和回滚路径。  
> 写入位置：`docs/changes/REQ-YYYY-NNN/release-plan.md`

## Version

- Version:
- Date:
- Owner:
- Target:

## Changes

本次发布包含什么，不包含什么。

- Included:
- Excluded:

## Build

| Artifact | Command / Source | Checksum / Evidence |
|---|---|---|

## Verification

- [ ] Self-test completed.
- [ ] Health check or equivalent verification completed.
- [ ] Logs checked.
- [ ] Rollback path confirmed.

## Deploy

部署步骤和验证断言。命令退出成功不等于部署成功，必须写验证结果。

| Step | Command / Action | Expected Verification |
|---|---|---|

## Rollback

触发回滚的条件和回滚步骤。

| Trigger | Rollback Action | Verification |
|---|---|---|
