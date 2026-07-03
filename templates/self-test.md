# Self-Test

> 用途：发布或交付前的最小质量门禁。  
> 写入位置：`docs/changes/REQ-YYYY-NNN/self-test.md`

## Metadata

- Project:
- Change ID:
- Tested By:
- Date:
- Build / Commit:

## Normal Paths

主要成功路径。每条写“操作、期望结果、实际结果”。

| Case | Steps | Expected | Actual | Pass |
|---|---|---|---|---|

## Boundary Cases

边界、空值、极值、并发、重复提交、超长输入、缺省配置等。

| Case | Expected | Actual | Pass |
|---|---|---|---|

## Error Cases

依赖失败、权限失败、网络失败、数据缺失、脚本非零退出等。

| Case | Expected Failure Handling | Actual | Pass |
|---|---|---|---|

## Permission / Data Safety

- [ ] 未读取或复制无关 `.env`、token、数据库、session、日志、备份。
- [ ] 外发内容已确认可公开或已脱敏。
- [ ] 涉及删除、覆盖、迁移、生产部署时已明确授权。

## Regression Checks

这次改动可能影响哪些旧功能？列出已检查项。

- [ ] 

## Result

Pass / Blocked / Needs Fix
