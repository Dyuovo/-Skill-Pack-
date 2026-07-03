# 架构与核心逻辑

## 概述

Solo Product Engineering Skills 是一套 AI 辅助的产品工程操作系统，由 20 个 Skill 组成。它将"记不住、容易漏"的产品工程纪律，变成对话中有规则、有持久化脚本、有质量门禁的轻量操作流。

---

## 三层架构

```
┌─────────────────────────────────────────────┐
│         入口层（1 个 Skill）                  │
│  solo-product-engineering-operator           │
│  自动扫描对话上下文 → 路由到对应工具层 Skill    │
└──────────────────┬──────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌────────┐   ┌────────┐   ┌────────┐
│产品阶段│   │工程阶段│   │运营阶段│
│ 7 个   │   │ 6 个   │   │ 6 个   │
└───┬────┘   └───┬────┘   └───┬────┘
    │            │            │
    └────────────┼────────────┘
                 ▼
┌─────────────────────────────────────────────┐
│         持久层（1 个 Skill）                  │
│  solo-fragment-collector                     │
│  跨会话碎片文件读写 + 合并历史追踪             │
└─────────────────────────────────────────────┘
```

### 入口层

`solo-product-engineering-operator` 是唯一入口。每次对话时自动扫描上下文，匹配信号后路由到对应工具层 Skill。用户不需要知道该调用哪个。

### 工具层（18 个）

按产品工程生命周期分为三个阶段：

**产品阶段（想法→定义）：**

| Skill | 职责 |
|---|---|
| `solo-idea-intake-triage` | 想法结构化评估：打分、分类、决策（pursue/park/reject）|
| `solo-problem-discovery-research` | 问题调研框架：风险假设→证据收集→竞品分析 |
| `solo-product-definition-prd` | 输出完整 PRD：用户/场景/目标/非目标/验收/风险 |
| `solo-mvp-scope-roadmap` | 砍范围、定版本切片、排里程碑 |
| `solo-project-ledger-prioritization` | 多项目台账 + 加权优先级 + WIP 限制 |
| `solo-requirement-to-acceptance` | 需求 → Given/When/Then 验收标准 |
| `solo-repo-doc-structure` | 仓库标准文档目录初始化 |

**工程阶段（设计→发布）：**

| Skill | 职责 |
|---|---|
| `solo-technical-design-adr` | 技术方案 + ADR：架构/数据库/API/迁移/env/回滚/风险 |
| `solo-task-breakdown-kanban` | 拆任务 → 看板流（Backlog→Doing→Done）|
| `solo-implementation-guardrails` | 6 项编码护栏：迁移/env/密钥/健康检查/日志/测试 |
| `solo-self-test-quality-gate` | 四类自测：正常/边界/异常/权限 + 发布前检查 |
| `solo-release-artifact-builder` | 打版→制品→SHA256→RELEASE.json |
| `solo-deploy-rollback-runbook` | 部署 13 步 + 7 种回滚触发条件 |

**运营阶段（运行→成长）：**

| Skill | 职责 |
|---|---|
| `solo-ops-observability-backup` | 最低可观测栈：健康/版本/日志/备份/磁盘/端口 |
| `solo-incident-review-improvement` | 事故时间线→根因→改进→更新 artifact |
| `solo-weekly-monthly-review-coach` | 周复盘/月复盘：产出/阻塞/计划/学习 |
| `solo-pm-dev-growth-roadmap` | 6 个月 PM+开发能力成长路线 |
| `solo-portfolio-case-study-builder` | 项目 → 作品案例：问题/决策/证据/经验 |

### 持久层

`solo-fragment-collector` 负责跨会话持久化。它通过 `scripts/fragment_store.py` 提供 6 个确定性操作：

| 操作 | 功能 |
|---|---|
| `Init` | 创建 `docs/changes/REQ-YYYY-NNN/` 目录和所有碎片文件 |
| `Status` | 从磁盘加载当前碎片状态 |
| `Capture` | 追加碎片 + 时间戳写入文件 |
| `Read` | 读取指定阶段碎片列表 |
| `Consolidate` | 归档旧碎片 → 产出结构化文件 → 更新合并日志 |
| `Diff` | 对比前后两次合并的变化 |

---

## 核心逻辑：碎片 → 结构

```
任意对话
    ↓
9 类候选信号自动检测（需求/设计/任务/测试/事故/复盘/成长/作品/编码）
    ↓
强/弱/疑似分层判断
    ↓
solo-fragment-collector 脚本 Capture  →  写入磁盘文件（带时间戳）
    ↓ 达到阈值
solo-fragment-collector.Consolidate  →  归档碎片 + 产出结构化文档
    ↓
solo-fragment-collector.Diff  →  展示改进变化
```

### 信号检测

每个阶段有多类信号词 + 一条语义兜底规则。关键词只发现候选碎片，写盘前按三档判断：

| 档位 | 动作 |
|---|---|
| 强信号 | 立即 capture |
| 弱信号 | 只有延续当前 active change 或与其他信号组合时 capture |
| 疑似信号 | 只提示，不写盘 |

| 阶段 | 阈值 | 产出物 |
|---|---|---|
| 需求 | ≥5 条 | PRD |
| 设计 | ≥3 条 | 技术方案 + ADR |
| 任务 | ≥5 条 | 看板 |
| 测试 | ≥3 条 | 自测清单 |
| 事故 | ≥1 条（立即） | 事故复盘 |
| 复盘 | ≥5 条 | 周/月报 |
| 成长 | ≥3 条 | 成长路线 |
| 作品 | ≥3 条 | 作品案例 |
| 编码 | 实时 | 护栏检查 |

### 持久化目录

```
docs/changes/current.md              ← 当前 active change
docs/changes/REQ-YYYY-NNN/
  requirement-fragments.md    ← 需求碎片
  design-fragments.md         ← 设计碎片
  task-fragments.md           ← 任务碎片
  test-fragments.md           ← 测试碎片
  incident-fragments.md       ← 事故碎片
  review-fragments.md         ← 复盘碎片
  growth-fragments.md         ← 成长碎片
  portfolio-fragments.md      ← 作品碎片
  consolidation-log.md        ← 合并历史
  prd.md                      ← 合并产出
  technical-design.md         ← 合并产出
```

### 持久化脚本

```bash
python3 scripts/fragment_store.py init
python3 scripts/fragment_store.py capture requirement "<fragment>"
python3 scripts/fragment_store.py status
python3 scripts/fragment_store.py consolidate requirement
```

脚本只负责可靠文件操作和历史归档；最终 PRD、ADR、看板、自测清单仍由对应专业 Skill 基于碎片生成。

---

## 编码护栏

每次写代码时自动检查 6 项：

| # | 检查项 | 内容 |
|---|---|---|
| 1 | 数据库迁移 | migration 存在？兼容性说明？旧迁移未被改写？ |
| 2 | 环境变量 | `.env.example` 已更新？ |
| 3 | 密钥安全 | 真实 `.env`/密钥/日志/备份未被提交？ |
| 4 | 健康检查 | `/health/live` 和 `/health/ready` 就绪？ |
| 5 | 版本端点 | `/version` 暴露 git SHA？ |
| 6 | 日志审计 | 错误可见？敏感数据未被记录？ |

---

## 完整工作流

```
第 1 天：想法 → idea-intake-triage → 调研 → problem-discovery → PRD → product-prd
第 2 天：设计 → technical-design-adr → 拆任务 → task-breakdown-kanban
第 3 天：编码 → implementation-guardrails（护栏自动检查）
第 4 天：自测 → self-test-quality-gate
第 5 天：打版 → release-artifact-builder → 部署 → deploy-rollback-runbook
第 6 天：运维 → ops-observability-backup
一个月后：复盘 → weekly-monthly-review-coach → 作品 → portfolio-case-study-builder
```

---

## 技术约束

- Skill 由各目录下的 `SKILL.md` 文件定义，加载到 AI 工具（Cursor / Claude / OpenClaw 等）即可使用
- 自动触发规则通过各 AI 工具的项目规则文件加载（如 `.cursorrules`、`AGENTS.md` 等）
- 碎片持久化依赖 `solo-fragment-collector/scripts/fragment_store.py`，写入 `docs/changes/` 目录
- `docs/changes/current.md` 是 active change 索引，多需求并行时必须显式切换 `REQ-YYYY-NNN`
- 规则文件按项目配置，可复制到其他项目中复用
