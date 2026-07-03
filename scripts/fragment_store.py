#!/usr/bin/env python3
"""Deterministic fragment storage for Solo Product Engineering skills."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


PHASES = {
    "requirement": {
        "label": "需求",
        "file": "requirement-fragments.md",
        "title": "Requirement Fragments",
        "threshold": 5,
        "output": "prd.md",
        "next_skill": "$solo-product-definition-prd",
    },
    "design": {
        "label": "设计",
        "file": "design-fragments.md",
        "title": "Design Fragments",
        "threshold": 3,
        "output": "technical-design.md",
        "next_skill": "$solo-technical-design-adr",
    },
    "task": {
        "label": "任务",
        "file": "task-fragments.md",
        "title": "Task Fragments",
        "threshold": 5,
        "output": "kanban.md",
        "next_skill": "$solo-task-breakdown-kanban",
    },
    "test": {
        "label": "测试",
        "file": "test-fragments.md",
        "title": "Test Fragments",
        "threshold": 3,
        "output": "self-test.md",
        "next_skill": "$solo-self-test-quality-gate",
    },
    "incident": {
        "label": "事故",
        "file": "incident-fragments.md",
        "title": "Incident Fragments",
        "threshold": 1,
        "output": "incident-review.md",
        "next_skill": "$solo-incident-review-improvement",
    },
    "review": {
        "label": "复盘",
        "file": "review-fragments.md",
        "title": "Review Fragments",
        "threshold": 5,
        "output": "weekly-monthly-review.md",
        "next_skill": "$solo-weekly-monthly-review-coach",
    },
    "growth": {
        "label": "成长",
        "file": "growth-fragments.md",
        "title": "Growth Fragments",
        "threshold": 3,
        "output": "growth-roadmap.md",
        "next_skill": "$solo-pm-dev-growth-roadmap",
    },
    "portfolio": {
        "label": "作品",
        "file": "portfolio-fragments.md",
        "title": "Portfolio Fragments",
        "threshold": 3,
        "output": "case-study.md",
        "next_skill": "$solo-portfolio-case-study-builder",
    },
}

ALIASES = {
    "req": "requirement",
    "requirements": "requirement",
    "idea": "requirement",
    "想法": "requirement",
    "需求": "requirement",
    "technical": "design",
    "tech": "design",
    "设计": "design",
    "任务": "task",
    "todo": "task",
    "testing": "test",
    "测试": "test",
    "事故": "incident",
    "故障": "incident",
    "retro": "review",
    "复盘": "review",
    "成长": "growth",
    "学习": "growth",
    "case": "portfolio",
    "作品": "portfolio",
    "案例": "portfolio",
}


def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def today() -> str:
    return dt.date.today().isoformat()


def normalize_phase(value: str) -> str:
    key = value.strip().lower()
    key = ALIASES.get(key, key)
    if key not in PHASES:
        valid = ", ".join(PHASES)
        raise SystemExit(f"Unknown phase '{value}'. Valid phases: {valid}")
    return key


def changes_root(root: Path) -> Path:
    return root / "docs" / "changes"


def current_file(root: Path) -> Path:
    return changes_root(root) / "current.md"


def next_change_id(root: Path) -> str:
    prefix = f"REQ-{dt.date.today().year}-"
    base = changes_root(root)
    max_num = 0
    if base.exists():
        for child in base.iterdir():
            if child.is_dir() and child.name.startswith(prefix):
                match = re.match(rf"{re.escape(prefix)}(\d{{3}})$", child.name)
                if match:
                    max_num = max(max_num, int(match.group(1)))
    return f"{prefix}{max_num + 1:03d}"


def write_current(root: Path, change_id: str) -> None:
    path = current_file(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "# Current Change",
                "",
                f"- Active change: `{change_id}`",
                f"- Updated: {now()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def read_current(root: Path) -> str | None:
    path = current_file(root)
    if not path.exists():
        return None
    match = re.search(r"Active change:\s*`([^`]+)`", path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def change_dir(root: Path, change_id: str | None = None, create: bool = False) -> Path:
    if change_id is None:
        change_id = read_current(root)
    if change_id is None:
        if not create:
            raise SystemExit("No active change. Run 'init' first or pass --change-id.")
        change_id = next_change_id(root)
    path = changes_root(root) / change_id
    if create:
        path.mkdir(parents=True, exist_ok=True)
        write_current(root, change_id)
    return path


def fragment_template(phase: str) -> str:
    info = PHASES[phase]
    return "\n".join(
        [
            f"# {info['title']}",
            "<!-- Last consolidated: never -->",
            "",
            "## Active Fragments",
            "",
            "## Consolidated History",
            "",
        ]
    )


def ensure_change(root: Path, change_id: str | None = None) -> Path:
    path = change_dir(root, change_id, create=True)
    for phase, info in PHASES.items():
        fragment_path = path / info["file"]
        if not fragment_path.exists():
            fragment_path.write_text(fragment_template(phase), encoding="utf-8")
    log_path = path / "consolidation-log.md"
    if not log_path.exists():
        log_path.write_text(
            "\n".join(
                [
                    "# Consolidation Log",
                    "",
                    "| Date | Phase | Fragments Consolidated | Output File |",
                    "|---|---|---:|---|",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
    return path


def active_lines(text: str) -> list[str]:
    match = re.search(r"## Active Fragments\n(?P<body>.*?)(?=\n## |\Z)", text, flags=re.S)
    if not match:
        return []
    return [line for line in match.group("body").splitlines() if line.strip().startswith("- [")]


def set_active_and_archive(text: str, archive_heading: str, lines: list[str]) -> str:
    text = re.sub(
        r"<!-- Last consolidated: .*? -->",
        f"<!-- Last consolidated: {today()} -->",
        text,
        count=1,
    )
    text = re.sub(
        r"## Active Fragments\n.*?(?=\n## |\Z)",
        "## Active Fragments\n",
        text,
        flags=re.S,
    )
    archive = "\n".join(["", archive_heading, *lines, ""])
    if "## Consolidated History" in text:
        return text.replace("## Consolidated History\n", f"## Consolidated History\n{archive}", 1)
    return text.rstrip() + "\n\n## Consolidated History\n" + archive


def command_init(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    path = ensure_change(root, args.change_id)
    print(f"Initialized fragment store: {path}")


def command_capture(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    phase = normalize_phase(args.phase)
    path = ensure_change(root, args.change_id)
    info = PHASES[phase]
    fragment_path = path / info["file"]
    text = fragment_path.read_text(encoding="utf-8")
    entry = f"- [{now()}] {args.text.strip()}"
    if "## Active Fragments" not in text:
        text = fragment_template(phase)
    text = text.replace("## Active Fragments\n", f"## Active Fragments\n{entry}\n", 1)
    fragment_path.write_text(text, encoding="utf-8")
    count = len(active_lines(fragment_path.read_text(encoding="utf-8")))
    status = "ready" if count >= info["threshold"] else "collecting"
    print(f"Captured {info['label']} fragment in {fragment_path}")
    print(f"Active count: {count}/{info['threshold']} ({status})")


def last_consolidated(path: Path) -> str:
    if not path.exists():
        return "never"
    match = re.search(r"<!-- Last consolidated: (.*?) -->", path.read_text(encoding="utf-8"))
    return match.group(1) if match else "never"


def command_status(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    path = change_dir(root, args.change_id, create=False)
    print("## Fragment Status")
    print(f"Change: `{path.name}`")
    print("")
    print("| Phase | Active | Threshold | Last Consolidated | Output | Status |")
    print("|---|---:|---:|---|---|---|")
    for phase, info in PHASES.items():
        fragment_path = path / info["file"]
        count = len(active_lines(fragment_path.read_text(encoding="utf-8"))) if fragment_path.exists() else 0
        state = "ready" if count >= info["threshold"] else "collecting"
        print(
            f"| {info['label']} | {count} | {info['threshold']} | "
            f"{last_consolidated(fragment_path)} | {info['output']} | {state} |"
        )


def command_read(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    path = change_dir(root, args.change_id, create=False)
    phases = [normalize_phase(args.phase)] if args.phase else list(PHASES)
    for phase in phases:
        info = PHASES[phase]
        fragment_path = path / info["file"]
        print(f"## {info['label']} ({info['file']})")
        if not fragment_path.exists():
            print("No fragment file.")
            continue
        lines = active_lines(fragment_path.read_text(encoding="utf-8"))
        if not lines:
            print("No active fragments.")
        else:
            print("\n".join(lines))
        print("")


def command_consolidate(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    phase = normalize_phase(args.phase)
    path = change_dir(root, args.change_id, create=False)
    info = PHASES[phase]
    fragment_path = path / info["file"]
    text = fragment_path.read_text(encoding="utf-8")
    lines = active_lines(text)
    if not lines:
        raise SystemExit(f"No active {info['label']} fragments to consolidate.")
    output_name = args.output or info["output"]
    output_path = path / output_name
    if not output_path.exists():
        output_path.write_text(
            "\n".join(
                [
                    f"# {info['label']} Consolidation Draft",
                    "",
                    f"- Change: `{path.name}`",
                    f"- Phase: {info['label']}",
                    f"- Source fragments: {len(lines)}",
                    f"- Suggested next skill: `{info['next_skill']}`",
                    "",
                    "## Source Fragments",
                    *lines,
                    "",
                    "## Structured Output",
                    "",
                    f"Use {info['next_skill']} to turn these fragments into the final artifact.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    else:
        with output_path.open("a", encoding="utf-8") as handle:
            handle.write("\n\n## New Source Fragments\n")
            handle.write("\n".join(lines))
            handle.write("\n")
    archive_heading = f"### Consolidated on {now()}"
    fragment_path.write_text(set_active_and_archive(text, archive_heading, lines), encoding="utf-8")
    log_path = path / "consolidation-log.md"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"| {today()} | {info['label']} | {len(lines)} | {output_name} |\n")
    print(f"Consolidated {len(lines)} {info['label']} fragments into {output_path}")


def command_diff(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve()
    path = change_dir(root, args.change_id, create=False)
    log_path = path / "consolidation-log.md"
    if not log_path.exists():
        raise SystemExit("No consolidation log found.")
    lines = [line for line in log_path.read_text(encoding="utf-8").splitlines() if line.startswith("| 20")]
    if args.phase:
        phase = PHASES[normalize_phase(args.phase)]["label"]
        lines = [line for line in lines if f"| {phase} |" in line]
    print("## Consolidation History")
    print("\n".join(lines[-2:]) if lines else "No consolidation events.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage solo product-engineering fragments.")
    parser.add_argument("--root", default=".", help="Project root. Defaults to current directory.")
    parser.add_argument("--change-id", help="Change id such as REQ-2026-001.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init").set_defaults(func=command_init)

    capture = sub.add_parser("capture")
    capture.add_argument("phase")
    capture.add_argument("text")
    capture.set_defaults(func=command_capture)

    sub.add_parser("status").set_defaults(func=command_status)

    read = sub.add_parser("read")
    read.add_argument("phase", nargs="?")
    read.set_defaults(func=command_read)

    consolidate = sub.add_parser("consolidate")
    consolidate.add_argument("phase")
    consolidate.add_argument("--output")
    consolidate.set_defaults(func=command_consolidate)

    diff = sub.add_parser("diff")
    diff.add_argument("phase", nargs="?")
    diff.set_defaults(func=command_diff)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
