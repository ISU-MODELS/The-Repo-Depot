# =============================================================================
# Unit tests for example_package.logic
# =============================================================================
# These tests validate the behavior of the "clean" module (logic.py) used by CI
# and CD. Marked @pytest.mark.unit so CI can run only unit tests when
# config/test-profile.txt is "unit". Add more test_* functions or test_*.py as needed.
# =============================================================================

"""
Unit tests for example_package.logic.

To add more tests:
  - Add new test_*.py files under tests/ (pytest discovers them automatically).
  - Or add new test_* functions in this file (e.g. test_multiply_returns_product).
  - Use @pytest.mark.unit for fast, isolated tests; @pytest.mark.integration for broader tests.
Pytest collects any function whose name starts with "test_" in files matching
test_*.py or *_test.py.
"""

import pytest

from example_package.logic import add, validate_positive


# -----------------------------------------------------------------------------
# Test 1: Pure function (add) — happy path and edge cases
# -----------------------------------------------------------------------------
@pytest.mark.unit
def test_add_returns_sum() -> None:
    """Test that add returns the sum of two integers."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


@pytest.mark.unit
def test_add_commutative() -> None:
    """Addition is commutative."""
    assert add(3, 7) == add(7, 3)


@pytest.mark.unit
def test_add_negative_values() -> None:
    """add handles negative integers."""
    assert add(-2, -3) == -5


# -----------------------------------------------------------------------------
# Test 2: Function that raises (validate_positive) — exception behavior
# -----------------------------------------------------------------------------
@pytest.mark.unit
def test_validate_positive_raises_for_negative() -> None:
    """Test that validate_positive raises ValueError for non-positive input."""
    with pytest.raises(ValueError, match="Expected positive integer"):
        validate_positive(0)
    with pytest.raises(ValueError, match="Expected positive integer"):
        validate_positive(-1)
    validate_positive(1)  # No raise for positive input


@pytest.mark.unit
def test_validate_positive_accepts_positive() -> None:
    """validate_positive does not raise for positive integers."""
    validate_positive(1)
    validate_positive(100)
