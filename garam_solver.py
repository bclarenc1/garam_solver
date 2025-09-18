# pylint: disable=line-too-long
# pylint: disable=invalid-name

"""
Main file to run the Garam solver algorithm.

@author: Benjamin Clarenc
@date: 2025-09-18
"""

import os
import sys
import argparse

from solver.builder import build_cycle, build_grid
from solver.solver import solve_cycle, solve_grid
from solver.display import display_init_and_sol, display_cycle, display_grid

if __name__ == "__main__":
    sname = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        description="Solves a full Garam grid or a single cycle (aka 'mini-Garam') that has been inputed.",
        epilog=("Examples:\n"
                + f"  python {sname}        -> input a full grid\n"
                + f"  python {sname} --mini -> input a single cycle\n"),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-m", "--mini", action='store_true', dest="use_cycle",
                        help="input a single cycle instead of a full grid")

    args = parser.parse_args()

    if args.use_cycle:
        scope = "cycle"
        digits_in, ops = build_cycle()
        digits_out = solve_cycle(digits_in, ops)
    else:
        scope = "grid"
        digits_in, ops = build_grid()
        digits_out = solve_grid(digits_in, ops)

    if digits_out:
        display_init_and_sol(digits_in, digits_out, ops, scope=scope)
    elif args.use_cycle:
        display_cycle(digits_in, ops)
    else:
        display_grid(digits_in, ops)
