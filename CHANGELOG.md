# Change Log

## 2026-06-17 Integrated Skill Package

### Summary

This update consolidates the Solo Product Engineering Skills package into a more complete and usable release. The package now has a consistent 20-skill shape in both forms:

- Trae package form: `.trae/skills/*`
- Top-level OpenAI/Codex skill form: `solo-*`

The most important change is that fragment persistence is no longer only a prompt convention. `solo-fragment-collector` now includes a deterministic script that initializes fragment folders, captures fragments, reads status, consolidates active fragments, and records consolidation history.

### Goals

- Keep the richer `.trae` package as the source of product intent.
- Fill the missing top-level `solo-fragment-collector` skill.
- Reduce noisy automatic fragment capture by introducing signal confidence levels.
- Make fragment persistence verifiable through scripts.
- Make installation safer for real projects.
- Produce a clean integrated zip package for reuse.

### Key Changes

#### 1. Completed The 20-Skill Shape

Added a top-level `solo-fragment-collector` folder so the root skill layout now matches the `.trae` package.

Added:

- `solo-fragment-collector/SKILL.md`
- `solo-fragment-collector/agents/openai.yaml`
- `solo-fragment-collector/scripts/fragment_store.py`

The `.trae` version also now includes:

- `.trae/skills/solo-fragment-collector/agents/openai.yaml`
- `.trae/skills/solo-fragment-collector/scripts/fragment_store.py`

#### 2. Added Deterministic Fragment Storage

Added `fragment_store.py` to handle file I/O for fragment persistence.

Supported commands:

```powershell
python ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" init
python ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" capture requirement "用户希望上传头像并限制 2MB"
python ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" status
python ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" read requirement
python ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" consolidate requirement
python ".trae\skills\solo-fragment-collector\scripts\fragment_store.py" diff requirement
```

The script creates and manages:

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

#### 3. Reduced Over-Capture Risk

Updated the routing rules from "capture everything that matches a keyword" to a three-level confidence model:

| Level | Behavior |
|---|---|
| Strong signal | Capture immediately |
| Weak signal | Capture only if it continues the active change or combines with another signal |
| Suspected signal | Mention it, but do not write to disk |

Updated files:

- `.trae/rules/project_rules.md`
- `.trae/skills/solo-product-engineering-operator/SKILL.md`
- `.trae/skills/solo-product-engineering-operator/agents/openai.yaml`
- `solo-product-engineering-operator/SKILL.md`

#### 4. Safer Installer

Updated `install.ps1` to support explicit target installation:

```powershell
.\install.ps1 -TargetPath "C:\path\to\your-project"
.\install.ps1 -TargetPath "C:\path\to\your-project" -Force
.\install.ps1 -TargetPath "C:\path\to\your-project" -GlobalRules
```

Installer improvements:

- Adds `-TargetPath`.
- Adds explicit `-GlobalRules`.
- Avoids deleting source `.trae/skills` when installing from the package directory.
- Backs up an existing target `.trae/skills` before overwriting with `-Force`.
- Uses ASCII console arrows for better Windows terminal compatibility.

#### 5. Documentation Alignment

Updated:

- `README.md`
- `ARCHITECTURE.md`

Documentation now reflects:

- 20 skills in both package forms.
- `docs/changes/current.md` as the active change index.
- `fragment_store.py` as the deterministic persistence layer.
- Strong/weak/suspected signal classification.
- Safer install command examples.

#### 6. Integrated Package

Created:

- `solo-product-engineering-skills-integrated.zip`

The integrated zip includes:

- `.trae/`
- all top-level `solo-*` skill folders
- `README.md`
- `ARCHITECTURE.md`
- `install.ps1`
- `CHANGELOG.md`

### Validation

Completed checks:

- Verified `.trae/skills` contains 20 skill directories.
- Verified top-level `solo-*` contains 20 skill directories.
- Ran `fragment_store.py --help` for both top-level and `.trae` script paths.
- Ran an end-to-end fragment persistence test in a temporary directory:
  - `init`
  - `capture`
  - `status`
  - `consolidate`
  - post-consolidation `status`
- Ran `quick_validate.py` for:
  - `solo-fragment-collector`
  - `.trae/skills/solo-fragment-collector`
  - `solo-product-engineering-operator`
  - `.trae/skills/solo-product-engineering-operator`
- Ran `py_compile` for both `fragment_store.py` copies.
- Tested `install.ps1 -TargetPath <temp>` and confirmed 20 skills plus rules were installed.
- Tested `install.ps1` from the package directory and confirmed source files were not deleted.
- Rebuilt `solo-product-engineering-skills-integrated.zip`.
- Verified the zip contains 20 `.trae` skills and 20 top-level skills.
- Verified no `__pycache__` entries were included in the zip.

Note: On Windows, `quick_validate.py` needs UTF-8 mode for these Chinese UTF-8 skill files:

```powershell
$env:PYTHONUTF8='1'
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py solo-fragment-collector
```

### Remaining Notes

- `fragment_store.py` creates consolidation drafts from source fragments. The final PRD, ADR, task board, test checklist, or case study should still be produced by the corresponding specialist skill.
- The original `solo-product-engineering-skills.zip` was left unchanged.
- `solo-product-engineering-skills-integrated.zip` is the current integrated release artifact.
