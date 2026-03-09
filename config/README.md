# Configuration for Lint and CI workflows

This directory holds **single-file settings** so you can change which lint level or which tests run without editing YAML.

## Lint level — `lint-level.txt`

**Used by:** [Lint workflow](../.github/workflows/lint.yml) (and optional pre-commit / local scripts).

**Allowed values (one per line, first line wins):**

| Value      | Meaning | Ruff rules |
|-----------|--------|------------|
| `minimal` | Errors and Pyflakes only | `E9`, `F` (syntax/runtime errors, unused imports) |
| `standard`| Default: pycodestyle + Pyflakes + naming + redundancy + PLR0915 | Same as `pyproject.toml` (E4, E7, E9, F, N8, B018, B019, ERA001, PLR0915) |
| `strict`  | Standard + more Pylint-style rules | Standard plus e.g. `PLR`, `PLE`, `TRY` (broader Pylint) |

**To change:** Edit `lint-level.txt` and set the first line to one of the values above. Push; the next Lint run uses that level. You can also trigger the workflow manually (Actions → Lint → Run workflow) and choose **Lint level** in the dropdown.

**Local:** To match CI, run Ruff with the same select/ignore as the workflow for your chosen level (see CONTRIBUTING.md or the workflow file).

---

## Test profile — `test-profile.txt`

**Used by:** [CI workflow](../.github/workflows/ci.yml) (test job).

**Allowed values (one per line, first line wins):**

| Value        | Meaning | Pytest |
|-------------|--------|--------|
| `unit`      | Only tests marked `@pytest.mark.unit` | `pytest -m unit` |
| `integration` | Only tests marked `@pytest.mark.integration` | `pytest -m integration` |
| `all`       | No filter; run all tests | `pytest` (no `-m`) |

**To change:** Edit `test-profile.txt` and set the first line to `unit`, `integration`, or `all`. Push; the next CI run uses that profile. You can also trigger the workflow manually (Actions → CI → Run workflow) and choose **Test profile** in the dropdown.

**Local:**

```bash
PROFILE=$(cat config/test-profile.txt 2>/dev/null || echo all)
pytest tests/ -v -m "$PROFILE"   # use "all" for no marker filter: pytest tests/ -v
```

---

## Summary

| File               | Purpose |
|--------------------|--------|
| `config/lint-level.txt`   | Which Ruff rule set the Lint workflow uses: `minimal` \| `standard` \| `strict` |
| `config/test-profile.txt` | Which tests the CI workflow runs: `unit` \| `integration` \| `all` |

Edit these files and push to change behavior for the next run. No YAML edits required.
