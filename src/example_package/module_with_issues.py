# =============================================================================
# Intentionally bad module (for teaching Ruff rule PLR0915)
# =============================================================================
# This file is kept to demonstrate what the linter reports. It violates
# PLR0915 (too many statements) on purpose. Do not fix it if you want the
# lint workflow to fail (useful for testing CI). To get a green lint run,
# refactor the long function below or exclude this file from Ruff.
#
# Primary violation:
#   - PLR0915: too many statements (function has > 25 statements;
#     max-statements = 25 in pyproject.toml [tool.ruff.lint.pylint])
#
# For teaching other rules (F401, N802, N806, ERA001, B018), see
# module_other_violations.py or TEACHING_PROCEDURE.md "Stage 2".
# =============================================================================

"""
Intentionally long function to trigger PLR0915 (too-many-statements).

Ruff counts statements (assignments, return), not physical lines. This
function has 27 statements; max-statements is set to 25, so Ruff reports it.
"""


# -----------------------------------------------------------------------------
# PLR0915: too many statements. This function has 27 statements (assignments
# + return); max-statements is set to 25 in pyproject.toml, so Ruff reports it.
# -----------------------------------------------------------------------------
def function_with_too_many_statements() -> int:
    """Function that exceeds max-statements = 25."""
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    u = 21
    v = 22
    w = 23
    x = 24
    y = 25
    z = 26
    return a + z
