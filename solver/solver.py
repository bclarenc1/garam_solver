"""
Methods for solving Garam puzzles (cycles and full grids) using Z3.

This module defines helper functions to translate Garam constraints into Z3 formulas and solve them.
"""

from typing import Dict, List, Tuple
from z3 import Int, Solver, sat

from .constants import VALID_OPS


def build_z3_vars(shape: str) -> Tuple[Dict[str, Int], List[Int], List[Int]]:
    """Create Z3 integer variables for a cycle or a full grid.

    Parameters
    ----------
    shape : {"cycle", "grid"}
        Shape of the puzzle.

    Returns
    -------
    zvars_dict : dict[str, Int]
        Dictionary mapping variable names to their Z3 integer objects.
    zvars : list[Int]
        List of Z3 integer variables in the order defined by the puzzle layout.
    tens : list[Int]
        List of variables that represent digits in the tens position,
        and therefore that cannot be zero.
    """
    if shape == "cycle":
        digit_names = ["a1","b1","c1","a2","c2","a3","c3","a4","b4","c4"]
        ten_names   = ["a3","c3"]
    else:
        digit_names = ["a1","b1","c1","e1","f1","g1","a2","c2","d2","e2","g2","a3","c3","e3","g3",
                       "a4","b4","c4","e4","f4","g4","b5","f5","a6","b6","c6","e6","f6","g6",
                       "a7","c7","d7","e7","g7","a8","c8","e8","g8","a9","b9","c9","e9","f9","g9"]
        ten_names   = ["a3","c3","e3","g3","a8","c8","e8","g8"]

    zvars_dict = {name: Int(name) for name in digit_names}
    zvars = [zvars_dict[name] for name in digit_names]
    tens  = [zvars_dict[name] for name in ten_names]

    return (zvars_dict, zvars, tens)


def add_equation_constraint(digits: List, op: str, solver: Solver) -> None:
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
        Arithmetic operator (among ``"+"``, ``"-"``, ``"*"``).
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


# pylint: disable=too-many-locals
def build_equation_constraints(shape: str, ops: List[str], zvars_dict: Dict[str, Int]
                               ) -> List[Tuple[List[Int], str]]:
    """Return a list of equation constraints for a puzzle.

    Each constraint is a tuple of Z3 variables involved in the equation
    and the operator defining the arithmetic relation.

    Parameters
    ----------
    shape : {"cycle", "grid"}
        Shape of the puzzle.
    ops : list of str
        List of 4 (cycle) or 20 (grid) arithmetic operators for the equations.
    zvars_dict : dict[str, Int]
        Dictionary mapping variable names to their Z3 integer objects.

    Returns
    -------
    list of tuple(list[Int], str)
        Each tuple contains the elements for one constraint:
        - the list of Z3 variables involved in the equation
        - the operator as a string
    """
    if shape == "cycle":
        oab1, oa12, oc12, oab4 = ops
        eqn_constraints = [
            (["a1","b1","c1"], oab1), (["a4","b4","c4"], oab4),
            (["a1","a2","a3","a4"], oa12), (["c1","c2","c3","c4"], oc12)]
    else:
        (oab1, oef1, oa12, oc12, oe12, og12, ocd2, oab4, oef4, ob45, of45,
         oab6, oef6, oa67, oc67, oe67, og67, ocd7, oab9, oef9) = ops
        eqn_constraints = [
            (["a1","b1","c1"], oab1),      (["e1","f1","g1"], oef1), (["c2","d2","e2"], ocd2),
            (["a4","b4","c4"], oab4),      (["e4","f4","g4"], oef4),
            (["a6","b6","c6"], oab6),      (["e6","f6","g6"], oef6), (["c7","d7","e7"], ocd7),
            (["a9","b9","c9"], oab9),      (["e9","f9","g9"], oef9),
            (["a1","a2","a3","a4"], oa12), (["c1","c2","c3","c4"], oc12),
            (["e1","e2","e3","e4"], oe12), (["g1","g2","g3","g4"], og12),
            (["b4","b5","b6"], ob45),      (["f4","f5","f6"], of45),
            (["a6","a7","a8","a9"], oa67), (["c6","c7","c8","c9"], oc67),
            (["e6","e7","e8","e9"], oe67), (["g6","g7","g8","g9"], og67)]

    return [([zvars_dict[dgt_name] for dgt_name in dgt_names], op)
            for dgt_names, op in eqn_constraints]


# pylint: disable=too-many-locals
def solve_puzzle(shape: str, digits_in: List, ops: List[str], bool_print=False) -> List[int]:
    """Solve a cycle or a full grid.

    A cycle is defined by 4 equations arranged in a loop. A full grid is made
    of 4 interconnected cycles, each with horizontal and vertical equations
    sharing digits at 2 intersections. Each placeholder ``"_"`` in ``digits_in``
    represents an unknown digit that will be solved for.

    Parameters
    ----------
    digits_in : list
        List of 10 (cycle) or 44 (grid) input digits and placeholders ``"_"``.
        The order must follow the internal variable layout:
        ``[a1, b1, c1, a2, c2, a3, c3, a4, b4, c4]`` for a cycle,
        ``[a1, b1, c1, e1, f1, g1, a2, c2, d2, e2, g2, a3, c3, e3, g3,
           a4, b4, c4, e4, f4, g4, b5, f5, a6, b6, c6, e6, f6, g6, a7,
           c7, d7, e7, g7, a8, c8, e8, g8, a9, b9, c9, e9, f9, g9]`` for a grid.
    ops : list of str
        List of 4 (cycle) or 20 (grid) arithmetic operators (among
        ``"+"``, ``"-"``, ``"*"``), defining each equation of the cycle.
    bool_print : bool, optional
        If True, print all variable assignments after solving. Default is False.

    Returns
    -------
    list of int
        List of solved digits, or an empty list if no solution is found.
    """
    assert shape in ["cycle", "grid"], "'shape' must be either 'cycle' or 'grid'"

    zsolver = Solver()

    # Digit constraints
    zvars_dict, zvars, tens = build_z3_vars(shape)
    for d, z in zip(digits_in, zvars):
        if isinstance(d, int):
            # Puzzle-specific
            zsolver.add(z == d)
        elif z in tens:
            # Int must be two digits
            zsolver.add(z >= 1, z <= 9)
        else:
            zsolver.add(z >= 0, z <= 9)

    # Equation constraints
    eqn_constraints = build_equation_constraints(shape, ops, zvars_dict)
    for these_zvars, op in eqn_constraints:
        add_equation_constraint(these_zvars, op, zsolver)

    # Resolution
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
