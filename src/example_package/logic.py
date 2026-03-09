# =============================================================================
# Core logic (lint-clean module)
# =============================================================================
# This module is used by the unit tests and the CD deployment check. It is
# intentionally written to pass all Ruff rules: snake_case names, no redundant
# code, no long functions. Use it as a reference for "good" style in this repo.
# =============================================================================

"""Clean module used by unit tests. No lint violations."""


def add(a: int, b: int) -> int:
    """Return the sum of a and b."""
    return a + b


def validate_positive(n: int) -> None:
    """Raise ValueError if n is not positive."""
    if n <= 0:
        raise ValueError(f"Expected positive integer, got {n}")
