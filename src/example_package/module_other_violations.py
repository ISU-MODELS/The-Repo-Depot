# =============================================================================
# Optional: other Ruff violations (for teaching Stage 2)
# =============================================================================
# Use this file after students have seen PLR0915 in module_with_issues.py.
# It demonstrates F401 (unused import), N802/N806 (naming), ERA001, B018.
# Ruff will report these when you run: ruff check . --no-fix
#
# To focus only on PLR0915, exclude this file in pyproject.toml:
#   exclude = [..., "**/module_other_violations.py"]
# =============================================================================

"""Example violations: unused import, naming, commented code, useless expression."""

import json  # F401: unused import

from typing import NoReturn  # F401 when unused


def DoSomething() -> None:  # N802: function name should be snake_case
    """Badly named function."""
    BadName = 1  # N806: variable in function should be lowercase
    _ = BadName
    # print("commented out")  # ERA001: commented-out code
    len([1, 2, 3])  # B018: useless expression (return value not used)
