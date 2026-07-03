# Product Engineering Workflow

## 0. 进入条件

满足任一条件时使用：

- 项目缺少清晰 PRD、任务、测试、发布或运维记录。
- 用户想把想法推进为可交付项目。
- 需要审查四 Agent 架构或其他项目的结构缺口。
- 需要把零散讨论沉淀为可复用项目资产。

## 1. 扫描

读取：

- README / AGENTS / 架构文档
- `docs/`
- 配置样例与环境变量说明
- 测试与发布脚本
- 运维、备份、监控、回滚记录

输出：

- 当前架构
- 缺口清单
- 风险边界
- 建议下一步

## 2. 初始化变更

在目标项目内创建或复用：

```text
docs/changes/current.md
docs/changes/REQ-YYYY-NNN/
```

原则：

- 一个 active change 只放一类改造主题。
- 不混入无关聊天和长期记忆。
- 不把敏感数据写入碎片。

## 3. 产出最小工件

按需要生成：

| 阶段 | 输出 |
|---|---|
| 想法 | `idea-intake.md` |
| 产品定义 | `prd.md` |
| 范围 | `mvp-roadmap.md` |
| 验收 | `acceptance.md` |
| 技术设计 | `technical-design.md` / ADR |
| 执行 | `task-list.md` |
| 自测 | `self-test.md` |
| 发布 | `release-plan.md` |
| 部署 | `deployment-record.md` |
| 回滚 | `rollback-record.md` |
| 观察 | `observation-log.md` |

ADR 推荐放在：

```text
docs/adr/ADR-NNN-short-title.md
```

可从 `templates/adr-000.md` 复制后改编号。

## 4. 进入小枢治理

只有以下内容进入 AI_SYSTEM：

- 经验证的长期规则
- 可重复使用 3 次以上的 Skill
- 跨 Agent 或跨日任务
- 系统级风险和架构改良建议

## 5. 小电学习转化

小电可把本工作流转成：

- AI PM 方法论课程素材
- PRD / ADR / 验收标准练习
- Agent 架构设计题
- 作品集案例复盘

小电只负责理解、教学、练习和反馈，不直接改治理层。

## 6. 测试升级路径

当前 Skill 状态为 `testing`。首个端到端候选优先选择：

```text
AI_SYSTEM/02_XIAOTING/POWER_MARKET_AGENT/
```

升为 `active` 前，至少完成一次真实项目闭环：

```text
project.scan -> change.init -> prd.build -> adr.build -> self-test -> release/check or rollback record -> review
```
