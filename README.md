# Solo Product Engineering Skills 🚀

> 单人产品工程方法论 — 20 个 AI Skill，覆盖从想法到发布、运维、成长的全生命周期

[![Skills](https://img.shields.io/badge/skills-20-blue)](./skills/)
[![Templates](https://img.shields.io/badge/templates-7-green)](./templates/)
[![Scripts](https://img.shields.io/badge/scripts-3-orange)](./scripts/)
[![Version](https://img.shields.io/badge/version-v0.2.0-brightgreen)]()
[![Status](https://img.shields.io/badge/status-active-success)]()

---

## 这是什么？

当你是 **唯一的产品经理 + 唯一的工程师** 时，传统的大团队方法论（Sprint、站会、多人评审）并不适用。

这套 Skill 是为 **Solo Developer / Indie Maker / 一人产品团队** 设计的全栈产品工程方法论。每个 Skill 是一个独立的 AI 提示词模块，可以单独使用，也可以串联成完整工作流。

---

## 三层架构

```
入口层：solo-product-engineering-operator（自动检测→路由→调度）
    ↓
工具层（20 个）：产品阶段(7) + 工程阶段(7) + 运营阶段(6)
    ↓
持久层：solo-fragment-collector（碎片记录+合并历史）
```

---

## 20 个 Skill 全景

### 🔵 产品阶段（想法 → 定义）
| # | Skill | 一句话 |
|---|-------|--------|
| 1 | `solo-idea-intake-triage` | 想法打分分类：做/搁置/放弃 |
| 2 | `solo-problem-discovery-research` | 调研验证：风险假设→证据→决策 |
| 3 | `solo-product-definition-prd` | 产出可执行 PRD |
| 4 | `solo-mvp-scope-roadmap` | 版本切片 + 里程碑 |
| 5 | `solo-project-ledger-prioritization` | 多项目台账 + WIP 限制 |
| 6 | `solo-requirement-to-acceptance` | Given/When/Then 可测验收 |
| 7 | `solo-repo-doc-structure` | 标准文档目录结构 |

### 🟢 工程阶段（设计 → 发布）
| # | Skill | 一句话 |
|---|-------|--------|
| 8 | `solo-technical-design-adr` | 技术方案 + ADR |
| 9 | `solo-task-breakdown-kanban` | Backlog→Review→Done |
| 10 | `solo-implementation-guardrails` | 6 项代码护栏（迁移/env/密钥/健康/日志/测试）|
| 11 | `solo-self-test-quality-gate` | 四类自测 + 发布前检查 |
| 12 | `solo-release-artifact-builder` | RELEASE.json + SHA256 |
| 13 | `solo-deploy-rollback-runbook` | 13 步部署 + 7 种回滚 |
| 14 | `solo-product-engineering-operator` | 总控入口，自动检测信号 |

### 🟡 运营阶段（运行 → 成长）
| # | Skill | 一句话 |
|---|-------|--------|
| 15 | `solo-ops-observability-backup` | 最低可观测栈 |
| 16 | `solo-incident-review-improvement` | 事故时间线→根因→改进 |
| 17 | `solo-weekly-monthly-review-coach` | 周/月复盘 |
| 18 | `solo-pm-dev-growth-roadmap` | 6 个月成长路线 |
| 19 | `solo-portfolio-case-study-builder` | 作品集案例 |
| 20 | `solo-fragment-collector` | 全程碎片记录 |

---

## 确定性脚本

| 脚本 | 功能 |
|------|------|
| `scripts/fragment_store.py` | 8 阶段碎片读写合并 |
| `scripts/product_state_store.py` | Product State 全生命周期管理 |
| `scripts/workflow_gate.py` | 实现门禁 / 发布门禁 / 架构加固检查 |

---

## 成熟度等级

```
Chaos → Shape → Spec → Buildable → Releasable → Operable
```

| 等级 | 含义 | 升级门禁 |
|------|------|---------|
| Chaos | 散乱想法 | 确定用户/问题/工作流 |
| Shape | 三要素可见 | 定义 v0 范围和非目标 |
| Spec | 可规格化 | 技术设计 + 任务拆解 |
| Buildable | 可开始实现 | 测试 + 发布计划 + 运维契约 |
| Releasable | 可安全发布 | 部署验证 + 回滚 + 健康检查 |
| Operable | 可持续运维 | 架构加固 + 监控 + 备份 + 复盘 |

---

## 快速开始

1. **选一个 Skill**：从上方 20 个中选当前需要的
2. **打开 `SKILL.md`**：每个 skill 目录下包含完整提示词
3. **加载到你的 AI 工具**：支持 Claude、ChatGPT、Cursor、OpenClaw 等
4. **按需串联**：多个 skill 可以串联成完整工作流

```bash
# 从总控入口开始
cat skills/solo-product-engineering-operator/SKILL.md

# 初始化项目碎片系统
python3 scripts/fragment_store.py --root /path/to/your/project init
```

---

## 目录结构

```
.
├── README.md              ← 你在这里
├── ARCHITECTURE.md        ← 架构设计文档
├── SKILL_INDEX.md         ← 20 个 Skill 索引
├── WORKFLOW.md            ← 工作流说明
├── CHANGELOG.md           ← 变更日志
├── VALIDATION_LOG.md      ← 验证记录
├── skills/                ← 20 个 Skill 目录
│   ├── solo-idea-intake-triage/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── solo-product-definition-prd/
│   │   └── ...
│   └── ...
├── scripts/               ← 确定性脚本
│   ├── fragment_store.py
│   ├── product_state_store.py
│   └── workflow_gate.py
└── templates/             ← 7 个模板
    ├── prd.md
    ├── adr.md
    ├── self-test.md
    ├── release-plan.md
    ├── rollback-record.md
    ├── runbook.md
    └── adr-000.md
```

---

## 适用场景

- ✅ Solo 开发者做产品
- ✅ 一人创业团队
- ✅ AI 辅助产品工程
- ✅ 产品经理学习工程侧方法论
- ✅ AI Agent 的工具箱（如 OpenClaw / Cursor）

---

## License

MIT — 自由使用、修改、分发。

---

*Built for solo builders. Automate the boring, focus on the product.*
