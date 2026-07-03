# Solo Product Engineering Skills — AI_SYSTEM 集成索引

版本：v0.2.0
状态：active（已从 Joey 提供的 integrated package 完整导入）
最后更新：2026-06-25
源：`solo-product-engineering-skills-integrated.zip`（Joey 通过飞书发送）

## 三层架构

```
入口层：solo-product-engineering-operator（自动检测→路由→调度）
    ↓
工具层（18 个）：产品阶段(7) + 工程阶段(6) + 运营阶段(5)
    ↓
持久层：solo-fragment-collector（scripts 已部署到 08_TOOLS/）
```

## 20 个 Skill 目录

### 总控入口

| # | Skill | 触发时机 | 所属阶段 |
|---|-------|---------|---------|
| 1 | `solo-product-engineering-operator` | 每次产品/工程对话自动 | 入口层 |

### 产品阶段（想法→定义）

| # | Skill | 触发信号 | 输出 |
|---|-------|---------|------|
| 2 | `solo-idea-intake-triage` | 我想做、要不要、评估 | 打分+分类 pursue/park/reject |
| 3 | `solo-problem-discovery-research` | 调研、用户、竞品、验证 | 风险假设→证据→决策 |
| 4 | `solo-product-definition-prd` | PRD、需求、目标、范围 | PRD.md |
| 5 | `solo-mvp-scope-roadmap` | MVP、版本、v0/v1 | 版本切片+里程碑 |
| 6 | `solo-project-ledger-prioritization` | 台账、多项目、优先级 | 台账+加权优先级+WIP |
| 7 | `solo-requirement-to-acceptance` | 验收、Given/When/Then | 可测验收标准 |
| 8 | `solo-repo-doc-structure` | README、文档、仓库结构 | 标准文档目录 |

### 工程阶段（设计→发布）

| # | Skill | 触发信号 | 输出 |
|---|-------|---------|------|
| 9 | `solo-technical-design-adr` | 架构、API、DB、部署 | 技术方案+ADR |
| 10 | `solo-task-breakdown-kanban` | TODO、分工、排期 | Backlog→Review→Done |
| 11 | `solo-implementation-guardrails` | 任何代码变更自动触发 | 6项护栏检查（migration/env/密钥/健康/日志/测试）|
| 12 | `solo-self-test-quality-gate` | 测一下、边界、异常 | 四类自测清单+发布前检查 |
| 13 | `solo-release-artifact-builder` | 发布、版本号、checksum | RELEASE.json+SHA256 |
| 14 | `solo-deploy-rollback-runbook` | 部署、上线、回滚 | 13步部署+7种回滚触发 |

### 运营阶段（运行→成长）

| # | Skill | 触发信号 | 输出 |
|---|-------|---------|------|
| 15 | `solo-ops-observability-backup` | 运维、监控、日志、备份 | 最低可观测栈 |
| 16 | `solo-incident-review-improvement` | 挂了、报错、500 | 时间线→根因→改进 |
| 17 | `solo-weekly-monthly-review-coach` | 这周、进度、总结 | 周/月复盘 |
| 18 | `solo-pm-dev-growth-roadmap` | 想学、怎么提升 | 6个月成长路线 |
| 19 | `solo-portfolio-case-study-builder` | 做完了、上线了 | 作品案例 |
| 20 | `solo-fragment-collector` | 全程自动 | 碎片读写+合并历史 |

## AI_SYSTEM 内的 Agent 归属

| Agent | 拥有/使用 Skill | 说明 |
|-------|----------------|------|
| **小枢**（治理层）| 全部 20 个 Skill 的主入口 | 产品工程模式（testing→active）时作为总控，operator 自动检测信号→路由 |
| **小电**（学习）| #18 solo-pm-dev-growth-roadmap + PRD/ADR 理解 | 学习产品工程方法论，成长路线 |
| **小霆**（业务）| #13-16 部署/运维/运维相关 | POWER_MARKET_AGENT 项目的发布和运维 |
| **小衡** | 不直接使用 | 与产品工程无关 |

## 确定性脚本

已部署到 `08_TOOLS/product_engineering/`：

| 脚本 | 功能 | 用法 |
|------|------|------|
| `fragment_store.py` | 8阶段碎片初始化/写入/读取/合并/diff | `python3 08_TOOLS/product_engineering/fragment_store.py init/capture/status/read/consolidate/diff` |
| `product_state_store.py` | Product State 管理（init/brief/set/add/capture/decision/gap/promote-maturity/reconcile）| `python3 08_TOOLS/product_engineering/product_state_store.py ...` |
| `workflow_gate.py` | 实现门禁/发布门禁/架构加固检查 | `python3 08_TOOLS/product_engineering/workflow_gate.py start-implementation/start-release/architecture-hardening ...` |

> 脚本原为 Trae IDE 设计（Windows 路径），已适配 AI_SYSTEM Linux 环境。用户需自行指定 `--root` 指向目标项目。

## 碎片持久化目录（按项目）

```
<project-root>/docs/changes/current.md          ← active change 索引
<project-root>/docs/changes/REQ-YYYY-NNN/        ← 单 change 目录
  requirement-fragments.md / design-fragments.md / task-fragments.md
  test-fragments.md / incident-fragments.md / review-fragments.md
  growth-fragments.md / portfolio-fragments.md
  consolidation-log.md / prd.md / technical-design.md
<project-root>/docs/product-state/
  product_state.json / fragments.jsonl / decisions.jsonl / scorecard.md
```

## 成熟度等级

| 等级 | 含义 | 升下一级门禁 |
|------|------|------------|
| Chaos | 散乱想法 | 确定用户/问题/工作流 |
| Shape | 用户/问题/工作流可见 | 定义 v0 范围和非目标 |
| Spec | 可规格化 | 产出可构建的技术设计和任务 |
| Buildable | 可开始实现 | 通过测试、发布计划、运维契约 |
| Releasable | 可安全发布 | 验证部署、回滚、健康、日志、版本 |
| Operable | 可持续运维改进 | 通过架构加固、监控、备份、事故复盘 |

## 模板索引

| 文件 | 用途 |
|------|------|
| `templates/prd.md` | PRD 模板 |
| `templates/adr.md` | ADR 填写指引 |
| `templates/adr-000.md` | ADR 编号文件模板 |
| `templates/self-test.md` | 自测清单 |
| `templates/release-plan.md` | 发布计划 |
| `templates/rollback-record.md` | 回滚记录 |
| `templates/runbook.md` | 运维手册 |

## 变更历史

- v0.2.0 (2026-06-25): 从 Joey 提供的 integrated package 完整导入 20 个 Skill + 3 个脚本；状态从 testing 升为 active
- v0.1.0 (2026-06-17): 初始 staging，碎片工具验证，POWER_MARKET_AGENT 第一轮闭环
