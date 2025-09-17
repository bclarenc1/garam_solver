# pylint: disable=no-member        # pylint finds phantom errors, boo this man!
# pylint: disable=useless-return   # explicit is better than implicit
# pylint: disable=too-many-locals  # I have no choice

"""Methods for solving cycles and grid"""


from z3 import Int, Solver, sat

VALID_OPES = ["+", "-", "*"]

def add_expression_constraint(digits, op, solver):
    """Create a constraint on an expression.
    The expression is either "a @ b = c" or "a @ b = cd",
    where @ is the operator and cd is a 2-digit int.

    Inputs
    ------
    - digits (list)  : list of 3 or 4 Z3 Ints
    - op     (str)   : "+", "-" or "*"
    - solver (Solver): Z3 solver to store the constraint
    """
    assert len(digits) in [3,4], "Invalid digits in expression constraint"
    assert op in VALID_OPES, f"Invalid operator {op} in expression constraint"

    lhs = digits[-1] if (len(digits) == 3) else 10*digits[-2] + digits[-1]
    if op == "+":
        solver.add(digits[0] + digits[1] == lhs)
    elif op == "-":
        solver.add(digits[0] - digits[1] == lhs)
    elif op == "*":
        solver.add(digits[0] * digits[1] == lhs)

    return None


def solve_cycle(digits_in, ops):
    """Solve a cycle given its digits and operators
    Inputs
    ------
    - digits_in (list): list of initial digits (native ints) and placeholders "_"
    - ops (list [str]): list of operators (among "+", "-", "*")

    Output
    ------
    - digits_in (list): list of digits that solve the puzzle, or empty list if
                        no solution is found
    """
    # 1. Z3 variables
    zsolver = Solver()
    a1 = Int('a1')
    b1 = Int('b1')
    c1 = Int('c1')
    a2 = Int('a2')
    c2 = Int('c2')
    a3 = Int('a3')
    c3 = Int('c3')
    a4 = Int('a4')
    b4 = Int('b4')
    c4 = Int('c4')
    zvars = [a1, b1, c1, a2, c2, a3, c3, a4, b4, c4]  # same order as arg digits
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
    add_expression_constraint([a1, a2, a3, a4], oa12, zsolver)
    add_expression_constraint([c1, c2, c3, c4], oc12, zsolver)
    add_expression_constraint([a4, b4, c4],     oab4, zsolver)
    for c in zsolver.assertions():
        print(c)

    # 3. Resolution
    if zsolver.check() == sat:
        model = zsolver.model()
        for z in zvars:
            print(f"{z} = {model[z]}")
        digits_out = [int(model[z].as_long()) for z in zvars]
    else:
        print("No solution found")
        digits_out = []

    return digits_out
