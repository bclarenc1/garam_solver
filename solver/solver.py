# pylint: disable=no-member
# pylint: disable=useless-return
# pylint: disable=too-many-locals
# pylint: disable=line-too-long

"""
Methods for solving Garam puzzles (cycles and full grids) using Z3.

This module defines helper functions to translate Garam constraints into Z3 formulas and solve them.
"""

from typing import List
from z3 import Int, Solver, sat

from .constants import VALID_OPS

def add_expression_constraint(digits: List, op: str, solver: Solver) -> None:
    """Add an arithmetic constraint of the form ``a $ b = c`` or ``a $ b = cd``.

    The function encodes one equation of the puzzle in the Z3 solver.
    The right-hand side may be a one- or two-digit number depending on the
    length of ``digits``.

    Parameters
    ----------
    digits : list of z3.IntRef
        Z3 integer variables representing the digits of the equation.
        Must contain either 3 or 4 elements.
    op : str
        Arithmetic operator, among ``"+"``, ``"-"``, ``"*"``
    solver : z3.Solver
        The Z3 solver where the constraint will be added.

    Raises
    ------
    AssertionError
        If the number of digits is not 3 or 4, or if the operator is invalid.

    Returns
    -------
    None
        The constraint is added directly to the provided solver.
    """
    assert len(digits) in [3,4], "Invalid digits in equation constraint"
    assert op in VALID_OPS, f"Invalid operator {op} in equation constraint"

    lhs = digits[-1] if (len(digits) == 3) else 10*digits[-2] + digits[-1]
    if op == "+":
        solver.add(digits[0] + digits[1] == lhs)
    elif op == "-":
        solver.add(digits[0] - digits[1] == lhs)
    elif op == "*":
        solver.add(digits[0] * digits[1] == lhs)

    return None


def solve_cycle(digits_in: List, ops: List[str], bool_print=False) -> List[int]:
    """Solve a single Garam cycle (a.k.a. mini-Garam).

    The cycle is defined by 4 equations arranged in a loop.
    Each placeholder ``"_"`` in ``digits_in`` represents an unknown digit
    that will be solved for.

    Parameters
    ----------
    digits_in : list
        List of 10 input digits and placeholders ``"_"``.
        The order must follow the internal variable layout:
        ``[a1, b1, c1, a2, c2, a3, c3, a4, b4, c4]``.
    ops : list of str
        List of 4 arithmetic operators (among ``"+", "-", "*"``),
        defining each equation of the cycle.
    bool_print : bool, optional
        If True, print all variable assignments after solving. Default is False.

    Returns
    -------
    list of int
        List of solved digits, or an empty list if no solution is found.
    """
    # 1. Z3 variables
    zsolver = Solver()
    a1, b1, c1 = Int('a1'), Int('b1'), Int('c1')
    a2,     c2 = Int('a2'),            Int('c2')
    a3,     c3 = Int('a3'),            Int('c3')
    a4, b4, c4 = Int('a4'), Int('b4'), Int('c4')
    zvars = [a1, b1, c1, a2, c2, a3, c3, a4, b4, c4]  # same order as digits_in
    tens  = [a3, c3]

    # 2. Constraints
    # Digits
    for d, z in zip(digits_in, zvars):
        if isinstance(d, int):
            # Puzzle-specific
            zsolver.add(z == d)
        elif z in tens:
            # Int must be two digits
            zsolver.add(z >= 1, z <= 9)
        else:
            zsolver.add(z >= 0, z <= 9)

    # Expressions
    oab1, oa12, oc12, oab4 = ops
    add_expression_constraint([a1, b1, c1],     oab1, zsolver)
    add_expression_constraint([a4, b4, c4],     oab4, zsolver)
    add_expression_constraint([a1, a2, a3, a4], oa12, zsolver)
    add_expression_constraint([c1, c2, c3, c4], oc12, zsolver)

    # 3. Resolution
    if zsolver.check() == sat:
        model = zsolver.model()
        if bool_print:
            for z in zvars:
                print(f"{z} = {model[z]}")
        digits_out = [int(model[z].as_long()) for z in zvars]
    else:
        print("No solution found")
        digits_out = []

    return digits_out


def solve_grid(digits_in: List, ops: List[str], bool_print=False) -> List[int]:
    """Solve a full Garam grid.

    The full grid is made of 4 interconnected cycles, each with
    horizontal and vertical equations sharing digits at 2 intersections.
    Each placeholder ``"_"`` in ``digits_in`` represents an unknown digit
    that will be solved for.

    Parameters
    ----------
    digits_in : list
        List of 44 input digits and placeholders ``"_"``.
        The order must follow the internal variable layout:
        ``[a1, b1, c1, e1, f1, g1, a2, c2, d2, e2, g2, a3, c3, e3, g3,
           a4, b4, c4, e4, f4, g4, b5, f5, a6, b6, c6, e6, f6, g6, a7,
           c7, d7, e7, g7, a8, c8, e8, g8, a9, b9, c9, e9, f9, g9]``.
    ops : list of str
        List of 20 arithmetic operators (among ``"+", "-", "*"``),
        defining each equation of the cycle.
    bool_print : bool, optional
        If True, print all variable assignments after solving. Default is False.

    Returns
    -------
    list of int
        List of solved digits, or an empty list if no solution is found.
    """
    # 1. Z3 variables
    zsolver = Solver()
    a1, b1, c1,     e1, f1, g1 = Int('a1'), Int('b1'), Int('c1'),            Int('e1'), Int('f1'), Int('g1')
    a2,     c2, d2, e2,     g2 = Int('a2'),            Int('c2'), Int('d2'), Int('e2'),            Int('g2')
    a3,     c3,     e3,     g3 = Int('a3'),            Int('c3'),            Int('e3'),            Int('g3')
    a4, b4, c4,     e4, f4, g4 = Int('a4'), Int('b4'), Int('c4'),            Int('e4'), Int('f4'), Int('g4')
    b5,                 f5     =            Int('b5'),                                  Int('f5')
    a6, b6, c6,     e6, f6, g6 = Int('a6'), Int('b6'), Int('c6'),            Int('e6'), Int('f6'), Int('g6')
    a7,     c7, d7, e7,     g7 = Int('a7'),            Int('c7'), Int('d7'), Int('e7'),            Int('g7')
    a8,     c8,     e8,     g8 = Int('a8'),            Int('c8'),            Int('e8'),            Int('g8')
    a9, b9, c9,     e9, f9, g9 = Int('a9'), Int('b9'), Int('c9'),            Int('e9'), Int('f9'), Int('g9')

    zvars = [a1, b1, c1, e1, f1, g1, a2, c2, d2, e2, g2, a3, c3, e3, g3,  # same order as digits_in
             a4, b4, c4, e4, f4, g4, b5, f5, a6, b6, c6, e6, f6, g6, a7,
             c7, d7, e7, g7, a8, c8, e8, g8, a9, b9, c9, e9, f9, g9]
    tens  = [a3, c3, e3, g3, a8, c8, e8, g8]

    # 2. Constraints
    # Digits
    for d, z in zip(digits_in, zvars):
        if isinstance(d, int):
            # Puzzle-specific
            zsolver.add(z == d)
        elif z in tens:
            # Int must be two digits
            zsolver.add(z >= 1, z <= 9)
        else:
            zsolver.add(z >= 0, z <= 9)

    # Expressions
    oab1, oef1, oa12, oc12, oe12, og12, ocd2, oab4, oef4, ob45, of45, \
    oab6, oef6, oa67, oc67, oe67, og67, ocd7, oab9, oef9 = ops
    add_expression_constraint([a1, b1, c1],     oab1, zsolver)
    add_expression_constraint([e1, f1, g1],     oef1, zsolver)
    add_expression_constraint([c2, d2, e2],     ocd2, zsolver)
    add_expression_constraint([a4, b4, c4],     oab4, zsolver)
    add_expression_constraint([e4, f4, g4],     oef4, zsolver)
    add_expression_constraint([a6, b6, c6],     oab6, zsolver)
    add_expression_constraint([e6, f6, g6],     oef6, zsolver)
    add_expression_constraint([c7, d7, e7],     ocd7, zsolver)
    add_expression_constraint([a9, b9, c9],     oab9, zsolver)
    add_expression_constraint([e9, f9, g9],     oef9, zsolver)
    add_expression_constraint([a1, a2, a3, a4], oa12, zsolver)
    add_expression_constraint([c1, c2, c3, c4], oc12, zsolver)
    add_expression_constraint([e1, e2, e3, e4], oe12, zsolver)
    add_expression_constraint([g1, g2, g3, g4], og12, zsolver)
    add_expression_constraint([b4, b5, b6],     ob45, zsolver)
    add_expression_constraint([f4, f5, f6],     of45, zsolver)
    add_expression_constraint([a6, a7, a8, a9], oa67, zsolver)
    add_expression_constraint([c6, c7, c8, c9], oc67, zsolver)
    add_expression_constraint([e6, e7, e8, e9], oe67, zsolver)
    add_expression_constraint([g6, g7, g8, g9], og67, zsolver)

    # 3. Resolution
    if zsolver.check() == sat:
        model = zsolver.model()
        if bool_print:
            for z in zvars:
                print(f"{z} = {model[z]}")
        digits_out = [int(model[z].as_long()) for z in zvars]
    else:
        print("No solution found")
        digits_out = []

    return digits_out
