# pylint: disable=line-too-long
# pylint: disable=invalid-name

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
The solver reads a grid or cycle from user input and uses the internal
modules under `solver/` to build, solve, and display the puzzle:
`builder`, `solver`, and `display`.

Modules
-------
builder : Functions to build the grid or cycle from user input.
solver  : Core solving algorithms for grids and cycles.
display : Utilities to render puzzles and their solutions.

@author:  Benjamin Clarenc
@date:    2025-10-07
@github:  bclarenc1
"""

import textwrap
import argparse
import sys

from solver.builder import build_cycle, build_grid
from solver.solver import solve_cycle, solve_grid
from solver.display import display_init_and_sol, display_cycle, display_grid

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""
            Solves a full Garam grid or a single cycle (a.k.a. 'mini-Garam') that has been inputed.
            The puzzle and its solution are displayed in the terminal.
            Grids can be found e.g. on the official website, like
            https://www.garamgame.com/garam/garam_en_ligne/avance/index.html"""),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-m", "--mini", action="store_true", dest="use_cycle",
                        help="input a single cycle instead of a full grid")
    parser.epilog = textwrap.dedent(f"""\
        examples:
          python {parser.prog}        -> input a full grid
          python {parser.prog} --mini -> input a single cycle""")

    args = parser.parse_args()

    if args.use_cycle:
        scope = "cycle"
        digits_in, ops = build_cycle()
        if not digits_in or not ops:
            # user closed the window :(
            sys.exit(0)
        digits_out = solve_cycle(digits_in, ops)
    else:
        scope = "grid"
        digits_in, ops = build_grid()
        if not digits_in or not ops:
            sys.exit(0)
        digits_out = solve_grid(digits_in, ops)

    if digits_out:
        display_init_and_sol(digits_in, digits_out, ops, scope=scope)
    elif args.use_cycle:
        display_cycle(digits_in, ops)
    else:
        display_grid(digits_in, ops)
