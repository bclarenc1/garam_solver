# pylint: disable=no-member
# pylint: disable=useless-return
# pylint: disable=too-many-locals
# pylint: disable=line-too-long

"""Methods for solving cycles and grids"""

from typing import List
from z3 import Int, Solver, sat

VALID_OPS = ["+", "-", "*"]

def add_expression_constraint(digits: List, op: str, solver: Solver) -> None:
    """Create a constraint on an expression.
    The expression is either "a $ b = c" or "a $ b = cd",
    where $ is the operator and cd is a 2-digit int.

    Inputs
    ------
    - digits (list)  : list of 3 or 4 Z3 Ints
    - op     (str)   : "+", "-" or "*"
    - solver (Solver): Z3 solver to store the constraint
    """
    assert len(digits) in [3,4], "Invalid digits in expression constraint"
    assert op in VALID_OPS, f"Invalid operator {op} in expression constraint"

    lhs = digits[-1] if (len(digits) == 3) else 10*digits[-2] + digits[-1]
    if op == "+":
        solver.add(digits[0] + digits[1] == lhs)
    elif op == "-":
        solver.add(digits[0] - digits[1] == lhs)
    elif op == "*":
        solver.add(digits[0] * digits[1] == lhs)

    return None


def solve_cycle(digits_in: List, ops: List[str], bool_print=False) -> List[int]:
    """Solve a cycle given its digits and operators.

    Inputs
    ------
    - digits_in (list):  list of initial digits (native ints) and placeholders "_"
    - ops (list [str]):  list of operators (among "+", "-", "*")
    - bool_print (bool): if True, display all digit values. Default is False

    Output
    ------
    - digits_in (list): list of digits that solve the puzzle, or empty list if
                        no solution is found
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
    """Solve a cycle given its digits and operators.
    Inputs
    ------
    - digits_in (list):  list of initial digits (native ints) and placeholders "_"
    - ops (list [str]):  list of operators (among "+", "-", "*")
    - bool_print (bool): if True, display all digit values. Default is False

    Output
    ------
    - digits_in (list): list of digits that solve the puzzle, or empty list if
                        no solution is found
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
