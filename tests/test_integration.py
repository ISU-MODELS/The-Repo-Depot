# =============================================================================
# Integration tests: package import and cross-module behavior
# =============================================================================
# These tests are marked @pytest.mark.integration so CI can run only integration
# tests when config/test-profile.txt is "integration". They import the package,
# run real code paths, and verify behavior that depends on more than one unit.
# =============================================================================

"""
Integration tests for example_package.

Use pytest -m integration to run only these, or set config/test-profile.txt to
"integration" for CI. Use pytest (no -m) or profile "all" to run unit + integration.
"""

import pytest

import example_package
from example_package.logic import add, validate_positive


@pytest.mark.integration
def test_package_imports() -> None:
    """The package can be imported and has expected public surface."""
    assert hasattr(example_package, "__version__") or hasattr(example_package, "logic")
    from example_package import logic

    assert callable(logic.add)
    assert callable(logic.validate_positive)


@pytest.mark.integration
def test_add_and_validate_work_together() -> None:
    """Use add then validate_positive in a small workflow."""
    total = add(10, 20)
    validate_positive(total)
    assert total == 30


@pytest.mark.integration
def test_validate_positive_raises_after_add_zero() -> None:
    """Adding to zero and passing to validate_positive raises."""
    zero_sum = add(5, -5)
    with pytest.raises(ValueError, match="Expected positive integer"):
        validate_positive(zero_sum)
