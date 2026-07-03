#!/usr/bin/env python3
"""Hard workflow gates for conversation-to-operable-product projects."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


REQUIRED_IMPLEMENTATION_STATE = [
    "product_summary",
    "target_users",
    "core_problem",
    "primary_workflow",
    "requirements",
    "non_goals",
    "mvp_scope",
    "engineering_risks",
    "test_plan",
]

REQUIRED_IMPLEMENTATION_ARTIFACTS = [
    "prd.md",
    "technical-design.md",
    "task-list.md",
]

REQUIRED_RELEASE_ARTIFACTS = [
    "implementation-gate.md",
    "implementation-notes.md",
]

RELEASE_TEST_ARTIFACTS = [
    "release-test-report.md",
    "self-test.md",
]

ARCHITECTURE_HARDENING_ARTIFACT = "architecture-hardening.md"

ARCHITECTURE_HARDENING_DIMENSIONS = [
    "Search Scale",
    "Sync Accuracy",
    "Dependency Fallback",
    "Migration",
    "Config Consistency",
    "Real Sample Verification",
]

ARCHITECTURE_HARDENING_INCOMPLETE_MARKERS = [
    "[ ]",
    "todo",
    "tbd",
    "unknown",
    "not verified",
    "not tested",
    "unverified",
]

DRIFT_DOC_FILES = [
    "prd.md",
    "tech-verification.md",
    "technical-design.md",
    "task-list.md",
    "implementation-notes.md",
    "self-test.md",
]

STALE_FTS5_CURRENT_CLAIMS = [
    "SQLite FTS5 统一索引",
    "SQLite FTS5 全文索引",
    "写入 FTS5 索引",
    "更新 FTS5 索引",
    "idea_collector.db (SQLite FTS5)",
    "SQLite FTS5 数据库初始化",
    "FTS5 全文搜索",
    "FTS5 查询构建",
    "将消息写入本地 SQLite FTS5 索引",
    "Python+FastAPI+SQLite FTS5",
]


def now() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat()


def changes_root(root: Path) -> Path:
    return root / "docs" / "changes"


def current_file(root: Path) -> Path:
    return changes_root(root) / "current.md"


def state_file(root: Path) -> Path:
    return root / "docs" / "product-state" / "product_state.json"


def read_current_change(root: Path) -> str:
    path = current_file(root)
    if not path.exists():
        raise SystemExit("No docs/changes/current.md found.")
    match = re.search(r"Active change:\s*`([^`]+)`", path.read_text(encoding="utf-8"))
    if not match:
        raise SystemExit("Could not parse active change from docs/changes/current.md.")
    return match.group(1)


def resolve_change(root: Path, change_id: str | None) -> str:
    active = read_current_change(root)
    if change_id and change_id != active:
        raise SystemExit(f"Requested change {change_id} does not match active change {active}.")
    return change_id or active


def change_dir(root: Path, change_id: str) -> Path:
    path = changes_root(root) / change_id
    if not path.exists():
        raise SystemExit(f"Change directory not found: {path}")
    return path


def load_state(root: Path) -> dict[str, Any]:
    path = state_file(root)
    if not path.exists():
        raise SystemExit("No Product State found. Run product_state_store.py init first.")
    return json.loads(path.read_text(encoding="utf-8"))


def is_present(value: Any) -> bool:
    if isinstance(value, list):
        return len(value) > 0
    return bool(value)


def missing_state_fields(state: dict[str, Any], fields: list[str]) -> list[str]:
    return [field for field in fields if not is_present(state.get(field))]


def missing_artifacts(path: Path, filenames: list[str]) -> list[str]:
    return [name for name in filenames if not (path / name).exists()]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def contains_any(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle.lower() in lowered for needle in needles)


def first_existing(path: Path, filenames: list[str]) -> Path | None:
    for name in filenames:
        candidate = path / name
        if candidate.exists():
            return candidate
    return None


def project_text_for_release(state: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in ["product_summary", "core_problem", "primary_workflow"]:
        value = state.get(key)
        if isinstance(value, str):
            parts.append(value)
    for key in ["requirements", "mvp_scope", "engineering_risks"]:
        value = state.get(key, [])
        if isinstance(value, list):
            parts.extend(str(item) for item in value)
    return "\n".join(parts)


def has_python_project(root: Path) -> bool:
    candidates = [root / "pyproject.toml", *root.glob("*/pyproject.toml")]
    return any(path.exists() for path in candidates)


def python_project_roots(root: Path) -> list[Path]:
    candidates = [root / "pyproject.toml", *root.glob("*/pyproject.toml")]
    return [path.parent for path in candidates if path.exists()]


def project_uses_sqlite_wal(root: Path) -> bool:
    for path in root.glob("**/*.py"):
        parts = {part.lower() for part in path.parts}
        if any(part in parts for part in {".venv", "venv", "__pycache__", "node_modules"}):
            continue
        try:
            if "journal_mode=WAL" in path.read_text(encoding="utf-8", errors="ignore"):
                return True
        except OSError:
            continue
    return False


def iter_project_python_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.glob("**/*.py"):
        parts = {part.lower() for part in path.parts}
        if any(part in parts for part in {".venv", "venv", "__pycache__", "node_modules"}):
            continue
        files.append(path)
    return files


def code_uses_fts5(root: Path) -> bool:
    for path in iter_project_python_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        if "create virtual table" in text and "fts5" in text:
            return True
        if "messages_fts" in text or " fts5" in text or "fts5(" in text:
            return True
    return False


def code_uses_sql_like_search(root: Path) -> bool:
    for path in iter_project_python_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if " LIKE ?" in text and "content" in text and "search" in path.name.lower():
            return True
    return False


def doc_code_drift_blockers(root: Path, cdir: Path) -> list[str]:
    blockers: list[str] = []
    state_text = read_text(state_file(root))
    docs: list[tuple[str, str]] = []
    for name in DRIFT_DOC_FILES:
        docs.append((name, read_text(cdir / name)))
    docs.append(("docs/product-state/product_state.json", state_text))

    if code_uses_sql_like_search(root) and not code_uses_fts5(root):
        for filename, text in docs:
            stale = [claim for claim in STALE_FTS5_CURRENT_CLAIMS if claim in text]
            if stale:
                shown = "; ".join(stale[:3])
                if len(stale) > 3:
                    shown += f"; +{len(stale) - 3} more"
                blockers.append(
                    f"Doc/code drift: code uses SQL LIKE search, but {filename} still claims current FTS5 implementation ({shown})."
                )
    return blockers


def release_test_blockers(root: Path, cdir: Path, state: dict[str, Any]) -> list[str]:
    artifact = first_existing(cdir, RELEASE_TEST_ARTIFACTS)
    if not artifact:
        names = " or ".join(RELEASE_TEST_ARTIFACTS)
        return [f"Release artifact missing: {names}"]

    text = read_text(artifact)
    blockers: list[str] = []
    if not contains_any(text, ["pass", "passed", "通过", "[x]"]):
        blockers.append(f"Release test evidence is not marked PASS: {artifact.name}")

    project_text = project_text_for_release(state)
    needs_search_positive_path = contains_any(project_text, ["search", "搜索", "检索", "索引"])
    needs_chinese_check = contains_any(project_text, ["微信", "QQ", "聊天", "中文", "CJK"])
    has_api_or_ui = contains_any(text + "\n" + project_text, ["/api", "api", "frontend", "前端", "页面", "浏览器"])

    if needs_search_positive_path and not contains_any(
        text,
        ["positive", "non-empty", "fixture", "seed", "search hit", "returns 1", "命中", "非空", "种子", "夹具", "有数据"],
    ):
        blockers.append(f"Release test evidence lacks a positive non-empty data path: {artifact.name}")

    if needs_chinese_check and not contains_any(text, ["中文", "Chinese", "CJK", "分词", "tokenization", "命中"]):
        blockers.append(f"Release test evidence lacks Chinese/domain text search coverage: {artifact.name}")

    if has_api_or_ui and not contains_any(text, ["contract", "payload", "request body", "response body", "前后端", "契约", "请求体", "响应体"]):
        blockers.append(f"Release test evidence lacks API/UI contract coverage: {artifact.name}")

    if has_python_project(root) and not contains_any(text, ["pytest", "py -3 -m pytest", "python -m pytest", "自动化测试"]):
        blockers.append(f"Release test evidence lacks an automated pytest command or explicit equivalent: {artifact.name}")

    return blockers


def pytest_blockers(root: Path) -> list[str]:
    blockers: list[str] = []
    for project_root in python_project_roots(root):
        tests_dir = project_root / "tests"
        if not tests_dir.exists():
            continue
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-q"],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            blockers.append(f"Automated pytest timed out after 30s: {project_root}")
            continue
        output = (result.stdout + "\n" + result.stderr).strip()
        summary = output.splitlines()[-1] if output else f"exit code {result.returncode}"
        if result.returncode != 0:
            blockers.append(f"Automated pytest failed in {project_root}: {summary}")
    return blockers


def backup_blockers(root: Path, cdir: Path) -> list[str]:
    artifact = cdir / "backup-restore-verification.md"
    if not artifact.exists():
        return ["Release artifact missing: backup-restore-verification.md"]

    text = read_text(artifact)
    blockers: list[str] = []
    if not contains_any(text, ["pass", "通过", "[x]"]):
        blockers.append("Backup/restore verification is not marked PASS.")
    if project_uses_sqlite_wal(root) and not contains_any(text, ["wal", "checkpoint", "sqlite backup", "sqlite_backup", "backup api"]):
        blockers.append("SQLite WAL project requires checkpoint or SQLite backup API evidence.")
    return blockers


def remove_hardening_gate_block(text: str) -> str:
    pattern = re.compile(
        r"<!-- workflow_gate:architecture-hardening:start -->.*?<!-- workflow_gate:architecture-hardening:end -->\s*",
        re.DOTALL,
    )
    return pattern.sub("", text).lstrip()


def default_hardening_review_body() -> str:
    lines = ["## Review Evidence", ""]
    for dimension in ARCHITECTURE_HARDENING_DIMENSIONS:
        lines.extend([
            f"## {dimension}",
            "",
            "- [ ] PASS or N/A:",
            "- Evidence:",
            "- Follow-up:",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def extract_markdown_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+.*{re.escape(heading)}.*$",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end]


def architecture_hardening_blockers(cdir: Path) -> list[str]:
    artifact = cdir / ARCHITECTURE_HARDENING_ARTIFACT
    if not artifact.exists():
        return [f"Architecture hardening artifact missing: {ARCHITECTURE_HARDENING_ARTIFACT}"]

    text = remove_hardening_gate_block(read_text(artifact))
    blockers: list[str] = []
    if contains_any(text, ["status: fail", "status: blocked", " fail", "failed", "阻断"]):
        blockers.append("Architecture hardening review contains an explicit FAIL/BLOCKED marker.")

    for dimension in ARCHITECTURE_HARDENING_DIMENSIONS:
        section = extract_markdown_section(text, dimension)
        if not section.strip():
            blockers.append(f"Architecture hardening dimension missing: {dimension}")
            continue
        lowered = section.lower()
        if not contains_any(section, ["[x]", "status: pass", "status: n/a", "pass", "n/a"]):
            blockers.append(f"Architecture hardening dimension is not marked PASS/N/A: {dimension}")
        if any(marker in lowered for marker in ARCHITECTURE_HARDENING_INCOMPLETE_MARKERS):
            blockers.append(f"Architecture hardening dimension still has incomplete evidence: {dimension}")
    return blockers


def write_architecture_hardening_gate(path: Path, change_id: str, blockers: list[str], body: str) -> None:
    status = "PASS" if not blockers else "BLOCKED"
    lines = [
        "<!-- workflow_gate:architecture-hardening:start -->",
        "# Architecture Hardening Review",
        "",
        f"- Status: {status}",
        f"- Updated: {now()}",
        f"- Change: `{change_id}`",
        "",
        *render_list("Blockers", blockers),
        "<!-- workflow_gate:architecture-hardening:end -->",
        "",
        body.rstrip() or default_hardening_review_body().rstrip(),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_gate(path: Path, title: str, status: str, lines: list[str]) -> None:
    content = [
        f"# {title}",
        "",
        f"- Status: {status}",
        f"- Updated: {now()}",
        "",
        *lines,
        "",
    ]
    path.write_text("\n".join(content), encoding="utf-8")


def render_list(title: str, items: list[str]) -> list[str]:
    if not items:
        return [f"## {title}", "", "- none", ""]
    return [f"## {title}", "", *[f"- {item}" for item in items], ""]


def implementation_checklist(intent: str) -> list[str]:
    return [
        "## Intent",
        "",
        f"- {intent}",
        "",
        "## Required Checks",
        "",
        "- [ ] Scope still matches Product State and PRD",
        "- [ ] Active change id confirmed",
        "- [ ] Env vars and .env.example checked",
        "- [ ] Migrations/schema impact checked",
        "- [ ] Secrets/data/log files excluded",
        "- [ ] /health/live, /health/ready, /version impact checked",
        "- [ ] Structured logs checked",
        "- [ ] Test plan updated",
        "- [ ] Rollback path documented",
        "- [ ] Product State reconcile will run after implementation",
        "",
    ]


def command_start_implementation(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    change_id = resolve_change(root, args.change_id)
    cdir = change_dir(root, change_id)
    state = load_state(root)
    missing_state = missing_state_fields(state, REQUIRED_IMPLEMENTATION_STATE)
    missing_files = missing_artifacts(cdir, REQUIRED_IMPLEMENTATION_ARTIFACTS)
    blockers = []
    blockers.extend([f"Product State missing: {item}" for item in missing_state])
    blockers.extend([f"Artifact missing: {item}" for item in missing_files])
    if state.get("maturity_level") not in {"Buildable", "Releasable", "Operable"}:
        blockers.append(f"Maturity is {state.get('maturity_level', 'unknown')}, expected Buildable or above.")

    gate_path = cdir / "implementation-gate.md"
    lines = [
        f"- Change: `{change_id}`",
        f"- Product: {state.get('product_summary') or 'unknown'}",
        f"- Maturity: {state.get('maturity_level') or 'unknown'}",
        "",
        *implementation_checklist(args.intent),
        *render_list("Blockers", blockers),
    ]
    status = "PASS" if not blockers else "BLOCKED"
    write_gate(gate_path, "Implementation Gate", status, lines)
    print(f"Implementation gate written: {gate_path}")
    print(f"Status: {status}")
    if blockers:
        for blocker in blockers:
            print(f"- {blocker}")
        raise SystemExit(1)


def command_implementation_status(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    change_id = resolve_change(root, args.change_id)
    cdir = change_dir(root, change_id)
    gate_path = cdir / "implementation-gate.md"
    if not gate_path.exists():
        raise SystemExit(f"Implementation gate missing: {gate_path}")
    text = gate_path.read_text(encoding="utf-8")
    print(text)
    if "Status: BLOCKED" in text:
        raise SystemExit(1)


def command_complete_implementation(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    change_id = resolve_change(root, args.change_id)
    cdir = change_dir(root, change_id)
    gate_path = cdir / "implementation-gate.md"
    if not gate_path.exists():
        raise SystemExit("Cannot complete implementation: implementation-gate.md is missing.")
    notes_path = cdir / "implementation-notes.md"
    if not notes_path.exists():
        raise SystemExit("Cannot complete implementation: implementation-notes.md is missing.")
    text = gate_path.read_text(encoding="utf-8")
    extra = [
        "",
        "## Completion Evidence",
        "",
        f"- Completed: {now()}",
        f"- Evidence: {args.evidence}",
        "",
    ]
    if "## Completion Evidence" not in text:
        gate_path.write_text(text + "\n".join(extra), encoding="utf-8")
    print(f"Implementation completion recorded: {gate_path}")


def command_start_release(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    change_id = resolve_change(root, args.change_id)
    cdir = change_dir(root, change_id)
    state = load_state(root)
    missing_files = missing_artifacts(cdir, REQUIRED_RELEASE_ARTIFACTS)
    gaps = state.get("operability_gaps", [])
    blockers = []
    blockers.extend([f"Release artifact missing: {item}" for item in missing_files])
    impl_gate = cdir / "implementation-gate.md"
    if impl_gate.exists() and "Status: PASS" not in read_text(impl_gate):
        blockers.append("Implementation gate is not PASS.")
    blockers.extend(doc_code_drift_blockers(root, cdir))
    blockers.extend(release_test_blockers(root, cdir, state))
    blockers.extend(pytest_blockers(root))
    blockers.extend(backup_blockers(root, cdir))
    blockers.extend([f"Operability gap open: {gap}" for gap in gaps])
    if state.get("maturity_level") not in {"Releasable", "Operable"}:
        blockers.append(f"Maturity is {state.get('maturity_level', 'unknown')}; promote-maturity Releasable must pass first.")

    gate_path = cdir / "release-gate.md"
    lines = [
        f"- Change: `{change_id}`",
        f"- Product: {state.get('product_summary') or 'unknown'}",
        f"- Maturity: {state.get('maturity_level') or 'unknown'}",
        "",
        "## Required Checks",
        "",
        "- [ ] Implementation gate passed",
        "- [ ] Docs and Product State match current code facts",
        "- [ ] Release test evidence exists (`self-test.md` or `release-test-report.md`)",
        "- [ ] Positive non-empty core workflow covered",
        "- [ ] Domain text/tokenization covered when relevant",
        "- [ ] API/UI contract covered when relevant",
        "- [ ] Automated test command recorded when relevant",
        "- [ ] Automated pytest command re-executed by release gate when relevant",
        "- [ ] Backup and restore verification exists",
        "- [ ] SQLite WAL/checkpoint handled when relevant",
        "- [ ] Version/artifact/release record exists",
        "- [ ] Rollback path verified",
        "- [ ] Operability gaps empty",
        "",
        *render_list("Blockers", blockers),
    ]
    status = "PASS" if not blockers else "BLOCKED"
    write_gate(gate_path, "Release Gate", status, lines)
    print(f"Release gate written: {gate_path}")
    print(f"Status: {status}")
    if blockers:
        for blocker in blockers:
            print(f"- {blocker}")
        raise SystemExit(1)


def command_status(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    change_id = resolve_change(root, args.change_id)
    cdir = change_dir(root, change_id)
    state = load_state(root)
    print("## Workflow Gate Status")
    print(f"- Change: `{change_id}`")
    print(f"- Maturity: {state.get('maturity_level') or 'unknown'}")
    print(f"- Implementation gate: {'present' if (cdir / 'implementation-gate.md').exists() else 'missing'}")
    print(f"- Release gate: {'present' if (cdir / 'release-gate.md').exists() else 'missing'}")
    hardening = cdir / ARCHITECTURE_HARDENING_ARTIFACT
    hardening_status = "missing"
    if hardening.exists():
        text = read_text(hardening)
        hardening_status = "PASS" if "Status: PASS" in text else "present"
        if "Status: BLOCKED" in text:
            hardening_status = "BLOCKED"
    print(f"- Architecture hardening: {hardening_status}")
    gaps = state.get("operability_gaps", [])
    print(f"- Operability gaps: {len(gaps)}")
    for gap in gaps:
        print(f"  - {gap}")
    release_gate = cdir / "release-gate.md"
    if release_gate.exists() and "Status: PASS" in read_text(release_gate) and gaps:
        print("- Warning: release-gate.md says PASS but Product State still has operability gaps. Re-run start-release.")


def command_drift(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    change_id = resolve_change(root, args.change_id)
    cdir = change_dir(root, change_id)
    blockers = doc_code_drift_blockers(root, cdir)
    print("## Doc/Code Drift")
    print(f"- Change: `{change_id}`")
    if not blockers:
        print("- Status: PASS")
        print("- Drift: none detected")
        return
    print("- Status: BLOCKED")
    print("")
    for blocker in blockers:
        print(f"- {blocker}")
    raise SystemExit(1)


def command_architecture_hardening(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    change_id = resolve_change(root, args.change_id)
    cdir = change_dir(root, change_id)
    artifact = cdir / ARCHITECTURE_HARDENING_ARTIFACT
    existing = remove_hardening_gate_block(read_text(artifact)) if artifact.exists() else default_hardening_review_body()
    blockers = architecture_hardening_blockers(cdir) if artifact.exists() else [
        f"Architecture hardening artifact missing: {ARCHITECTURE_HARDENING_ARTIFACT}"
    ]
    write_architecture_hardening_gate(artifact, change_id, blockers, existing)
    status = "PASS" if not blockers else "BLOCKED"
    print(f"Architecture hardening written: {artifact}")
    print(f"Status: {status}")
    if blockers:
        for blocker in blockers:
            print(f"- {blocker}")
        raise SystemExit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Enforce workflow gates for product-engineering changes.")
    parser.add_argument("--root", default=".", help="Project root. Defaults to current directory.")
    sub = parser.add_subparsers(dest="command", required=True)

    start_impl = sub.add_parser("start-implementation")
    start_impl.add_argument("--change-id")
    start_impl.add_argument("--intent", required=True)
    start_impl.set_defaults(func=command_start_implementation)

    impl_status = sub.add_parser("implementation-status")
    impl_status.add_argument("--change-id")
    impl_status.set_defaults(func=command_implementation_status)

    complete_impl = sub.add_parser("complete-implementation")
    complete_impl.add_argument("--change-id")
    complete_impl.add_argument("--evidence", required=True)
    complete_impl.set_defaults(func=command_complete_implementation)

    release = sub.add_parser("start-release")
    release.add_argument("--change-id")
    release.set_defaults(func=command_start_release)

    status = sub.add_parser("status")
    status.add_argument("--change-id")
    status.set_defaults(func=command_status)

    drift = sub.add_parser("drift")
    drift.add_argument("--change-id")
    drift.set_defaults(func=command_drift)

    hardening = sub.add_parser("architecture-hardening")
    hardening.add_argument("--change-id")
    hardening.set_defaults(func=command_architecture_hardening)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
