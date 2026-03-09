# Contributing to CI/CD Ruff Demo

This document explains how to contribute to this repository in a way that matches our CI/CD and quality practices. Following these steps helps keep the main branch green and makes review easier.

For an **interactive overview** of all principles (linting, CI, CD, security, build, speed, and reporting), see **[LEARNING.md](LEARNING.md)** — it links to each workflow and code example.

---

## Before you start

- **Fork and clone** the repo (or create a branch if you have write access).
- Ensure you have **Python 3.9+** and **pip** available.
- We recommend using a **virtual environment** (e.g. `python -m venv .venv` then `.venv/bin/activate`).

---

## Running checks locally

All of the following should pass before you open a pull request. The same checks run in GitHub Actions; running them locally saves time and keeps CI green.

### 1. Install dependencies

```bash
pip install -r requirements/base.txt
```

This installs pytest, pytest-cov, ruff, and mypy (and any other base dependencies).

### 2. Lint (Ruff check and format)

We use Ruff for both **linting** (rule violations) and **formatting** (style). The linter is configured to **not** auto-fix so that developers fix issues explicitly.

**Lint level** is read from **`config/lint-level.txt`** (or set when you run the Lint workflow manually). Allowed values: `minimal` (E9,F only), `standard` (default; full rule set in pyproject.toml), `strict` (standard + more Pylint rules). See [config/README.md](config/README.md).

```bash
# Lint: report issues only; exits non-zero if there are violations
ruff check . --no-fix

# Format: check that code is formatted; exits non-zero if reformatting would occur
ruff format --check .
```

To **reformat** code locally (so that `ruff format --check` passes):

```bash
ruff format .
```

Do **not** run `ruff check . --fix` if you want to match CI behavior; fix reported issues by hand.

### 3. Type checking (mypy)

```bash
mypy src/
```

Fix any reported type errors (or add type: ignore with a comment if there is a known limitation).

### 4. Tests and coverage

**Test profile** is read from **`config/test-profile.txt`**: `unit` (only `@pytest.mark.unit`), `integration` (only `@pytest.mark.integration`), or `all` (no filter). See [config/README.md](config/README.md).

```bash
# Run all tests (default)
pytest tests/ -v --cov=src --cov-report=term-missing

# Run only unit or only integration (match CI when profile is set)
PROFILE=$(cat config/test-profile.txt 2>/dev/null | head -1 || echo all)
pytest tests/ -v -m "$PROFILE" --cov=src --cov-report=term-missing
```

All tests must pass. Coverage is reported in the terminal; we do not enforce a minimum coverage threshold in this demo, but you can set `--cov-fail-under=80` (or similar) in CI if you want to enforce it.

### 5. Security checks (optional locally)

- **Dependency vulnerabilities:**  
  `pip install pip-audit && pip-audit --desc`  
  Fix or accept risk for any reported vulnerabilities.

- **Secrets:**  
  Do not commit API keys, passwords, or tokens. The Security workflow runs Gitleaks in CI; if you accidentally commit a secret, rotate it immediately and remove it from history (e.g. with `git filter-branch` or BFG).

---

## Pre-commit hooks (recommended)

We provide a [pre-commit](https://pre-commit.com/) config so that lint and format run automatically before each commit.

```bash
pip install pre-commit
pre-commit install
```

After this, every `git commit` will run the configured hooks (Ruff lint, Ruff format, and a few generic checks). To run all hooks manually on the whole repo:

```bash
pre-commit run --all-files
```

---

## Pull request process

1. **Create a branch** from `main` (or `master`) for your change.
2. **Make your changes** and run all local checks above until they pass.
3. **Push** your branch and open a **Pull Request** against `main` (or `master`).
4. **Wait for CI.** All workflows (Lint, CI, CD, Security, Build) must pass. If any fail, fix the issues and push again.
5. **Request review** if the project has maintainers. Address review feedback.
6. **Merge** once approved and CI is green. We recommend using “Squash and merge” or “Rebase and merge” to keep history clean.

---

## Branch protection (for maintainers)

To enforce that nothing lands without passing CI:

1. Go to **Settings → Branches**.
2. Add a **branch protection rule** for `main` (and/or `master`).
3. Enable **Require status checks to pass before merging** and select the status checks that correspond to your workflows (e.g. “Lint”, “CI”, “CD”, “Security”, “Build”).
4. Optionally enable **Require branches to be up to date before merging** so that PRs must be rebased or merged from the latest main.

---

## Adding new tests

- Place test modules under **`tests/`** and name them **`test_*.py`** so pytest discovers them automatically.
- Use **`test_`** as the prefix for test functions (e.g. `test_add_returns_sum`).
- Mark tests with **`@pytest.mark.unit`** (fast, isolated) or **`@pytest.mark.integration`** (package import, multi-step) so CI can run by profile (`config/test-profile.txt`: unit | integration | all).
- Prefer **one logical assertion per test** where possible; use parametrize or multiple assertions when it makes sense.
- See **`tests/test_logic.py`** (unit) and **`tests/test_integration.py`** (integration) for the pattern used in this repo.

---

## Adding new dependencies

- **Runtime/library dependencies:** Add them to **`requirements/base.txt`** (and optionally to **`requirements/min.txt`** with a minimum version and **`requirements/pinned.txt`** with a pinned version for the CD matrix).
- **Tool-only dependencies (e.g. for CI):** Can stay in **`requirements/base.txt`** if everyone uses them, or in a separate file (e.g. **`requirements/dev.txt`**) and install that file in the relevant workflow.
- After adding or changing dependencies, run **`pip-audit`** and fix any new vulnerabilities.

---

## Code style and conventions

- **Formatting:** Ruff format (line length 88, double quotes, etc.). Run `ruff format .` before committing.
- **Lint rules:** Configured in **`pyproject.toml`** under `[tool.ruff.lint]`. Override which rules run in CI by editing **`config/lint-level.txt`** (`minimal` | `standard` | `strict`). Do not disable rules without a comment explaining why.
- **Naming:** Use **snake_case** for functions and variables (enforced by Ruff pep8-naming, N8).
- **Comments:** This repo uses **verbose comments** for teaching: block comments at the start of sections or ideas, inline comments for non-obvious lines or list items.

---

## Questions or issues

If something is unclear or you find a bug in the CI/CD setup, please open an **Issue** so we can improve the docs or the workflows for everyone.

Thank you for contributing.
