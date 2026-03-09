# =============================================================================
# Unit tests for example_package.logic
# =============================================================================
# These tests validate the behavior of the "clean" module (logic.py) used by CI
# and CD. We keep exactly two tests as specified in the plan; the comment block
# below explains how to add more so this repo can be used as a teaching template.
# =============================================================================

"""
Unit tests for example_package.logic.

To add more tests:
  - Add new test_*.py files under tests/ (pytest discovers them automatically).
  - Or add new test_* functions in this file (e.g. test_multiply_returns_product).
Pytest collects any function whose name starts with "test_" in files matching
test_*.py or *_test.py.
"""

import pytest

from example_package.logic import add, validate_positive


# -----------------------------------------------------------------------------
# Test 1: Pure function (add) — happy path and edge cases
# -----------------------------------------------------------------------------
def test_add_returns_sum() -> None:
    """Test that add returns the sum of two integers."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


# -----------------------------------------------------------------------------
# Test 2: Function that raises (validate_positive) — exception behavior
# -----------------------------------------------------------------------------
def test_validate_positive_raises_for_negative() -> None:
    """Test that validate_positive raises ValueError for non-positive input."""
    with pytest.raises(ValueError, match="Expected positive integer"):
        validate_positive(0)
    with pytest.raises(ValueError, match="Expected positive integer"):
        validate_positive(-1)
    validate_positive(1)  # No raise for positive input
