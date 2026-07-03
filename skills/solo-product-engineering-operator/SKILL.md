---
name: solo-product-engineering-operator
description: Coordinate conversation-to-operable-product work. Invoke on every product, design, coding, deployment, operations, or exploratory conversation where messy user dialogue should be turned into Product State, scoped MVP decisions, engineering artifacts, implementation tasks, release evidence, rollback paths, and operability. 适用于从零散对话提炼产品状态、收敛 MVP、生成 PRD/ADR/任务/测试/发布/运维闭环。
---

# Solo Product Engineering Operator

## Purpose

Turn ordinary, messy, long-running user conversation into an operable product. The primary object is **Product State**, not a pile of prompt templates.

Core loop:

```text
messy conversation
  -> interpret semantic fragments
  -> update Product State
  -> detect gaps, conflicts, and scope creep
  -> ask one critical question when needed
  -> generate or update the smallest useful artifact
  -> enforce build, release, rollback, and operations gates
```

## Operating Rule

On every relevant turn:

1. Read current Product State brief when it exists.
2. Classify the user's message into fragments: pain, requirement, role, workflow, data, constraint, risk, change, evidence, preference, incident, or noise.
3. Decide evidence level: confirmed fact, assumption, preference, evidence, conflict, or noise.
4. Update Product State before generating downstream artifacts.
5. Detect conflicts with previous decisions or scope.
6. Ask at most one clarifying question, only if it removes the largest blocker.
7. Route to the smallest specialist skill needed next.
8. Keep operability requirements active from the start, not as a final checklist.
9. Before writing code, run the implementation gate. After creating artifacts, reconcile Product State.

Use deterministic storage when available:

```bash
# Run from the project root or use --root to specify the project path
python3 scripts/product_state_store.py --root . init
python3 scripts/product_state_store.py --root . capture --type requirement --evidence assumption --raw "<user text>" --meaning "<interpreted meaning>"
python3 scripts/product_state_store.py --root . brief
python3 scripts/product_state_store.py --root . reconcile --change-id REQ-YYYY-NNN
python3 scripts/product_state_store.py --root . promote-maturity Buildable
python3 scripts/workflow_gate.py --root . start-implementation --change-id REQ-YYYY-NNN --intent "<implementation intent>"
```

On systems where `python3` is not available, use `python` or `py -3` instead.

Use legacy fragment storage only for phase-specific source notes and consolidation history:

```bash
python3 scripts/fragment_store.py --root . capture requirement "<fragment>"
```

## Context Budget

Protect the context window as a product resource:

- Start with `product_state_store.py brief`; use `status` only when counts and gap lists are needed.
- Do not read the full Product State JSON unless debugging state storage or reconciling a corruption.
- Do not load all `docs/changes/*` artifacts. Open only the current change and only the file needed for the next gate.
- Do not paste or carry long exported chat logs. Convert them into typed fragments, decisions, conflicts, and evidence.
- Choose one specialist skill at a time. Load another only after the current decision requires it.
- Summarize previous work in 5-8 lines before continuing instead of re-reading every generated artifact.
- Prefer deterministic script output over large manually written status sections.

If context is already crowded, pause artifact generation and compact into Product State first.

## Product State

Maintain these fields, even if many are initially unknown:

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
test_plan
next_question
maturity_level
```

Maturity levels:

| Level | Meaning | Gate To Next Level |
|---|---|---|
| Chaos | Only scattered ideas | Identify likely user, problem, and rough workflow |
| Shape | User/problem/workflow are visible | Define v0 scope, non-goals, and acceptance frame |
| Spec | Product can be specified | Produce buildable technical design and task slices |
| Buildable | Implementation can start | Pass tests, release plan, and operations contract |
| Releasable | Can ship safely | Verify deploy, rollback, health, logs, and version |
| Operable | Can run and improve | Pass architecture hardening, monitor, back up, review incidents, and iterate |

Do not advance maturity because a template is filled. Advance only when the gate is satisfied.

## Fragment Interpretation

| User language | Interpret as | Default action |
|---|---|---|
| "太麻烦了" | pain | capture as possible problem; ask only if it blocks scope |
| "能不能自动一点" | requirement or automation opportunity | add assumption unless user confirms workflow |
| "我朋友也遇到过" | evidence | record evidence source and confidence |
| "先不要这个" | scope reduction | move item to non-goal or backlog |
| "顺手加个会员系统" | scope creep risk | record backlog unless it serves primary workflow |
| "上线之后别老挂" | operability requirement | update operability gaps and release gate |

Only strong, reusable information should be stored. Treat casual emotion as signal only when it reveals pain, risk, or priority.

## Scope Control

Every new requirement must be classified:

| Bucket | Rule |
|---|---|
| v0 | Directly serves primary workflow and is needed for first usable release |
| v1 | Valuable after v0 proves the workflow |
| backlog | Plausible but not yet tied to evidence or workflow |
| reject | Conflicts with product direction, cost, safety, or operability |

When rejecting or deferring scope, record the decision and reason. Do not silently drop it.

## Clarification Policy

Ask at most one question per turn. Prefer questions that unlock the next maturity gate.

Priority order:

1. Who is the first target user?
2. What is the main job or painful workflow?
3. What is the minimal successful outcome?
4. What must be explicitly out of scope for v0?
5. What risk would make release unsafe?

If the answer can be inferred with reasonable confidence, write it as an assumption instead of asking.

## Skill Routing

Use the smallest next skill:

| Need | Use |
|---|---|
| Raw idea or early product embryo | `$solo-idea-intake-triage` |
| Evidence, alternatives, market, workflow pain | `$solo-problem-discovery-research` |
| Product definition from Product State | `$solo-product-definition-prd` |
| v0/v1 scope and roadmap | `$solo-mvp-scope-roadmap` |
| Acceptance criteria and release slices | `$solo-requirement-to-acceptance` |
| Architecture, API, DB, rollout, rollback risks | `$solo-technical-design-adr` |
| Executable tasks and board | `$solo-task-breakdown-kanban` |
| Code-change guardrails | `$solo-implementation-guardrails` |
| Test and release readiness | `$solo-self-test-quality-gate` |
| Versioned release artifacts | `$solo-release-artifact-builder` |
| Deploy, verify, rollback | `$solo-deploy-rollback-runbook` |
| Logs, health, monitoring, backups | `$solo-ops-observability-backup` |
| Outage, failed deploy, rollback, data issue | `$solo-incident-review-improvement` |

## Implementation Gate

Before any code change:

1. Confirm the active change id.
2. Read Product State brief, then status only if needed.
3. Run `workflow_gate.py start-implementation --change-id <REQ-YYYY-NNN> --intent "<intent>"`.
4. Continue only if `implementation-gate.md` says `Status: PASS`.
5. Invoke or apply `$solo-implementation-guardrails`.
6. Check scope, env vars, migrations/schema, secrets, health/version, logs, tests, and rollback.
7. Write or update implementation notes.
8. Run `product_state_store.py reconcile --change-id <REQ-YYYY-NNN>` from the active change artifacts.
9. Run `workflow_gate.py implementation-status --change-id <REQ-YYYY-NNN>`.

If this gate was skipped, stop implementation and run it retroactively before continuing.

Never hand-edit `implementation-gate.md` or `release-gate.md` to say `PASS`. Treat those files as machine outputs. If the file contradicts Product State or command output, rerun the gate and trust the command.

## Release Evidence Gate

Before claiming Releasable, run `promote-maturity Releasable` and `workflow_gate.py start-release`. Release evidence must prove the risky path, not just a happy empty smoke test:

- Search/index products must include a positive non-empty hit; Chinese/chat products must include Chinese/domain text search coverage.
- API + UI products must verify request/response contract compatibility.
- Python projects must record `py -3 -m pytest -q` passing; release gate will also re-run pytest, so the report alone is not enough.
- SQLite WAL projects must verify backup consistency using checkpoint or SQLite backup API evidence.
- Secrets and keys must not be passed in query strings, logs, or browser history.

## Architecture Hardening Gate

After the product reaches Releasable, run an Architecture Hardening Review before claiming Operable. This catches structural issues that normal release tests may miss.

Use `$solo-technical-design-adr` for the review and `$solo-implementation-guardrails` for code-level checks. Write the evidence to:

```text
docs/changes/REQ-YYYY-NNN/architecture-hardening.md
```

The review must cover six dimensions with a checked PASS or N/A and evidence:

- Search Scale: latency and upgrade path for search/index products.
- Sync Accuracy: idempotent re-sync, no duplicate/loss, source-to-index count explanation.
- Dependency Fallback: missing external tools/libraries fail gracefully with clear user-visible errors.
- Migration: schema evolution or rebuild path is explicit.
- Config Consistency: `.env.example` matches runtime config.
- Real Sample Verification: real target data end-to-end, or a documented blocker and resolution path.

Then run:

```bash
python3 scripts/workflow_gate.py --root . architecture-hardening --change-id <REQ-YYYY-NNN>
python3 scripts/product_state_store.py --root . promote-maturity Operable
```

Do not claim Operable while `architecture-hardening.md` is missing, BLOCKED, or manually marked PASS without the gate command.

## Operability Defaults

Any buildable product must include:

```text
/health/live
/health/ready
/version
structured logs
error visibility
.env.example
backup strategy for persistent data
restore verification
release record
rollback path
basic monitoring or inspection command
incident review location
```

If any item is missing, add it to `operability_gaps` and block promotion to Releasable.

## Output Contract

For ordinary turns, keep the response natural, then include a compact status when useful:

```text
Product State
- Maturity: <Chaos|Shape|Spec|Buildable|Releasable|Operable>
- Current product: <one sentence or unknown>
- Primary workflow: <known/assumed/unknown>
- v0 scope: <short list>
- Main gap: <one blocker>
- Next action: <one concrete step>
```

For artifact-generation turns, output:

- Source Product State assumptions used.
- Artifact created or updated.
- Open conflicts or missing evidence.
- Quality gate before the next maturity level.

Do not append bulky status tables when they bury the answer. Prefer the deterministic `product_state_store.py status` output when exact status is needed.

## End-of-Conversation Closeout

End every product/design/code/test/release/ops conversation with a compact operational handoff. The user should know where the product stands and exactly what to say next.

Use this shape:

```text
开发状态
- 当前阶段：<Chaos|Shape|Spec|Buildable|Releasable|Operable>
- 当前 change：<REQ-YYYY-NNN>
- 本轮完成：<1-3 bullets>
- 机器验证：<commands/results, or not run>
- 剩余 blocker：<current gate blockers, or none>

下一步
- 做什么：<one smallest next slice>
- 不做什么：<scope guard>
- 你可以对我说：
  <copy-paste prompt for the next turn>
```

Rules:

- Derive status from `product_state_store.py brief` and `workflow_gate.py` output.
- Report machine gate blockers exactly; do not infer release readiness from documents alone.
- Recommend one next slice only.
- Translate engineering detail into a copy-paste instruction for the user.
- Keep the closeout under 15 lines unless the user asks for a full report.

## Quality Gate

Do not move to Buildable unless Product State names:

- Target user or operator.
- Core problem or job.
- Primary workflow.
- v0 scope and non-goals.
- Acceptance criteria.
- Technical risk.
- Test plan.
- Release verification.
- Rollback path.
- Operability gaps or confirmation that none are known.
