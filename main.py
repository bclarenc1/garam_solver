"""Le main file"""

from solver.builder import build_cycle
from solver.solver import solve_cycle
from solver.display import display_init_and_sol

if __name__ == "__main__":
    digits_in, ops = build_cycle()
    digits_out = solve_cycle(digits_in, ops)
    display_init_and_sol(digits_in, digits_out, ops, scope="cycle")
