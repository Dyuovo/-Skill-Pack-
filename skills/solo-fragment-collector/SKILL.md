---
name: solo-fragment-collector
description: Persist and manage conversation-to-operable-product state across sessions. Use to initialize, capture, read, and update Product State, structured conversation fragments, decisions, phase fragments, consolidation history, maturity status, and operability gaps. Includes deterministic scripts for Product State and legacy fragment file I/O. 适用于产品状态持久化、对话碎片结构化、决策账本、成熟度状态、运维缺口和跨会话连续性。
---

# Solo Fragment Collector

## Purpose

Persist the system's memory so scattered user conversation can become an operable product across sessions.

There are two storage tracks:

1. **Product State track**: the primary source of truth for product understanding, maturity, decisions, risks, and operability gaps.
2. **Phase Fragment track**: legacy Markdown phase files for PRD/ADR/task/test/review consolidation history.

Use deterministic scripts instead of manually editing these files when possible.

## Product State Script

Run from the target project root:

```powershell
function Invoke-ProjectPython {
  param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
  if (Get-Command py -ErrorAction SilentlyContinue) { & py -3 @Args; return }
  if (Get-Command python -ErrorAction SilentlyContinue) { & python @Args; return }
  throw "No Python interpreter found. Install Python or fix the launcher before continuing."
}
$stateScript = if (Test-Path ".trae\skills\solo-fragment-collector\scripts\product_state_store.py") {
  ".trae\skills\solo-fragment-collector\scripts\product_state_store.py"
} else {
  "$env:USERPROFILE\.trae-cn\skills\solo-fragment-collector\scripts\product_state_store.py"
}
Invoke-ProjectPython $stateScript init
Invoke-ProjectPython $stateScript brief
Invoke-ProjectPython $stateScript capture --type requirement --evidence assumption --raw "能不能自动一点" --meaning "用户希望减少手动操作"
Invoke-ProjectPython $stateScript set core_problem "用户当前流程存在重复手工操作"
Invoke-ProjectPython $stateScript add mvp_scope "v0 支持单人完成主流程"
Invoke-ProjectPython $stateScript decision "v0 不做多人协作" --reason "当前目标用户是个人操作者" --impact "暂不设计 org/team 模型"
Invoke-ProjectPython $stateScript reconcile --change-id REQ-2026-002
Invoke-ProjectPython $stateScript promote-maturity Buildable
Invoke-ProjectPython $stateScript resolve-gap "/health/live"
```

Useful options:

- `--root <path>`: operate on another project root.
- `brief`: print compact Product State for low-context startup.
- `brief --json`: print the same compact state as JSON for tooling.
- `status`: print counts and gaps when the brief is not enough.
- `capture --updates key=value`: include one or more state update hints.
- `set <field> <value>`: replace scalar fields.
- `add <field> <value>`: append to list fields.
- `gap <text>`: append an operability gap.
- `resolve-gap <text>`: remove matching operability gaps.
- `promote-maturity <level>`: promote only when hard gates pass.
- `reconcile --change-id <REQ-YYYY-NNN>`: update Product State from PRD/design/task/implementation artifacts.

## Workflow Gate Script

Use this script to make implementation and release gates deterministic:

```powershell
$gateScript = if (Test-Path ".trae\skills\solo-fragment-collector\scripts\workflow_gate.py") {
  ".trae\skills\solo-fragment-collector\scripts\workflow_gate.py"
} else {
  "$env:USERPROFILE\.trae-cn\skills\solo-fragment-collector\scripts\workflow_gate.py"
}
Invoke-ProjectPython $gateScript start-implementation --change-id REQ-2026-002 --intent "implement search bug fix"
Invoke-ProjectPython $gateScript implementation-status --change-id REQ-2026-002
Invoke-ProjectPython $gateScript complete-implementation --change-id REQ-2026-002 --evidence "manual API check passed"
Invoke-ProjectPython $gateScript drift --change-id REQ-2026-002
Invoke-ProjectPython $gateScript start-release --change-id REQ-2026-002
Invoke-ProjectPython $gateScript architecture-hardening --change-id REQ-2026-002
```

`start-implementation` writes `implementation-gate.md` and fails if Product State or required artifacts are missing.

`drift` reports doc/code drift such as docs claiming FTS5 while current code uses SQL LIKE.

`start-release` writes `release-gate.md` and fails while doc/code drift, release test evidence, backup/restore verification, operability gaps, positive core-flow coverage, API/UI contract evidence, domain text coverage, pytest evidence, actual pytest execution, or SQLite WAL backup evidence are missing.

`architecture-hardening` writes `architecture-hardening.md` and fails until Search Scale, Sync Accuracy, Dependency Fallback, Migration, Config Consistency, and Real Sample Verification are checked with PASS/N/A evidence.

Never hand-edit `implementation-gate.md`, `release-gate.md`, or `architecture-hardening.md` to say `PASS`. These files are machine outputs; rerun the gate if they are stale.

Product State files:

```text
docs/product-state/product_state.json
docs/product-state/fragments.jsonl
docs/product-state/decisions.jsonl
docs/product-state/scorecard.md
```

## Context Budget

Default to progressive disclosure:

1. Run `brief`.
2. If the brief exposes a gap, read only `scorecard.md` or the named change artifact.
3. If an artifact is long, search it with `rg` before opening.
4. If an exported chat is long, capture fragments into Product State instead of carrying the full transcript.
5. Avoid reading all phase files, all skill files, or the full Product State JSON unless debugging storage itself.

For ordinary product work, the agent should keep only:

```text
brief status
current user request
one relevant artifact or code area
one selected specialist skill
```

## Product State Fields

Maintain:

```text
product_summary
target_users
core_problem
primary_workflow
confirmed_facts
assumptions
requirements
non_goals
mvp_scope
backlog
rejected_items
conflicts
decisions
evidence
engineering_risks
operability_gaps
next_question
maturity_level
```

Treat unknowns honestly. Store uncertain interpretations under `assumptions`, not `confirmed_facts`.

## Capture Guidance

Use structured fragments:

| Field | Meaning |
|---|---|
| raw_text | User's original wording |
| interpreted_meaning | Product interpretation |
| fragment_type | pain, requirement, role, workflow, data, constraint, risk, change, evidence, preference, incident, noise |
| confidence | low, medium, high |
| evidence_level | confirmed, assumption, preference, evidence, conflict, noise |
| product_area | Feature or product area |
| state_updates | Suggested Product State fields to update |
| conflicts_with | Prior state or decision it conflicts with |
| requires_clarification | Whether one critical question is needed |

Rules:

- Confirmed user statements can update `confirmed_facts`.
- Inferred meanings go to `assumptions`.
- "Nice to have" or "顺手加" items usually go to `backlog` unless they directly serve the primary workflow.
- Operations concerns go to `operability_gaps` until satisfied.
- Never discard conflicts; store them in `conflicts` or `decisions`.

## Maturity Status

Use Product State to classify maturity:

| Level | Required State |
|---|---|
| Chaos | Scattered ideas only |
| Shape | target user, core problem, and primary workflow are visible |
| Spec | v0 scope, non-goals, and acceptance frame are explicit |
| Buildable | technical design, tasks, tests, and risks are sufficient |
| Releasable | release verification, rollback, health, logs, and version are ready |
| Operable | monitoring, backup, restore verification, and review loop exist |

Do not promote maturity just because a document exists.

## Legacy Phase Fragment Script

Use this for source material and consolidation history:

```powershell
Invoke-ProjectPython ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" init
Invoke-ProjectPython ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" capture requirement "用户希望上传头像并限制 2MB"
Invoke-ProjectPython ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" status
Invoke-ProjectPython ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" read requirement
Invoke-ProjectPython ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" consolidate requirement
Invoke-ProjectPython ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" diff requirement
```

Legacy structure:

```text
docs/changes/current.md
docs/changes/REQ-YYYY-NNN/
  requirement-fragments.md
  design-fragments.md
  task-fragments.md
  test-fragments.md
  incident-fragments.md
  review-fragments.md
  growth-fragments.md
  portfolio-fragments.md
  consolidation-log.md
```

## Quality Gate

- Verify `product_state_store.py status` after init or significant updates.
- Run `reconcile` after creating or editing PRD, technical design, task list, implementation notes, or release notes.
- Use `promote-maturity` instead of directly setting `maturity_level`.
- Never mix unrelated products in one Product State.
- Never delete decision history to make the current answer look cleaner.
- Never silently promote assumptions to facts.
- If `operability_gaps` is non-empty, do not claim the product is Releasable or Operable.
