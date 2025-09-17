# pylint: disable=too-many-locals
# pylint: disable=line-too-long
# pylint: disable=invalid-name


"""Methods for displaying cycles and grids"""

NB_DIGITS = 44
NB_OPS    = 20
NB_DIGITS_PER_CYCLE = 10
NB_OPS_PER_CYCLE    = 4
VALID_NON_DIGITS = [" ", "_", "?", "X"]  # valid str values for digits

def display_cycle(digits: list, ops: list, bool_print=True) -> str:
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


def display_grid(digits: list, ops: list, bool_print=True) -> str:
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


def display_init_and_sol(init_digits: list, solved_digits: list, ops: list, scope="grid") -> str:
    """Display the initial cycle or grid along with its solution"""

    if scope == "grid":
        str_init   = display_grid(init_digits,   ops, False)
        str_solved = display_grid(solved_digits, ops, False)
        offset = 14
    elif scope == "cycle":
        str_init   = display_cycle(init_digits,   ops, False)
        str_solved = display_cycle(solved_digits, ops, False)
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


# quick tests
if __name__ == "__main__":
    _ = "_"
    cycle_init_digits   = [_,1,7,_,_,1,3,_,2,_]
    cycle_solved_digits = [8,1,7,9,5,1,3,7,2,5]
    cycle_ops           = ["-","+","*","-"]
    display_init_and_sol(cycle_init_digits, cycle_solved_digits, cycle_ops, scope="cycle")

    grid_init_digits   = [_,3,_,_,_,_,5,_,1,_,6,_,_,_,_,_,_,_,_,_,_,1,4,_,_,_,_,_,_,_,_,4,_,7,_,_,2,_,_,4,_,_,_,_]
    grid_solved_digits = [7,3,4,9,0,9,5,9,1,9,6,3,3,8,1,5,1,6,1,4,5,1,4,9,2,7,5,0,5,8,9,4,5,7,7,1,2,3,2,4,6,5,1,5]
    grid_ops           = ["-","-","*","*","*","+","*","+","+","+","-","-","+","*","+","*","*","-","+","*"]
    display_init_and_sol(grid_init_digits, grid_solved_digits, grid_ops, scope="grid")
