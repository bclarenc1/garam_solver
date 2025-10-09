"""
Main entry point for the Garam solver application.

This script provides a command-line interface to solve either a full Garam grid
or a single "mini-Garam" cycle. The solver reconstructs the numerical and operational
structure of the puzzle, computes the solution, and displays both the input and output
in a human-readable format within the terminal.

The puzzle format follows the conventions used on the official Garam website:
https://www.garamgame.com/garam/garam_en_ligne/avance/index.html

Usage
-----
Run the solver on a full grid (default):
    $ python main.py

Run the solver on a single cycle:
    $ python main.py --mini

Notes
-----
The solver reads a unsolved puzzle from user input and uses the internal
modules under ``solver/`` to build, solve, and display the puzzle:
``builder``, ``solver``, and ``display``.

Modules
-------
builder : Functions to build the puzzle from user input.
solver  : Core solving algorithm.
display : Utilities to render puzzles and their solutions.

@author:  Benjamin Clarenc
@date:    2025-10-09
@github:  bclarenc1
"""

import argparse
import sys
import textwrap

from solver.builder import build_puzzle
from solver.solver import solve_puzzle
from solver.display import display_init_and_sol, display_puzzle

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""
            Solves a full Garam grid or a single cycle (a.k.a. "mini-Garam") that has been inputed.
            The puzzle and its solution are displayed in the terminal.
            Garam grids can be found on the official website:
            https://www.garamgame.com/garam/garam_en_ligne/avance/index.html"""),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-m", "--mini", action="store_true", dest="is_cycle",
                        help="input a single cycle instead of a full grid")
    parser.epilog = textwrap.dedent(f"""\
        examples:
          python {parser.prog}        -> input a full grid
          python {parser.prog} --mini -> input a single cycle""")

    args = parser.parse_args()
    shape = "cycle" if args.is_cycle else "grid"  # pylint: disable=invalid-name

    digits_in, ops = build_puzzle(shape)
    if not digits_in or not ops:
        # user closed the window :(
        sys.exit(0)

    digits_out = solve_puzzle(shape, digits_in, ops)

    if digits_out:
        display_init_and_sol(shape, digits_in, digits_out, ops)
    else:
        # No solution found, display the initial puzzle anyway
        display_puzzle(shape, digits_in, ops)
