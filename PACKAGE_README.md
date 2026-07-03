# Solo Product Engineering Skills

> AI 辅助的单人产品工程操作系统 — 从想法到上线运维，20 个 Skill 全链路覆盖。

---

## 一、这是什么

一套 AI 工具 Skill 集，为单人开发者 / 独立创始人设计。覆盖产品工程的完整生命周期：

- 想法评估 → 需求调研 → PRD → MVP 路线图 → 技术设计 → 任务拆解 → 编码护栏 → 自测 → 发布 → 部署 → 运维 → 事故复盘 → 周月复盘 → 成长规划 → 作品案例

**核心理念**：你正常聊天、正常写代码，它检测候选信号、按强弱判断是否收纳碎片，用脚本持久化到磁盘，并在合适时机提醒你合并成结构化产出。

---

## 二、安装

### 2.1 手动部署（推荐）

将本仓库克隆或下载到本地，复制 `skills/` 目录到你使用的 AI 工具的 skills 目录中：

| AI 工具 | Skills 目录 | 说明 |
|:---|:---|:---|
| **Cursor** | 项目根目录的 `.cursor/skills/` | 项目级 Skill |
| **Claude Code** | `~/.claude/skills/` | 全局或项目级 |
| **OpenClaw** | 项目 `AGENTS.md` 中引用 | 通过 Agent 配置加载 |
| **GitHub Copilot** | 通过自定义指令加载 SKILL.md 内容 | 粘贴到 `.github/copilot-instructions.md` |

也可以将 SKILL.md 内容直接粘贴到你的 AI 对话中作为系统提示。

### 2.2 目录结构

```
skills/
├── solo-product-engineering-operator/   ← 总控入口
├── solo-idea-intake-triage/             ← 产品阶段 (7个)
├── solo-problem-discovery-research/
├── solo-product-definition-prd/
├── solo-mvp-scope-roadmap/
├── solo-project-ledger-prioritization/
├── solo-requirement-to-acceptance/
├── solo-repo-doc-structure/
├── solo-technical-design-adr/           ← 工程阶段 (6个)
├── solo-task-breakdown-kanban/
├── solo-implementation-guardrails/
├── solo-self-test-quality-gate/
├── solo-release-artifact-builder/
├── solo-deploy-rollback-runbook/
├── solo-ops-observability-backup/       ← 运营阶段 (5个)
├── solo-incident-review-improvement/
├── solo-weekly-monthly-review-coach/
├── solo-pm-dev-growth-roadmap/
├── solo-portfolio-case-study-builder/
└── solo-fragment-collector/             ← 持久化引擎
```

### 2.3 确定性脚本

```bash
# 初始化项目碎片系统
python3 scripts/fragment_store.py --root /path/to/your-project init

# 管理 Product State
python3 scripts/product_state_store.py --root /path/to/your-project init
python3 scripts/product_state_store.py --root /path/to/your-project brief

# 工作流门禁
python3 scripts/workflow_gate.py --root /path/to/your-project start-implementation --change-id REQ-2026-001
```

---

## 三、架构

```
                    ┌──────────────────────────────────┐
                    │  solo-product-engineering-operator │ ← 总控入口
                    │       自动检测 → 路由 → 调度        │
                    └──────────┬───────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
   产品阶段 Skill          工程阶段 Skill          运营/成长 Skill
   (7个)                  (6个)                  (5个)
   idea-intake           technical-design       ops-observability
   problem-discovery     task-breakdown         incident-review
   product-prd           implementation-guard   weekly-review
   mvp-roadmap           self-test              pm-dev-growth
   project-ledger        release-artifact       portfolio-case
   requirement-accept    deploy-rollback
   repo-doc
   
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ solo-fragment-collector │ ← 持久化引擎
                    │   跨会话碎片记录 + 变更追踪 │
                    └──────────────────────┘
```

---

## 四、Skill 完整目录

### 4.1 总控

| Skill | 触发时机 | 做什么 |
|---|---|---|
| `solo-product-engineering-operator` | 每次对话自动 | 总控入口，扫描上下文，路由到对应子 Skill |

### 4.2 产品阶段

| Skill | 关键词/信号 | 做什么 |
|---|---|---|
| `solo-idea-intake-triage` | 我想做、要不要、评估、优先级 | 结构化评估想法：价值/紧迫度/可行性打分，决定 pursue/park/reject |
| `solo-problem-discovery-research` | 调研、用户、竞品、市场、验证 | 问题调研框架：风险假设→证据路径→竞品分析→决策 |
| `solo-product-definition-prd` | PRD、需求、目标、非目标、范围 | 输出完整 PRD：用户→场景→问题→目标→非目标→验收→风险→指标 |
| `solo-mvp-scope-roadmap` | MVP、版本、路线图、v0/v1 | 砍范围、定版本切片、排里程碑 |
| `solo-project-ledger-prioritization` | 台账、多项目、优先级、WIP | 项目台账 + 加权优先级公式 + WIP 限制 |
| `solo-requirement-to-acceptance` | 验收、Given/When/Then、用户故事 | 需求→可测试的验收标准 |
| `solo-repo-doc-structure` | README、文档、仓库结构 | 建标准文档目录结构 |

### 4.3 工程阶段

| Skill | 关键词/信号 | 做什么 |
|---|---|---|
| `solo-technical-design-adr` | 架构、数据库、API、表结构、部署、回滚 | 输出技术方案 + ADR：设计→迁移→env→验证→回滚→风险 |
| `solo-task-breakdown-kanban` | 要做、TODO、分工、排期 | 拆任务→看板（Backlog→Doing→Review→Done） |
| `solo-implementation-guardrails` | **任何代码变更自动触发** | 6 项护栏检查：迁移/env/密钥/健康检查/日志/测试 |
| `solo-self-test-quality-gate` | 测一下、边界、异常、权限、回归 | 四类自测清单：正常/边界/异常/权限 + 发布前检查 |
| `solo-release-artifact-builder` | 发布、版本号、制品、checksum | 打版→制品→SHA256→RELEASE.json |
| `solo-deploy-rollback-runbook` | 部署、上线、回滚 | 部署 13 步 + 验证断言 + 7 种回滚触发条件 |

### 4.4 运营/成长阶段

| Skill | 关键词/信号 | 做什么 |
|---|---|---|
| `solo-ops-observability-backup` | 运维、监控、日志、备份 | 最低可观测栈：健康检查/版本/日志/备份/磁盘/端口 |
| `solo-incident-review-improvement` | 挂了、报错、500、回滚、数据丢了 | 事故时间线→根因→改进措施→更新 artifact |
| `solo-weekly-monthly-review-coach` | 这周、进度、总结、回顾 | 周复盘：产出/阻塞/下周计划；月复盘：成果/路线/学习 |
| `solo-pm-dev-growth-roadmap` | 想学、怎么提升、规划、路线 | 6 个月 PM+开发能力成长路线 |
| `solo-portfolio-case-study-builder` | 做完了、上线了、案例 | 项目→作品集案例：问题/决策/证据/经验 |

### 4.5 持久化引擎

| Skill | 触发时机 | 做什么 |
|---|---|---|
| `solo-fragment-collector` | 全程自动 | Init/Capture/Read/Consolidate/Diff — 碎片文件读写 + 合并历史追踪 |

---

## 五、碎片系统

### 5.1 工作原理

```
你随便说的话
       ↓
9 类候选信号自动检测（需求/设计/任务/测试/事故/复盘/成长/作品/编码）
       ↓
强/弱/疑似分层判断
       ↓
fragment-collector 脚本 Capture → 写入磁盘文件
       ↓ 达到阈值
fragment-collector.Consolidate → 归档碎片 + 产出结构化文档 + 更新 changelog
       ↓
fragment-collector.Diff → 展示改进变化
```

### 5.2 碎片阈值

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

### 5.3 持久化文件

```
docs/changes/current.md              ← 当前 active change
docs/changes/REQ-YYYY-NNN/
  requirement-fragments.md
  design-fragments.md
  task-fragments.md
  test-fragments.md
  incident-fragments.md
  review-fragments.md
  growth-fragments.md
  portfolio-fragments.md
  consolidation-log.md       ← 合并历史
  prd.md                     ← 合并产出
  technical-design.md        ← 合并产出
  ...
```

### 5.4 确定性脚本

```bash
python3 scripts/fragment_store.py --root /path/to/project init
python3 scripts/fragment_store.py --root /path/to/project capture requirement "用户希望上传头像并限制 2MB"
python3 scripts/fragment_store.py --root /path/to/project status
python3 scripts/fragment_store.py --root /path/to/project consolidate requirement
```

---

## 六、编码护栏自动检查

**每次写代码时自动运行**，检查 6 项：

| # | 检查项 | 详情 |
|---|---|---|
| 1 | 数据库迁移 | migration 文件存在？兼容性是否说明？ |
| 2 | 环境变量 | `.env.example` 是否更新？ |
| 3 | 密钥安全 | 是否误提交了真实 `.env`/密钥/日志/备份？ |
| 4 | 健康检查 | `/health/live` 和 `/health/ready` 是否就绪？ |
| 5 | 版本端点 | `/version` 是否暴露 git SHA？ |
| 6 | 日志审计 | 错误是否可见？敏感数据是否被记录？ |

---

## 七、使用方式

### 7.1 被动模式（推荐）

你正常和你的 AI 工具对话，系统自动：

- 检测信号 → 收纳碎片
- 弱信号先判断是否属于当前 active change
- 写代码时 → 跑护栏检查
- 碎片攒够了 → 提醒合并
- 每次回复末尾 → 显示碎片统计

### 7.2 主动指令

| 指令 | 效果 |
|---|---|
| "初始化碎片目录" | 创建 `docs/changes/` 结构 |
| "看看现在攒了多少碎片" | 从磁盘读取碎片状态 |
| "把需求合并成 PRD" | 跳过阈值，直接合并 |
| "看看上次合并后改了什么" | 展示 Diff |
| "初始化项目文档" | 创建标准 README + docs 结构 |
| "帮我评估这个想法" | 触发 idea-intake-triage |
| "写个 PRD" | 触发 product-definition-prd |
| "做技术设计" | 触发 technical-design-adr |
| "拆任务" | 触发 task-breakdown-kanban |
| "部署检查" | 触发 deploy-rollback-runbook |
| "自测清单" | 触发 self-test-quality-gate |

---

## 八、典型工作流

```
第 1 天："我想做个 XX"         → idea-intake-triage 评估
      "用户是不是真的有这需求"    → problem-discovery 调研
      "帮我写个 PRD"            → product-definition-prd 输出

第 2 天："数据库怎么设计"        → technical-design-adr 方案
      "帮我拆成任务"            → task-breakdown-kanban 看板

第 3 天："帮我写登录模块"        → implementation-guardrails 护栏检查

第 4 天："测完了，感觉可以"      → self-test-quality-gate 验证

第 5 天："准备上线"             → release-artifact-builder 打版
      "部署到服务器"            → deploy-rollback-runbook 部署

第 6 天："线上跑得怎么样"        → ops-observability-backup 运维

一个月后："这个月做了什么"        → weekly-monthly-review-coach 复盘
        "项目做完了，写案例"     → portfolio-case-study-builder 作品
```

---

## 九、回答格式

每次回复末尾自动附带：

```
## Fragment Status
| 阶段 | 碎片数 | 状态 |
|---|---|---|
| 需求 | 3 | collecting |
| 设计 | 1 | collecting |
| 任务 | 0 | collecting |
| 测试 | 2 | collecting |
| 事故 | 0 | — |
| 复盘 | 0 | — |
| 成长 | 0 | — |
| 作品 | 0 | — |
```

---

## 十、贡献与扩展

如需新增 Skill：
1. 在 `skills/<skill-name>/` 下创建 `SKILL.md`（含 frontmatter）
2. 在本文件更新 Skill 目录表
3. 在规则文件中添加触发规则

**Skill 格式**：

```markdown
---
name: "skill-name"
description: "描述（含触发条件）"
---

# Skill Title

## Purpose
...

## Workflow
...
```
