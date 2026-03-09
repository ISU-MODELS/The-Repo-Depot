# Teaching procedure: CI/CD and Ruff in this repository

This document gives you a **step-by-step procedure** to teach students how this repo works, with Ruff failing first on **“too many statements”** (PLR0915), not on unused variables.

---

## Learning goals

- Students see the **lint fail on function length** (PLR0915, max 25 statements).
- Students understand where the rule is configured (`pyproject.toml`) and how to fix or relax it.
- Optionally, students see **other Ruff rules** (unused import, naming, etc.) in a second stage.
- Students can run the same checks locally and see them on GitHub Actions.
- Students can change **which lint rules** or **which tests** run without editing YAML (using `config/lint-level.txt` and `config/test-profile.txt`).

---

## Prerequisites

- Python 3.9+ and `pip`.
- (Optional) [Ruff](https://docs.astral.sh/ruff/) installed: `pip install ruff`.

---

## Stage 1: Ruff and “too many statements” (PLR0915)

**Goal:** Lint fails only on **one** rule — “function has too many statements” — so the lesson is clear.

### Step 1.1 — Clone and install

```bash
git clone <this-repo-url>
cd The-Repo-Depot
pip install -r requirements/base.txt
pip install ruff   # if not already installed
```

### Step 1.2 — Run the linter (no fix)

```bash
ruff check . --no-fix
```

**Expected:** Ruff reports **one** violation:

- **PLR0915** in `src/example_package/module_with_issues.py`: function `function_with_too_many_statements` has too many statements (e.g. 27 > 25).

If you see F401 (unused import) or N802/N806 (naming) here, the repo is not in the intended state: the only file that should trigger by default is `module_with_issues.py`, and it should only violate PLR0915. The optional file `module_other_violations.py` is excluded from Ruff by default (see [Stage 2](#stage-2-optional-other-ruff-rules)).

### Step 1.3 — Show where the rule is configured

Open [pyproject.toml](pyproject.toml) and show:

- `[tool.ruff.lint]` → `select = [..., "PLR0915"]`
- `[tool.ruff.lint.pylint]` → `max-statements = 25`

Explain: Ruff counts **statements** (assignments, `return`, etc.), not physical lines, so “max 25 statements” is a proxy for “keep functions short.”

### Step 1.4 — Fix the violation (two options)

**Option A — Refactor the function**  
Have students shorten `function_with_too_many_statements()` (e.g. use a loop or a data structure) so it has ≤ 25 statements, then run `ruff check . --no-fix` again until it passes.

**Option B — Exclude the file**  
To keep the “bad” function for demo purposes, add it to Ruff’s exclude in `pyproject.toml`:

```toml
exclude = [
    # ... existing entries ...
    "**/module_with_issues.py",
]
```

Then `ruff check . --no-fix` passes (Ruff skips that file).

### Step 1.5 — Run format check (optional)

```bash
ruff format --check .
```

Use this to show that the repo also enforces formatting; fix with `ruff format .` if you want to allow auto-fix in the lesson.

---

## Stage 2 (optional): Other Ruff rules

**Goal:** Show F401 (unused import), N802/N806 (naming), ERA001 (commented-out code), B018 (useless expression) without overshadowing the PLR0915 lesson.

The file [src/example_package/module_other_violations.py](src/example_package/module_other_violations.py) contains these violations but is **excluded** from Ruff by default in `pyproject.toml`.

### Step 2.1 — Include the optional file in linting

In [pyproject.toml](pyproject.toml), remove (or comment out) this line from the `exclude` list:

```toml
"**/module_other_violations.py",  # optional Stage 2 demo; remove to show F401, N802, etc.
```

### Step 2.2 — Run Ruff again

```bash
ruff check . --no-fix
```

**Expected:** In addition to PLR0915 in `module_with_issues.py`, Ruff now reports violations in `module_other_violations.py`: F401, N802, N806, ERA001, B018. Use this to explain each code and how to fix it.

---

## Running the full workflow locally

- **Lint (Ruff):** `ruff check . --no-fix` and `ruff format --check .`
- **Tests:** `pytest tests/ -v --cov=src --cov-report=term-missing`
- **Type check:** `mypy src/`
- **Pre-commit (all at once):** `pre-commit run --all-files` (after `pre-commit install`)

Point students to [CONTRIBUTING.md](CONTRIBUTING.md) and [LEARNING.md](LEARNING.md) for the full picture and links to each workflow file.

---

## Suggested teaching order

1. **Stage 1** — Run `ruff check . --no-fix`, see **only** PLR0915; show `max-statements` in `pyproject.toml`; fix or exclude.
2. **Stage 2** — Un-exclude `module_other_violations.py`, run Ruff again, discuss F401, N802, N806, ERA001, B018.
3. **CI/CD** — Use [LEARNING.md](LEARNING.md) and the links to `.github/workflows/*.yml` to show how the same checks run on push/PR.

---

## Troubleshooting

| What you see | What to check |
|--------------|----------------|
| Ruff fails on “unused import” (F401) before “too many statements” | Ensure the **only** file that triggers by default is `module_with_issues.py` (only PLR0915). Keep `module_other_violations.py` in Ruff’s `exclude` until Stage 2. |
| No PLR0915 reported | Confirm `PLR0915` is in `tool.ruff.lint.select` and `max-statements = 25` is set under `[tool.ruff.lint.pylint]`. Run `ruff check src/example_package/module_with_issues.py --no-fix`. |
| Lint passes immediately | Either `module_with_issues.py` was fixed/excluded or Ruff is not checking it (path/exclude). |

---

## Quick reference

| Topic | File or command |
|-------|------------------|
| Ruff rule “too many statements” | [pyproject.toml](pyproject.toml) → `[tool.ruff.lint.pylint]` `max-statements = 25` |
| Intended first failure (PLR0915 only) | [src/example_package/module_with_issues.py](src/example_package/module_with_issues.py) |
| Optional other violations (Stage 2) | [src/example_package/module_other_violations.py](src/example_package/module_other_violations.py); remove from `exclude` in pyproject.toml |
| Lint workflow on GitHub | [.github/workflows/lint.yml](.github/workflows/lint.yml) |
| Full learning guide | [LEARNING.md](LEARNING.md) |
