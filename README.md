# CI/CD Repository with Ruff Linting and Matrix Deployment

This repository demonstrates **industry-standard CI/CD practices** for a Python project. It is intended for **teaching**: workflows and config files include verbose comments explaining *why* each step exists and how to extend or adapt it.

**New to this repo?** Start with the **[Learning guide (LEARNING.md)](LEARNING.md)** — an interactive overview that links to each workflow, config file, and code example — and **[Teaching procedure (TEACHING_PROCEDURE.md)](TEACHING_PROCEDURE.md)** for a step-by-step lesson plan (Ruff first fails on “too many statements,” then optional other rules).

## What this repo demonstrates

- **Lint workflow**: Ruff lint and format checks; no autocorrect; caching for speed.
- **CI workflow**: Unit tests with coverage (pytest-cov), type checking (mypy), and artifact upload.
- **CD workflow**: Matrix testing over Python versions, OS, and dependency sets; optional GPU job.
- **Security workflow**: Dependency vulnerability scan (pip-audit) and secret scanning (Gitleaks).
- **Build workflow**: Verify the package builds (sdist + wheel) from `pyproject.toml`.
- **Pre-commit**: Same lint/format locally before commit.
- **Dependabot**: Automated dependency and GitHub Actions updates.
- **LICENSE**, **CONTRIBUTING.md**, and clear layout for contributors.

---

## Quick start

### Run lint locally

```bash
pip install ruff
ruff check . --no-fix    # Report only; do not modify code
ruff format --check .     # Fail if formatting would change
```

The linter does **not** modify code; it exits with a non-zero status when violations are found. To reformat code so that `ruff format --check` passes, run `ruff format .`.

### Run tests locally

```bash
pip install -r requirements/base.txt
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Run type checking

```bash
mypy src/
```

### Run all checks (pre-commit)

We recommend using [pre-commit](https://pre-commit.com/) so lint and format run before each commit:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files   # Run manually on entire repo
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full list of local checks and the PR process.

---

## Workflows (GitHub Actions)

All workflows run on **push** and **pull_request** to `main` and `master`. Each file in `.github/workflows/` includes **block comments** at the top and before major sections explaining purpose and best practices.

| Workflow   | File            | Purpose |
|-----------|-----------------|---------|
| **Lint**  | `lint.yml`      | Ruff lint (`--no-fix`) and Ruff format check; pip and Ruff caches. |
| **CI**    | `ci.yml`       | Tests with coverage (pytest-cov), coverage artifact upload; mypy typecheck; pip cache. |
| **CD**    | `cd.yml`       | Matrix over Python × OS × dependency-set; deployment check; optional GPU job; pip cache. |
| **Security** | `security.yml` | pip-audit (dependency vulnerabilities); Gitleaks (secret scanning). |
| **Build** | `build.yml`    | `python -m build` (sdist + wheel); upload dist as artifact. |

Workflows only run when **relevant files** change (path filters) and **cancel** previous runs on the same branch (concurrency). See [LEARNING.md — Speeding up workflows](LEARNING.md#speeding-up-workflows) and [LEARNING.md — Progress reporting](LEARNING.md#progress-reporting-for-developers).

### CD matrix

Edit [`.github/workflows/cd.yml`](.github/workflows/cd.yml) to change the developer-provided lists:

- **python-version**: e.g. `["3.9", "3.10", "3.11", "3.12"]`
- **os**: e.g. `[ubuntu-latest, windows-latest, macos-latest]`
- **dependency-set**: `min` (from `requirements/min.txt`) or `pinned` (from `requirements/pinned.txt`)

Use `matrix.exclude` to skip known-bad combinations. The workflow file contains inline comments explaining each list.

### Adding more unit tests

- Add new files under `tests/` named `test_*.py`; pytest discovers them automatically.
- Add new functions named `test_*` in existing test files.

See [tests/test_logic.py](tests/test_logic.py) for two example tests and a short comment block on how to add more.

---

## Example code that triggers lint

[`src/example_package/module_with_issues.py`](src/example_package/module_with_issues.py) is **intentionally** written to violate **PLR0915** (too many statements; max 25) so that `ruff check . --no-fix` fails. Use it to see the linter report. Fix the function or exclude that file to get a passing lint run. For a step-by-step teaching procedure, see [TEACHING_PROCEDURE.md](TEACHING_PROCEDURE.md). Optional violations (F401, N802, etc.) are in [`module_other_violations.py`](src/example_package/module_other_violations.py), excluded from Ruff by default until you want to teach them.

---

## Industry practices included (and where to find them)

| Practice              | Where to look |
|-----------------------|----------------|
| Ruff format check     | `lint.yml` (step "Run Ruff format check"); `pyproject.toml` Ruff config. |
| Pre-commit            | `.pre-commit-config.yaml`; [CONTRIBUTING.md](CONTRIBUTING.md). |
| Dependabot            | `.github/dependabot.yml` (pip + github-actions). |
| Dependency audit      | `security.yml` job `dependency-audit` (pip-audit). |
| Secret scanning       | `security.yml` job `secret-scan` (Gitleaks). |
| Test coverage         | `ci.yml` (pytest-cov, artifact); `requirements/base.txt` (pytest-cov). |
| Type checking         | `ci.yml` job `typecheck` (mypy); `pyproject.toml` `[tool.mypy]`. |
| Caching               | `lint.yml`, `ci.yml`, `cd.yml` (actions/cache for pip and Ruff). |
| LICENSE               | [LICENSE](LICENSE) (MIT). |
| CONTRIBUTING          | [CONTRIBUTING.md](CONTRIBUTING.md). |
| Build check           | `build.yml`; `pyproject.toml` `[build-system]`. |

---

## Implementation notes (report-back)

### Nondescriptive names

Ruff has no rule that forbids “nondescriptive” or too-short names (e.g. single-letter variables). We enable **N8** (pep8-naming), which enforces **snake_case** for functions and variables (N802, N806), improving consistency and readability. Stricter “no single-letter names” checks would require a custom script or another tool.

### Functions greater than 25 code lines

We use **PLR0915** (too-many-statements) with `max-statements = 25` in [pyproject.toml](pyproject.toml). Ruff counts **statements**, not physical lines, so this is a close proxy for “> 25 lines” but not identical. Strict line-based limits would require another tool or script.

### Redundant code lines

We enable **F401** (unused import), **F811** (redefined while unused), **B018** (useless expression), **B019** (useless type annotation), and **ERA001** (commented-out code). Ruff does not do full duplicate-code-block detection; these cover redundant lines and obvious redundancy.

### No autocorrect

The lint workflow runs `ruff check . --no-fix`. Ruff exits with a non-zero code when any violation is found and does not change any code. Pre-commit is configured the same way for consistency.

### AMD / Intel / NVIDIA

- **CPU**: GitHub-hosted runners do not let you choose CPU vendor. Linux/Windows use AMD EPYC; macOS varies by image. The matrix uses **OS** and **Python version**, not “AMD vs Intel.”
- **NVIDIA GPU**: Requires self-hosted or third-party GPU runners. The CD workflow includes an optional **gpu-test** job (`runs-on: [self-hosted, gpu]`, disabled by default). Set `if: true` when you have such a runner.

---

## Layout

```
.github/
  workflows/       lint.yml, ci.yml, cd.yml, security.yml, build.yml
  dependabot.yml   Automated dependency and action updates
.pre-commit-config.yaml   Hooks for lint/format before commit
src/example_package/   __init__.py, logic.py, module_with_issues.py
tests/                 test_logic.py, conftest.py
requirements/          base.txt, min.txt, pinned.txt
pyproject.toml         Build, Ruff, pytest, mypy config
LICENSE                MIT
CONTRIBUTING.md        How to run checks and open PRs
LEARNING.md            Interactive learning guide (links to all principles and code)
TEACHING_PROCEDURE.md  Step-by-step teaching procedure (Ruff PLR0915 first, then optional rules)
README.md              This file
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for the full text.
