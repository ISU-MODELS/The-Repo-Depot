# Learning guide: CI/CD and quality practices

This page is an **interactive overview** for learning all principles used in this repository. Use the table of contents and the links below to jump to code examples and workflow files. It is aimed at developers new to CI/CD who want to understand *what* we do and *where* it is implemented.

---

## How to use this guide

- **Table of contents** — Click any item to jump to that section.
- **Bold links** — Point to the exact file (and sometimes the idea) where the concept is implemented.
- **“See in repo”** — Links to the actual workflow or config file so you can read the code and comments.
- **Suggested order** — Read [Core idea: what runs and when](#core-idea-what-runs-and-when) first, then [Linting](#1-linting), [CI](#2-continuous-integration-ci), and [CD](#3-continuous-deployment-matrix-testing-cd). Use [Speeding up workflows](#speeding-up-workflows) and [Progress reporting](#progress-reporting-for-developers) when you care about performance and feedback.

---

## Table of contents

1. [Core idea: what runs and when](#core-idea-what-runs-and-when)
2. [Speeding up workflows](#speeding-up-workflows)
3. [Progress reporting for developers](#progress-reporting-for-developers)
4. [Principles in detail](#principles-in-detail)
   - [1. Linting](#1-linting)
   - [2. Continuous Integration (CI)](#2-continuous-integration-ci)
   - [3. Continuous Deployment / matrix testing (CD)](#3-continuous-deployment-matrix-testing-cd)
   - [4. Security](#4-security)
   - [5. Build](#5-build)
   - [6. Pre-commit](#6-pre-commit)
   - [7. Dependencies and updates](#7-dependencies-and-updates)
5. [Quick reference: where is everything?](#quick-reference-where-is-everything)

---

## Core idea: what runs and when

When you **push** or open a **pull request** to `main` or `master`, GitHub Actions runs several **workflows**. Each workflow is a YAML file under [`.github/workflows/`](.github/workflows/). They run in parallel and can be **skipped** if your change doesn’t touch relevant files (see [Speeding up workflows](#speeding-up-workflows)).

| What runs | Purpose | See in repo |
|-----------|---------|-------------|
| **Lint** | Enforce code style and lint rules (no autocorrect) | [lint.yml](.github/workflows/lint.yml) |
| **CI** | Run tests, coverage, and type checking | [ci.yml](.github/workflows/ci.yml) |
| **CD** | Run tests on many Python/OS/dependency combinations | [cd.yml](.github/workflows/cd.yml) |
| **Security** | Check dependencies for vulnerabilities and scan for secrets | [security.yml](.github/workflows/security.yml) |
| **Build** | Check that the package builds (sdist + wheel) | [build.yml](.github/workflows/build.yml) |

Branch protection can require these checks to pass before merging. See [CONTRIBUTING.md](CONTRIBUTING.md#branch-protection-for-maintainers) for how to set that up.

---

## Speeding up workflows

We use three techniques to **run fewer jobs** and **finish each run faster**.

### 1. Path filters — run only when relevant files change

Each workflow runs only when files in certain paths change. For example, the **Lint** workflow runs only when Python files or Ruff config change, not when you edit only the README.

- **Lint**: [paths in lint.yml](.github/workflows/lint.yml) — `**.py`, `pyproject.toml`, `.ruff.toml`, and the workflow file itself.
- **CI**: [paths in ci.yml](.github/workflows/ci.yml) — Python, `requirements/`, `pyproject.toml`, `tests/`, and the workflow file.
- **CD**: [paths in cd.yml](.github/workflows/cd.yml) — Python, requirements, config, tests, `src/`, and the workflow file.
- **Security**: [paths in security.yml](.github/workflows/security.yml) — requirements, Python, and the workflow file.
- **Build**: [paths in build.yml](.github/workflows/build.yml) — `src/`, `pyproject.toml`, and the workflow file.

**Effect:** Pushes that only change docs or unrelated config won’t trigger every workflow, so you get faster feedback and use fewer runner minutes.

### 2. Concurrency — cancel outdated runs

When you push again to the same branch before the previous run finishes, we **cancel** the previous run so only the latest commit is validated.

- **Where it’s set:** In every workflow file, under `concurrency:` (e.g. [lint.yml concurrency](.github/workflows/lint.yml), [ci.yml concurrency](.github/workflows/ci.yml)).
- **Pattern:** `group: <workflow-name>-${{ github.ref }}` and `cancel-in-progress: true`. **Exception:** [CD has no concurrency block](.github/workflows/cd.yml) so each run completes all matrix jobs; with a group, a newer push can cancel in-progress jobs ("higher priority waiting request").

**Effect:** You don’t wait for an obsolete run (Lint/CI), and you see status for the latest push. For CD, every deployment combination is tested and no run cancels another.

### 3. Caching — reuse dependencies and tool data

We cache **pip** installs and **Ruff**’s cache so repeat runs are faster.

- **Lint**: [Cache pip and Ruff in lint.yml](.github/workflows/lint.yml) — keys use hashes of `requirements/base.txt` and of `pyproject.toml` + `**/*.py`.
- **CI**: [Cache pip in ci.yml](.github/workflows/ci.yml) — same cache key for both test and typecheck jobs.
- **CD**: [Cache pip per matrix cell in cd.yml](.github/workflows/cd.yml) — key includes OS, Python version, and dependency-set so each environment has its own cache.

**Effect:** After the first run (or when deps/code change), install and lint steps are much faster.

---

## Progress reporting for developers

We make workflow results easy to see in the GitHub Actions UI.

### 1. Job summary (markdown in the Summary tab)

Steps write markdown to **Job summary** (`GITHUB_STEP_SUMMARY`) so you see a short recap without opening the raw log.

- **Lint**: [Ruff lint and format steps in lint.yml](.github/workflows/lint.yml) — append Ruff output and a short “Ruff format check” status to the summary.
- **CI**: [Pytest and mypy steps in ci.yml](.github/workflows/ci.yml) — “Test results” and “Type check (mypy)” lines in the summary.
- **Security**: [pip-audit step in security.yml](.github/workflows/security.yml) — dependency audit output in the summary.
- **Build**: [Build step in build.yml](.github/workflows/build.yml) — “Build result” and `ls dist/` in the summary.

**Where to look:** Open a workflow run → click a job → the **Summary** tab (top) shows this markdown.

### 2. Log grouping (collapsible sections)

Long command output is wrapped in `::group::` / `::endgroup::` so the log is collapsible.

- **CI**: [Pytest and mypy in ci.yml](.github/workflows/ci.yml) — “Pytest output” and “Mypy output” groups.
- **CD**: [Pytest in cd.yml](.github/workflows/cd.yml) — one group per matrix job (e.g. “Pytest (Py 3.11 / ubuntu-latest / min)”).
- **Build**: [Build step in build.yml](.github/workflows/build.yml) — “Build output” group.

**Where to look:** In the job log, look for collapsible sections with these names.

### 3. GitHub Actions annotations (Ruff)

Ruff is run with **`--output-format=github`** so each lint issue appears as an annotation on the **Files changed** tab of the PR.

- **Where:** [Run Ruff lint step in lint.yml](.github/workflows/lint.yml) — `ruff check . --no-fix --output-format=github`.

**Where to look:** Open a PR → “Files changed” → annotations on the relevant lines.

---

## Principles in detail

Below, each principle is explained and linked to the exact files and sections that implement it.

---

### 1. Linting

**Goal:** Enforce code style and lint rules **without** modifying code; the workflow fails and reports issues so developers fix them locally.

**What we use:** Ruff for both **lint** (rule violations) and **format** (style). Lint is run with `--no-fix` so the pipeline never auto-corrects.

| Topic | Where it’s configured | Where it runs |
|--------|----------------------|----------------|
| Which rules run | [pyproject.toml — tool.ruff.lint](pyproject.toml) | [lint.yml — Ruff check and format steps](.github/workflows/lint.yml) |
| Max function length (statements) | [pyproject.toml — tool.ruff.lint.pylint](pyproject.toml) (`max-statements = 25`) | Same as above |
| Naming (e.g. snake_case) | [pyproject.toml — select N8](pyproject.toml) | Same as above |
| Redundant code (unused import, commented code, etc.) | [pyproject.toml — F401, ERA001, B018, B019, etc.](pyproject.toml) | Same as above |

**Configurable lint level:** Edit [config/lint-level.txt](config/lint-level.txt) (first line: `minimal` \| `standard` \| `strict`) to change which rules the Lint workflow runs — no YAML edit. Or run the workflow manually and choose **Lint level**. See [config/README.md](config/README.md).

**Example of code that fails lint (for teaching):** [module_with_issues.py](src/example_package/module_with_issues.py) — intentionally violates **PLR0915** (too many statements). See [TEACHING_PROCEDURE.md](TEACHING_PROCEDURE.md) for a step-by-step lesson. Optional file [module_other_violations.py](src/example_package/module_other_violations.py) demonstrates F401, N802, N806, ERA001, B018 (excluded from Ruff by default).

**Example of clean code:** [logic.py](src/example_package/logic.py).

**Run locally:**  
`ruff check . --no-fix` and `ruff format --check .`  
(See [README — Run lint locally](README.md#run-lint-locally).)

---

### 2. Continuous Integration (CI)

**Goal:** On every relevant push/PR, run **tests** (with coverage) and **type checking** so the main branch stays green and type-safe.

**What we use:** pytest, pytest-cov, and mypy. Two jobs run in parallel: **test** and **typecheck**.

| Topic | Where it’s configured | Where it runs |
|--------|----------------------|----------------|
| Test discovery and paths | [pyproject.toml — tool.pytest.ini_options](pyproject.toml) | [ci.yml — test job](.github/workflows/ci.yml) |
| Coverage (source and reports) | [ci.yml — Run tests with coverage](.github/workflows/ci.yml) | Same (term + XML; artifact upload) |
| Type checking | [pyproject.toml — tool.mypy](pyproject.toml) | [ci.yml — typecheck job](.github/workflows/ci.yml) |
| Test markers (unit vs integration) | [pyproject.toml — markers](pyproject.toml) | [ci.yml — pytest -m](.github/workflows/ci.yml) per profile |

**Configurable test profile:** Edit [config/test-profile.txt](config/test-profile.txt) (first line: `unit` \| `integration` \| `all`) to change which tests the CI workflow runs. Or run the workflow manually and choose **Test profile**. See [config/README.md](config/README.md).

**Example tests:** [tests/test_logic.py](tests/test_logic.py) (unit), [tests/test_integration.py](tests/test_integration.py) (integration).

**Run locally:**  
`pytest tests/ -v --cov=src --cov-report=term-missing` and `mypy src/`  
(See [README — Run tests and type checking](README.md#run-tests-locally).)

---

### 3. Continuous Deployment / matrix testing (CD)

**Goal:** Check that the codebase works across **many environments**: different Python versions, operating systems, and dependency sets (min vs pinned). This catches compatibility issues before deployment.

**What we use:** A single **matrix** job (Python × OS × dependency-set) plus an optional **GPU** job (off by default).

| Topic | Where it’s configured | Where it runs |
|--------|----------------------|----------------|
| Matrix axes (Python, OS, deps) | [cd.yml — strategy.matrix](.github/workflows/cd.yml) | [cd.yml — matrix-test job](.github/workflows/cd.yml) |
| Excluding bad combinations | [cd.yml — matrix.exclude](.github/workflows/cd.yml) | Same |
| Dependency sets (min vs pinned) | [requirements/min.txt](requirements/min.txt), [requirements/pinned.txt](requirements/pinned.txt) | [cd.yml — Install dependencies step](.github/workflows/cd.yml) |
| Deployment check (import + smoke) | [cd.yml — Deployment check step](.github/workflows/cd.yml) | Same |
| Optional GPU job | [cd.yml — gpu-test job](.github/workflows/cd.yml) (`if: false`) | Same (enable when you have a GPU runner) |

**Run locally:**  
Use one Python version and one dependency set, e.g.  
`pip install -r requirements/pinned.txt` then `pytest tests/ -v`.  
(See [README — CD matrix](README.md#cd-matrix).)

---

### 4. Security

**Goal:** Detect **known vulnerabilities** in dependencies and **secrets** committed in the repo.

**What we use:** pip-audit (dependency audit) and Gitleaks (secret scanning).

| Topic | Where it’s configured | Where it runs |
|--------|----------------------|----------------|
| Dependency vulnerabilities | None (pip-audit uses public advisories) | [security.yml — dependency-audit job](.github/workflows/security.yml) |
| Secret scanning | Gitleaks defaults (or custom config) | [security.yml — secret-scan job](.github/workflows/security.yml) |

**Run locally:**  
`pip install pip-audit && pip-audit --desc`  
(See [CONTRIBUTING — Security checks](CONTRIBUTING.md#5-security-checks-optional-locally).)

---

### 5. Build

**Goal:** Verify that the package **builds** correctly (sdist and wheel) from [pyproject.toml](pyproject.toml) and the `src/` layout.

**What we use:** PEP 517 build (`python -m build`). The workflow does not install or test the package; CI/CD cover that.

| Topic | Where it’s configured | Where it runs |
|--------|----------------------|----------------|
| Build backend and package discovery | [pyproject.toml — build-system and setuptools.packages.find](pyproject.toml) | [build.yml — build job](.github/workflows/build.yml) |

**Run locally:**  
`pip install build && python -m build`  
(See [README — Industry practices / Build check](README.md#industry-practices-included-and-where-to-find-them).)

---

### 6. Pre-commit

**Goal:** Run the **same** lint and format checks **before** each commit so developers fix issues before pushing.

**What we use:** [pre-commit](https://pre-commit.com/) with Ruff and generic hooks.

| Topic | Where it’s configured | How to use |
|--------|----------------------|------------|
| Ruff (lint + format) and other hooks | [.pre-commit-config.yaml](.pre-commit-config.yaml) | `pre-commit install` then commit as usual; or `pre-commit run --all-files` |

**Setup:**  
[README — Run all checks (pre-commit)](README.md#run-all-checks-pre-commit) and [CONTRIBUTING — Pre-commit hooks](CONTRIBUTING.md#pre-commit-hooks-recommended).

---

### 7. Dependencies and updates

**Goal:** Keep dependencies and GitHub Actions **up to date** and **secure** with minimal manual work.

**What we use:** Dependabot for pip and GitHub Actions.

| Topic | Where it’s configured | What it does |
|--------|----------------------|--------------|
| Pip and Actions update schedule | [.github/dependabot.yml](.github/dependabot.yml) | Opens PRs when new versions are available |

**Dependency files:**  
[requirements/base.txt](requirements/base.txt), [requirements/min.txt](requirements/min.txt), [requirements/pinned.txt](requirements/pinned.txt) — see comments in each file for their role.

---

## Quick reference: where is everything?

Use this table to jump straight to the file that implements each piece.

| Concept | File(s) |
|---------|--------|
| Lint workflow (Ruff, format, path filters, concurrency, cache, summary) | [.github/workflows/lint.yml](.github/workflows/lint.yml) |
| CI workflow (tests, coverage, mypy, path filters, concurrency, grouping, summary) | [.github/workflows/ci.yml](.github/workflows/ci.yml) |
| CD workflow (matrix, deployment check, GPU job, path filters, concurrency, grouping) | [.github/workflows/cd.yml](.github/workflows/cd.yml) |
| Security workflow (pip-audit, Gitleaks, path filters, concurrency, summary) | [.github/workflows/security.yml](.github/workflows/security.yml) |
| Build workflow (build, path filters, concurrency, grouping, summary) | [.github/workflows/build.yml](.github/workflows/build.yml) |
| Ruff rules and options | [pyproject.toml](pyproject.toml) (sections `[tool.ruff]`, `[tool.ruff.lint]`) |
| Lint level and test profile (no YAML edit) | [config/lint-level.txt](config/lint-level.txt), [config/test-profile.txt](config/test-profile.txt); [config/README.md](config/README.md) |
| Pytest and mypy config | [pyproject.toml](pyproject.toml) (sections `[tool.pytest.ini_options]`, `[tool.mypy]`) |
| Build system and package layout | [pyproject.toml](pyproject.toml) (`[build-system]`, `[tool.setuptools.packages.find]`) |
| Pre-commit hooks | [.pre-commit-config.yaml](.pre-commit-config.yaml) |
| Dependabot | [.github/dependabot.yml](.github/dependabot.yml) |
| Example tests | [tests/test_logic.py](tests/test_logic.py) (unit), [tests/test_integration.py](tests/test_integration.py) (integration), [tests/conftest.py](tests/conftest.py) |
| Example “bad” module (for lint demos) | [src/example_package/module_with_issues.py](src/example_package/module_with_issues.py) (PLR0915); optional [module_other_violations.py](src/example_package/module_other_violations.py) (F401, N802, etc.) |
| Example “good” module | [src/example_package/logic.py](src/example_package/logic.py), [src/example_package/__init__.py](src/example_package/__init__.py) |
| How to contribute and run checks | [CONTRIBUTING.md](CONTRIBUTING.md) |
| High-level README | [README.md](README.md) |

---

## Optional: status badges in the README

To show workflow status at a glance, add badges to [README.md](README.md). Replace `OWNER` and `REPO` with your GitHub org and repo:

```markdown
[![Lint](https://github.com/OWNER/REPO/actions/workflows/lint.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/lint.yml)
[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)
[![CD](https://github.com/OWNER/REPO/actions/workflows/cd.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/cd.yml)
[![Security](https://github.com/OWNER/REPO/actions/workflows/security.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/security.yml)
[![Build](https://github.com/OWNER/REPO/actions/workflows/build.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/build.yml)
```

Each badge links to the corresponding workflow run list so developers can open the latest run with one click.
