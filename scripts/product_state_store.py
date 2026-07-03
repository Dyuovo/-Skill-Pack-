#!/usr/bin/env python3
"""Deterministic Product State storage for conversation-to-operable-product work."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


SCALAR_FIELDS = {
    "product_summary",
    "core_problem",
    "primary_workflow",
    "next_question",
    "maturity_level",
}

LIST_FIELDS = {
    "target_users",
    "confirmed_facts",
    "assumptions",
    "requirements",
    "non_goals",
    "mvp_scope",
    "backlog",
    "rejected_items",
    "conflicts",
    "decisions",
    "evidence",
    "engineering_risks",
    "operability_gaps",
    "test_plan",
}

VALID_FRAGMENT_TYPES = {
    "pain",
    "requirement",
    "role",
    "workflow",
    "data",
    "constraint",
    "risk",
    "change",
    "evidence",
    "preference",
    "incident",
    "noise",
}

VALID_EVIDENCE_LEVELS = {
    "confirmed",
    "assumption",
    "preference",
    "evidence",
    "conflict",
    "noise",
}

DEFAULT_STATE: dict[str, Any] = {
    "schema_version": "2.0",
    "product_summary": "",
    "target_users": [],
    "core_problem": "",
    "primary_workflow": "",
    "confirmed_facts": [],
    "assumptions": [],
    "requirements": [],
    "non_goals": [],
    "mvp_scope": [],
    "backlog": [],
    "rejected_items": [],
    "conflicts": [],
    "decisions": [],
    "evidence": [],
    "engineering_risks": [],
    "operability_gaps": [
        "/health/live not specified",
        "/health/ready not specified",
        "/version not specified",
        "structured logs not specified",
        "backup and restore verification not specified",
        "rollback path not specified",
    ],
    "test_plan": [],
    "next_question": "",
    "maturity_level": "Chaos",
    "created_at": "",
    "updated_at": "",
}


def now() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat()


def state_root(root: Path) -> Path:
    return root / "docs" / "product-state"


def state_path(root: Path) -> Path:
    return state_root(root) / "product_state.json"


def fragments_path(root: Path) -> Path:
    return state_root(root) / "fragments.jsonl"


def decisions_path(root: Path) -> Path:
    return state_root(root) / "decisions.jsonl"


def scorecard_path(root: Path) -> Path:
    return state_root(root) / "scorecard.md"


def load_state(root: Path) -> dict[str, Any]:
    path = state_path(root)
    if not path.exists():
        raise SystemExit("No Product State found. Run 'init' first.")
    return migrate_state(json.loads(path.read_text(encoding="utf-8")))


def migrate_state(state: dict[str, Any]) -> dict[str, Any]:
    for key, value in DEFAULT_STATE.items():
        if key not in state:
            state[key] = list(value) if isinstance(value, list) else value
    for field in LIST_FIELDS:
        if not isinstance(state.get(field), list):
            state[field] = []
    for field in SCALAR_FIELDS:
        if not isinstance(state.get(field), str):
            state[field] = ""
    state["schema_version"] = DEFAULT_STATE["schema_version"]
    return state


def save_state(root: Path, state: dict[str, Any]) -> None:
    state["updated_at"] = now()
    state_path(root).write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_scorecard(root, state)


def ensure_state(root: Path) -> dict[str, Any]:
    state_root(root).mkdir(parents=True, exist_ok=True)
    path = state_path(root)
    if path.exists():
        state = migrate_state(json.loads(path.read_text(encoding="utf-8")))
    else:
        state = dict(DEFAULT_STATE)
        timestamp = now()
        state["created_at"] = timestamp
        state["updated_at"] = timestamp
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fragments_path(root).touch(exist_ok=True)
    decisions_path(root).touch(exist_ok=True)
    write_scorecard(root, state)
    return state


def append_unique(values: list[Any], value: Any) -> None:
    if value in values:
        return
    values.append(value)


def ensure_field(field: str) -> None:
    if field not in SCALAR_FIELDS and field not in LIST_FIELDS:
        valid = ", ".join(sorted(SCALAR_FIELDS | LIST_FIELDS))
        raise SystemExit(f"Unknown field '{field}'. Valid fields: {valid}")


def apply_update(state: dict[str, Any], field: str, value: Any) -> None:
    ensure_field(field)
    if field in SCALAR_FIELDS:
        state[field] = value
    else:
        append_unique(state.setdefault(field, []), value)


def infer_maturity(state: dict[str, Any]) -> str:
    has_shape = bool(state.get("target_users") and state.get("core_problem") and state.get("primary_workflow"))
    has_spec = bool(has_shape and state.get("mvp_scope") and state.get("non_goals") and state.get("requirements"))
    has_buildable = bool(has_spec and state.get("engineering_risks") and state.get("test_plan"))
    has_releasable = bool(has_buildable and not state.get("operability_gaps"))
    if has_releasable:
        return "Releasable"
    if has_buildable and has_spec:
        return "Buildable"
    if has_spec:
        return "Spec"
    if has_shape:
        return "Shape"
    return "Chaos"


def write_scorecard(root: Path, state: dict[str, Any]) -> None:
    inferred = infer_maturity(state)
    lines = [
        "# Product State Scorecard",
        "",
        f"- Stored maturity: {state.get('maturity_level', 'Chaos')}",
        f"- Inferred maturity: {inferred}",
        f"- Product: {state.get('product_summary') or 'unknown'}",
        f"- Core problem: {state.get('core_problem') or 'unknown'}",
        f"- Primary workflow: {state.get('primary_workflow') or 'unknown'}",
        f"- Next question: {state.get('next_question') or 'none'}",
        "",
        "| Area | Count |",
        "|---|---:|",
    ]
    for field in [
        "target_users",
        "confirmed_facts",
        "assumptions",
        "requirements",
        "non_goals",
        "mvp_scope",
        "backlog",
        "conflicts",
        "decisions",
        "evidence",
        "engineering_risks",
        "operability_gaps",
        "test_plan",
    ]:
        lines.append(f"| {field} | {len(state.get(field, []))} |")
    lines.extend(["", "## Operability Gaps", ""])
    gaps = state.get("operability_gaps", [])
    lines.extend([f"- {gap}" for gap in gaps] or ["- none"])
    scorecard_path(root).write_text("\n".join(lines) + "\n", encoding="utf-8")


def current_change_id(root: Path) -> str | None:
    path = root / "docs" / "changes" / "current.md"
    if not path.exists():
        return None
    match = re.search(r"Active change:\s*`([^`]+)`", path.read_text(encoding="utf-8", errors="ignore"))
    return match.group(1) if match else None


def architecture_hardening_passed(root: Path) -> bool:
    change_id = current_change_id(root)
    if not change_id:
        return False
    path = root / "docs" / "changes" / change_id / "architecture-hardening.md"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return "Status: PASS" in text


def parse_updates(values: list[str] | None) -> dict[str, str]:
    updates: dict[str, str] = {}
    for item in values or []:
        if "=" not in item:
            raise SystemExit(f"Invalid update '{item}'. Use key=value.")
        key, value = item.split("=", 1)
        updates[key.strip()] = value.strip()
    return updates


def missing_for_level(state: dict[str, Any], level: str) -> list[str]:
    missing: list[str] = []
    normalized = level.lower()
    if normalized in {"shape", "spec", "buildable", "releasable", "operable"}:
        if not state.get("target_users"):
            missing.append("target_users")
        if not state.get("core_problem"):
            missing.append("core_problem")
        if not state.get("primary_workflow"):
            missing.append("primary_workflow")
    if normalized in {"spec", "buildable", "releasable", "operable"}:
        if not state.get("requirements"):
            missing.append("requirements")
        if not state.get("mvp_scope"):
            missing.append("mvp_scope")
        if not state.get("non_goals"):
            missing.append("non_goals")
    if normalized in {"buildable", "releasable", "operable"}:
        if not state.get("engineering_risks"):
            missing.append("engineering_risks")
        if not state.get("test_plan"):
            missing.append("test_plan")
    if normalized in {"releasable", "operable"} and state.get("operability_gaps"):
        missing.append("operability_gaps must be empty")
    return missing


def remove_gap_containing(state: dict[str, Any], needles: list[str]) -> int:
    gaps = state.get("operability_gaps", [])
    before = len(gaps)
    state["operability_gaps"] = [
        gap for gap in gaps
        if not any(needle.lower() in gap.lower() for needle in needles)
    ]
    return before - len(state["operability_gaps"])


def remove_values_containing(values: list[Any], needles: list[str]) -> int:
    before = len(values)
    values[:] = [
        value for value in values
        if not any(needle.lower() in str(value).lower() for needle in needles)
    ]
    return before - len(values)


def extract_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        return ""
    body = text[start + len(marker):]
    next_heading = body.find("\n## ")
    if next_heading >= 0:
        body = body[:next_heading]
    return body.strip()


def command_init(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    state = ensure_state(root)
    print(f"Initialized Product State: {state_path(root)}")
    print(f"Maturity: {state.get('maturity_level')}")


def command_status(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    state = load_state(root)
    inferred = infer_maturity(state)
    print("## Product State")
    print(f"- Stored maturity: {state.get('maturity_level', 'Chaos')}")
    print(f"- Inferred maturity: {inferred}")
    print(f"- Product: {state.get('product_summary') or 'unknown'}")
    print(f"- Core problem: {state.get('core_problem') or 'unknown'}")
    print(f"- Primary workflow: {state.get('primary_workflow') or 'unknown'}")
    print(f"- Next question: {state.get('next_question') or 'none'}")
    print("")
    print("| Field | Count |")
    print("|---|---:|")
    for field in sorted(LIST_FIELDS):
        print(f"| {field} | {len(state.get(field, []))} |")
    gaps = state.get("operability_gaps", [])
    if gaps:
        print("")
        print("## Operability Gaps")
        for gap in gaps:
            print(f"- {gap}")


def command_brief(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    state = load_state(root)
    inferred = infer_maturity(state)
    gaps = state.get("operability_gaps", [])
    conflicts = state.get("conflicts", [])
    main_gap = gaps[0] if gaps else "none"
    next_action = state.get("next_question") or (
        "Resolve the main operability gap before release." if gaps else "Use the smallest next artifact or gate."
    )
    if args.json:
        payload = {
            "stored_maturity": state.get("maturity_level", "Chaos"),
            "inferred_maturity": inferred,
            "product": state.get("product_summary") or "unknown",
            "core_problem": state.get("core_problem") or "unknown",
            "primary_workflow": state.get("primary_workflow") or "unknown",
            "main_gap": main_gap,
            "counts": {
                "requirements": len(state.get("requirements", [])),
                "risks": len(state.get("engineering_risks", [])),
                "gaps": len(gaps),
                "conflicts": len(conflicts),
            },
            "next_action": next_action,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print("## Product State Brief")
    print(f"- Maturity: {state.get('maturity_level', 'Chaos')} (inferred: {inferred})")
    print(f"- Product: {state.get('product_summary') or 'unknown'}")
    print(f"- Core problem: {state.get('core_problem') or 'unknown'}")
    print(f"- Primary workflow: {state.get('primary_workflow') or 'unknown'}")
    print(
        "- Counts: "
        f"requirements={len(state.get('requirements', []))}, "
        f"risks={len(state.get('engineering_risks', []))}, "
        f"gaps={len(gaps)}, "
        f"conflicts={len(conflicts)}"
    )
    print(f"- Main gap: {main_gap}")
    print(f"- Next action: {next_action}")


def command_set(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    state = load_state(root)
    apply_update(state, args.field, args.value)
    if args.field != "maturity_level":
        state["maturity_level"] = infer_maturity(state)
    save_state(root, state)
    print(f"Set {args.field}: {args.value}")


def command_add(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    state = load_state(root)
    if args.field not in LIST_FIELDS:
        raise SystemExit(f"'{args.field}' is not a list field.")
    append_unique(state.setdefault(args.field, []), args.value)
    state["maturity_level"] = infer_maturity(state)
    save_state(root, state)
    print(f"Added to {args.field}: {args.value}")


def command_capture(args: argparse.Namespace) -> None:
    if args.type not in VALID_FRAGMENT_TYPES:
        raise SystemExit(f"Invalid fragment type '{args.type}'.")
    if args.evidence not in VALID_EVIDENCE_LEVELS:
        raise SystemExit(f"Invalid evidence level '{args.evidence}'.")
    root = Path(args.root).resolve()
    state = ensure_state(root)
    entry = {
        "timestamp": now(),
        "raw_text": args.raw,
        "interpreted_meaning": args.meaning,
        "fragment_type": args.type,
        "confidence": args.confidence,
        "evidence_level": args.evidence,
        "product_area": args.area or "",
        "state_updates": parse_updates(args.updates),
        "conflicts_with": args.conflicts_with or "",
        "requires_clarification": bool(args.requires_clarification),
    }
    with fragments_path(root).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")

    meaning = args.meaning.strip()
    if meaning and args.evidence == "confirmed":
        append_unique(state["confirmed_facts"], meaning)
    elif meaning and args.evidence == "assumption":
        append_unique(state["assumptions"], meaning)
    elif meaning and args.evidence == "evidence":
        append_unique(state["evidence"], meaning)
    elif meaning and args.evidence == "conflict":
        append_unique(state["conflicts"], meaning)
    elif meaning and args.evidence == "preference":
        append_unique(state["backlog"], meaning)

    if meaning and args.type == "requirement" and args.evidence == "confirmed":
        append_unique(state["requirements"], meaning)
    if meaning and args.type == "risk":
        append_unique(state["engineering_risks"], meaning)
    if meaning and args.type == "incident":
        append_unique(state["operability_gaps"], f"Incident follow-up needed: {meaning}")
    for field, value in entry["state_updates"].items():
        apply_update(state, field, value)
    if args.requires_clarification and not state.get("next_question"):
        state["next_question"] = "Clarify the largest unknown before advancing maturity."
    state["maturity_level"] = infer_maturity(state)
    save_state(root, state)
    print(f"Captured {args.type} fragment: {fragments_path(root)}")
    print(f"Maturity: {state['maturity_level']}")


def command_decision(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    state = ensure_state(root)
    entry = {
        "timestamp": now(),
        "decision": args.decision,
        "reason": args.reason or "",
        "alternatives": args.alternatives or "",
        "impact": args.impact or "",
        "review_at": args.review_at or "",
    }
    with decisions_path(root).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    append_unique(state["decisions"], entry)
    state["maturity_level"] = infer_maturity(state)
    save_state(root, state)
    print(f"Recorded decision: {args.decision}")


def command_gap(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    state = ensure_state(root)
    append_unique(state["operability_gaps"], args.text)
    state["maturity_level"] = infer_maturity(state)
    save_state(root, state)
    print(f"Added operability gap: {args.text}")


def command_clear_gap(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    state = load_state(root)
    before = len(state.get("operability_gaps", []))
    state["operability_gaps"] = [gap for gap in state.get("operability_gaps", []) if args.text not in gap]
    after = len(state["operability_gaps"])
    state["maturity_level"] = infer_maturity(state)
    save_state(root, state)
    print(f"Removed {before - after} matching operability gaps.")


def command_promote_maturity(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    state = load_state(root)
    missing = missing_for_level(state, args.level)
    if args.level == "Operable" and not architecture_hardening_passed(root):
        missing.append("architecture hardening review must PASS")
    if missing and not args.force:
        print(f"Cannot promote to {args.level}. Missing:")
        for item in missing:
            print(f"- {item}")
        raise SystemExit(1)
    state["maturity_level"] = args.level
    save_state(root, state)
    print(f"Promoted maturity to {args.level}")


def command_reconcile(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    state = ensure_state(root)
    change = root / "docs" / "changes" / args.change_id
    if not change.exists():
        raise SystemExit(f"Change folder not found: {change}")

    prd_path = change / "prd.md"
    tech_path = change / "tech-verification.md"
    design_path = change / "technical-design.md"
    task_path = change / "task-list.md"
    notes_path = change / "implementation-notes.md"
    self_test_path = change / "self-test.md"
    release_test_path = change / "release-test-report.md"
    backup_verify_path = change / "backup-restore-verification.md"
    release_gate_path = change / "release-gate.md"

    prd = prd_path.read_text(encoding="utf-8") if prd_path.exists() else ""
    tech = tech_path.read_text(encoding="utf-8") if tech_path.exists() else ""
    design = design_path.read_text(encoding="utf-8") if design_path.exists() else ""
    tasks = task_path.read_text(encoding="utf-8") if task_path.exists() else ""
    notes = notes_path.read_text(encoding="utf-8") if notes_path.exists() else ""
    self_test = self_test_path.read_text(encoding="utf-8") if self_test_path.exists() else ""
    release_test = release_test_path.read_text(encoding="utf-8") if release_test_path.exists() else ""
    backup_verify = backup_verify_path.read_text(encoding="utf-8") if backup_verify_path.exists() else ""
    release_gate = release_gate_path.read_text(encoding="utf-8") if release_gate_path.exists() else ""

    if "想法收集器" in prd:
        state["product_summary"] = "想法收集器：自动读取 PC 端微信/QQ 本地聊天记录并建立本地搜索索引，用于找回散乱想法。"
    elif prd.startswith("# PRD:"):
        state["product_summary"] = prd.splitlines()[0].replace("# PRD:", "").strip()

    if "单人自用" in prd:
        append_unique(state["target_users"], "单人开发者")
    if "碎片化想法" in prd or "经常找不到" in prd:
        state["core_problem"] = "有价值的想法散落在微信、QQ等聊天记录中，缺少统一检索入口，事后难以回溯。"
    if "打开工具" in prd and "搜索关键词" in prd:
        state["primary_workflow"] = "打开工具 -> 同步本地聊天数据库 -> 搜索关键词/筛选联系人和时间 -> 查看消息上下文。"

    for item in [
        "读取 PC 微信本地数据库并提取文本消息",
        "读取 PC QQ 本地数据库并提取文本消息",
        "将消息写入本地 SQLite FTS5 索引",
        "提供关键词搜索、联系人过滤、时间范围过滤和上下文查看",
    ]:
        append_unique(state["requirements"], item)

    for item in [
        "v0 不做实时同步、云端存储、移动端、AI分类、多人协作、消息编辑/删除、聊天客户端、跨设备同步",
    ]:
        append_unique(state["non_goals"], item)

    append_unique(
        state["mvp_scope"],
        "Windows 本地单人工具：手动同步微信/QQ聊天数据库，建立只读索引，支持全文检索和上下文查看。",
    )

    for item in [
        "实时监听新消息",
        "移动端",
        "AI智能分类标签",
        "云同步",
        "多人协作",
    ]:
        append_unique(state["backlog"], item)

    if "QQ NT 的数据库为**未加密 SQLite**" in tech and "QQ 数据库加密" in notes:
        append_unique(
            state["conflicts"],
            "技术验证曾判断 QQ NT 未加密可直接读取；实现阶段发现本机 QQ NT 数据页加密，需要 qq-win-db-key/SQLCipher 密钥流程。",
        )
    if "微信版本更新" in prd or "微信版本更新" in tech:
        append_unique(state["engineering_risks"], "微信版本更新可能导致内存密钥扫描或数据库解密失效。")
    if "QQ 数据库加密" in notes:
        append_unique(state["engineering_risks"], "QQ NT 数据库加密状态与版本/账号环境有关，需要密钥提取流程和失败提示。")
    if "SQLCipher Python 绑定安装困难" in design or "sqlcipher CLI" in notes:
        append_unique(state["engineering_risks"], "SQLCipher 依赖在 Windows 上安装/分发困难，v0 依赖外部 CLI 或密钥工具。")

    if "/health/live" in notes or "/health/live" in design:
        remove_gap_containing(state, ["/health/live"])
    if "/health/ready" in notes or "/health/ready" in design:
        remove_gap_containing(state, ["/health/ready"])
    if "/version" in notes or "/version" in design:
        remove_gap_containing(state, ["/version"])
    if "JSON 结构化日志" in notes or "JSON 格式结构化日志" in notes or "结构化日志" in design:
        remove_gap_containing(state, ["structured logs"])
    if "索引DB可删除重建" in notes or "索引数据库 (`idea_collector.db`) 可随时删除重建" in notes:
        remove_gap_containing(state, ["rollback path"])
    if "无外部监控，本地查看日志文件即可" in design:
        append_unique(state["confirmed_facts"], "v0 采用本地日志查看作为最低监控/巡检方式。")

    if "Tests — v0 暂未写测试" in notes or "Tests — 阻断 Releasable" in notes:
        append_unique(state["test_plan"], "补齐最小测试：健康端点、版本端点、搜索 API、上下文弹窗关闭、空数据库同步、路径错误提示。")
        append_unique(state["engineering_risks"], "当前实现缺少自动化测试，发布前不能升级为 Releasable。")
        if not (self_test or release_test):
            append_unique(state["operability_gaps"], "release test evidence not recorded")
    elif tasks:
        append_unique(state["test_plan"], "按任务清单 T13 进行端到端联调：启动、同步、搜索、查看上下文、错误处理。")

    if self_test or release_test:
        artifact_name = "release-test-report.md" if release_test else "self-test.md"
        append_unique(state["evidence"], f"Release test artifact recorded: {artifact_name}")
    if backup_verify and ("PASS" in backup_verify or "通过" in backup_verify):
        append_unique(state["evidence"], "Backup/restore verification artifact recorded.")

    remove_values_containing(state["confirmed_facts"], ["Release Gate: PASS", "Implementation Gate: PASS, Release Gate: PASS"])
    if "Status: PASS" in release_gate and state.get("operability_gaps"):
        append_unique(
            state["conflicts"],
            "release-gate.md claims PASS while Product State still has operability gaps; rerun workflow_gate.py start-release and trust the command result.",
        )

    state["maturity_level"] = infer_maturity(state)
    save_state(root, state)
    print(f"Reconciled Product State from {change}")
    print(f"Maturity: {state['maturity_level']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Product State for conversation-to-operable-product work.")
    parser.add_argument("--root", default=".", help="Project root. Defaults to current directory.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init").set_defaults(func=command_init)
    brief = sub.add_parser("brief")
    brief.add_argument("--json", action="store_true")
    brief.set_defaults(func=command_brief)
    sub.add_parser("status").set_defaults(func=command_status)

    set_cmd = sub.add_parser("set")
    set_cmd.add_argument("field")
    set_cmd.add_argument("value")
    set_cmd.set_defaults(func=command_set)

    add_cmd = sub.add_parser("add")
    add_cmd.add_argument("field")
    add_cmd.add_argument("value")
    add_cmd.set_defaults(func=command_add)

    capture = sub.add_parser("capture")
    capture.add_argument("--type", required=True)
    capture.add_argument("--evidence", default="assumption")
    capture.add_argument("--raw", required=True)
    capture.add_argument("--meaning", required=True)
    capture.add_argument("--confidence", default="medium")
    capture.add_argument("--area")
    capture.add_argument("--updates", action="append")
    capture.add_argument("--conflicts-with")
    capture.add_argument("--requires-clarification", action="store_true")
    capture.set_defaults(func=command_capture)

    decision = sub.add_parser("decision")
    decision.add_argument("decision")
    decision.add_argument("--reason")
    decision.add_argument("--alternatives")
    decision.add_argument("--impact")
    decision.add_argument("--review-at")
    decision.set_defaults(func=command_decision)

    gap = sub.add_parser("gap")
    gap.add_argument("text")
    gap.set_defaults(func=command_gap)

    clear_gap = sub.add_parser("clear-gap")
    clear_gap.add_argument("text")
    clear_gap.set_defaults(func=command_clear_gap)

    resolve_gap = sub.add_parser("resolve-gap")
    resolve_gap.add_argument("text")
    resolve_gap.set_defaults(func=command_clear_gap)

    promote = sub.add_parser("promote-maturity")
    promote.add_argument("level", choices=["Chaos", "Shape", "Spec", "Buildable", "Releasable", "Operable"])
    promote.add_argument("--force", action="store_true")
    promote.set_defaults(func=command_promote_maturity)

    reconcile = sub.add_parser("reconcile")
    reconcile.add_argument("--change-id", required=True)
    reconcile.set_defaults(func=command_reconcile)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
