# =============================================================================
# Package public API
# =============================================================================
# This module defines what is exposed when users do "from example_package import *"
# and documents the main entry points for the demo package. All public symbols
# should be listed in __all__ so that the API is explicit and stable.
# =============================================================================

"""Example package for CI/CD Ruff lint and matrix deployment demo."""

# Public symbols: only these are exported by "from example_package import *"
__all__ = [
    "add",  # Sum two integers (used by tests and deployment check)
    "validate_positive",  # Raise if value is not positive (used by tests)
]

from example_package.logic import add, validate_positive
