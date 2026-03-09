# =============================================================================
# Intentionally bad module (for teaching Ruff rules)
# =============================================================================
# This file is kept to demonstrate what the linter reports. It violates several
# Ruff rules on purpose. Do not fix it if you want the lint workflow to fail
# (useful for testing CI). To get a green lint run, fix the issues or exclude
# this file from Ruff (e.g. in pyproject.toml: exclude = [..., "**/module_with_issues.py"]).
#
# Violations included:
#   - N802: invalid function name (DoSomething should be do_something)
#   - N806: non-lowercase variable in function (BadName should be bad_name)
#   - F401: unused import (json, NoReturn)
#   - ERA001: commented-out code (the # print(...) line)
#   - B018: useless expression (len() result not used)
#   - PLR0915: too many statements (function has > 25 statements)
# =============================================================================

"""
Intentionally bad module to demonstrate Ruff lint rules.

Violations:
- N802: invalid function name (DoSomething, not snake_case)
- N806: non-lowercase variable in function (BadName)
- F401: unused import (json)
- ERA001: commented-out code
- B018: useless expression (e.g. function call as statement)
- B019: useless type annotation (e.g. NoReturn in wrong place) — if available
- PLR0915: too many statements (> 25)
"""

import json  # F401: unused import

from typing import NoReturn  # F401 when unused; kept for B019 reference


# -----------------------------------------------------------------------------
# N802 (function name) and N806 (variable name): naming convention violations
# -----------------------------------------------------------------------------
def DoSomething() -> None:  # N802: function name should be snake_case
    """Badly named function."""
    BadName = 1  # N806: variable in function should be lowercase
    _ = BadName
    # print("commented out")  # ERA001: commented-out code
    len([1, 2, 3])  # B018: useless expression (return value not used)


# -----------------------------------------------------------------------------
# PLR0915: too many statements. This function has 27 statements (assignments + return);
# max-statements is set to 25 in pyproject.toml, so Ruff reports it.
# -----------------------------------------------------------------------------
def function_with_too_many_statements() -> int:  # PLR0915: > 25 statements
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
