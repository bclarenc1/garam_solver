# pylint: disable=too-many-locals
# pylint: disable=line-too-long
# pylint: disable=invalid-name


"""Methods for displaying cycles and grids"""

from typing import List

NB_DIGITS = 44
NB_OPS    = 20
NB_DIGITS_PER_CYCLE = 10
NB_OPS_PER_CYCLE    = 4
VALID_NON_DIGITS = [" ", "_", "?", "X"]  # valid str values for digits

def display_cycle(digits: List, ops: List[str], bool_print=True) -> str:
    """From the lists of digits and operators, display a cycle as:
    a1 $ b1 = c1
    $         $
    a2        c2
    =         =
    a3        c3
    a4 $ b4 = c4
    """

    # 0. Sanity checks
    assert len(digits) == NB_DIGITS_PER_CYCLE, \
           f"Invalid number of digits: expected {NB_DIGITS_PER_CYCLE}, got {len(digits)}"
    invalid_digits = [d for d in digits if not(d in VALID_NON_DIGITS or (isinstance(d, int) and (0 <= d <= 9)))]
    assert not invalid_digits, f"Invalid digit(s): {invalid_digits}"

    assert len(ops) == NB_OPS_PER_CYCLE, \
           f"Invalid number of operators: expected {NB_OPS_PER_CYCLE}, got {len(ops)}"
    ops = [o.strip() for o in ops]
    invalid_ops = [o for o in ops if o not in ("+", "-", "*")]
    assert not invalid_ops, f"Invalid operator(s): {invalid_ops}"

    # 1. Extract digits and operators
    a1, b1, c1, a2, c2, a3, c3, a4, b4, c4 = digits
    oab1, oa12, oc12, oab4 = ops

    # 2. Build cycle
    cycle_str = f"""
    {a1} {oab1} {b1} = {c1}
    {oa12}       {oc12}
    {a2}       {c2}
    =       =
    {a3}       {c3}
    {a4} {oab4} {b4} = {c4}
    """
    if bool_print:
        print(cycle_str)

    return cycle_str


def display_grid(digits: List, ops: List[str], bool_print=True) -> str:
    """From the lists of digits and operators, display the full grid as:
    a1 $ b1 = c1        e1 $ f1 = g1
    $         $         $         $
    a2        c2 $ d2 = e2        g2
    =         =         =         =
    a3        c3        e3        g3
    a4 $ b4 = c4        e4 $ f4 = g4
         $                   $
         b5                  f5
         =                   =
    a6 $ b6 = c6        e6 $ f6 = g6
    $         $         $         $
    a7        c7 $ d7 = e7        g7
    =         =         =         =
    a8        c8        e8        g8
    a9 $ b9 = c9        e9 $ f9 = g9
    """

    # 0. Sanity checks
    assert len(digits) == NB_DIGITS, \
           f"Invalid number of digits: expected {NB_DIGITS}, got {len(digits)}"
    invalid_digits = [d for d in digits if not(d in VALID_NON_DIGITS or (isinstance(d, int) and (0 <= d <= 9)))]
    assert not invalid_digits, f"Invalid digit(s): {invalid_digits}"

    assert len(ops) == NB_OPS, \
           f"Invalid number of operators: expected {NB_OPS}, got {len(ops)}"
    ops = [o.strip() for o in ops]
    invalid_ops = [o for o in ops if o not in ("+", "-", "*")]
    assert not invalid_ops, f"Invalid operator(s): {invalid_ops}"

    # 1. Extract digits and operators
    a1, b1, c1,     e1, f1, g1, \
    a2,     c2, d2, e2,     g2, \
    a3,     c3,     e3,     g3, \
    a4, b4, c4,     e4, f4, g4, \
        b5,             f5,     \
    a6, b6, c6,     e6, f6, g6, \
    a7,     c7, d7, e7,     g7, \
    a8,     c8,     e8,     g8, \
    a9, b9, c9,     e9, f9, g9 = digits
    oab1, oef1,             \
    oa12, oc12, oe12, og12, \
    ocd2,                   \
    oab4, oef4,             \
    ob45, of45,             \
    oab6, oef6,             \
    oa67, oc67, oe67, og67, \
    ocd7,                   \
    oab9, oef9 = ops

    # 2. Build grid
    grid_str = f"""
    {a1} {oab1} {b1} = {c1}       {e1} {oef1} {f1} = {g1}
    {oa12}       {oc12}       {oe12}       {og12}
    {a2}       {c2} {ocd2} {d2} = {e2}       {g2}
    =       =       =       =
    {a3}       {c3}       {e3}       {g3}
    {a4} {oab4} {b4} = {c4}       {e4} {oef4} {f4} = {g4}
        {ob45}               {of45}
        {b5}               {f5}
        =               =
    {a6} {oab6} {b6} = {c6}       {e6} {oef6} {f6} = {g6}
    {oa67}       {oc67}       {oe67}       {og67}
    {a7}       {c7} {ocd7} {d7} = {e7}       {g7}
    =       =       =       =
    {a8}       {c8}       {e8}       {g8}
    {a9} {oab9} {b9} = {c9}       {e9} {oef9} {f9} = {g9}
    """
    if bool_print:
        print(grid_str)

    return grid_str


def display_init_and_sol(digits_in: List, digits_out: List[int], ops: List[str], scope="grid") -> None:
    """Display the initial cycle or grid along with its solution"""

    if scope == "grid":
        str_init   = display_grid(digits_in,  ops, False)
        str_solved = display_grid(digits_out, ops, False)
        offset = 14
    elif scope == "cycle":
        str_init   = display_cycle(digits_in,  ops, False)
        str_solved = display_cycle(digits_out, ops, False)
        offset = 6
    else:
        print("'scope' must be either 'grid' or 'cycle'. Abort'")
        return None

    DEF = "\033[0m"  # default
    BLD = "\033[1m"  # bold
    RED = "\033[91m"
    YLW = "\033[93m"

    print("\n" + " "*offset + "Puzzle" + " "*28 + "Solution")
    for row_i, row_s in zip(str_init.splitlines(), str_solved.splitlines()):
        row_out = f"{row_i.ljust(35)} {row_s}"
        row_colored = row_out.replace("=", f"{BLD}={DEF}").replace("_", f"{RED}_{DEF}")\
                             .replace("+", f"{YLW}+{DEF}").replace("-", f"{YLW}-{DEF}")\
                             .replace("*", f"{YLW}*{DEF}")
        print(row_colored)

    return None
