# pylint: disable=line-too-long

"""
Methods for displaying Garam cycles and grids.

This module provides utilities for rendering Garam puzzles (cycles or full grids)
in a textual format suitable for terminal output. It can also display the initial
puzzle alongside its solved version with color highlighting.
"""
from math import ceil
from typing import Any, Iterator, List
import textwrap

from .constants import VALID_OPS

NB_DIGITS_IN_CYCLE = 10
NB_DIGITS_IN_GRID  = 44
NB_OPS_IN_CYCLE = 4
NB_OPS_IN_GRID  = 20
VALID_NON_DIGITS = [" ", "_", "?", "X"]  # valid str values for digits

DEF = "\033[0m"  # default
BLD = "\033[1m"  # bold
RED = "\033[91m"
YLW = "\033[93m"

def get_next(it: Iterator[Any]) -> Any:
    """Return the next element from an iterator.

    Parameters
    ----------
    it : iterator
        An iterator object. The function advances the iterator by one step
        and returns the next value.

    Returns
    -------
    object
        The next element from the iterator.
    """
    return next(it)


def display_puzzle(shape: str, digits: List, ops: List[str], bool_print=True) -> str:
    """Render a puzzle as a formatted multiline string.

    A cycle is composed of 4 arithmetical statements:
    ```
    a1 $ b1 = c1
    $         $
    a2        c2
    =         =
    a3        c3
    a4 $ b4 = c4
    ```
    where $ in an operator.
    A grid is composed of 20 arithmetical statements arranged in 4 linked cycles:
    ```
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
    ```

    Parameters
    ----------
    shape : {"cycle", "grid"}
        Shape of the puzzle.
    digits : list
        List of 10 (cycle) or 44 (grid) digits or placeholders representing the puzzle state.
    ops : list of str
        List of 4 (cycle) or 20 (grid) operators (among ``"+"``, ``"-"``, ``"*"``).
    bool_print : bool, optional
        If True, the formatted cycle is printed to stdout. Default is True.

    Returns
    -------
    str
        Multiline string representation of the puzzle.

    Raises
    ------
    AssertionError
        If the number or type of digits/operators is invalid.
    """
    assert shape in ["cycle", "grid"], "'shape' must be either 'cycle' or 'grid'"

    if shape == "cycle":
        exp_nb_digits = NB_DIGITS_IN_CYCLE
        exp_nb_ops    = NB_OPS_IN_CYCLE
    else:
        exp_nb_digits = NB_DIGITS_IN_GRID
        exp_nb_ops    = NB_OPS_IN_GRID

    assert len(digits) == exp_nb_digits, f"Invalid number of digits: expected {exp_nb_digits}, got {len(digits)}"
    invalid_digits = [d for d in digits if not(d in VALID_NON_DIGITS or (isinstance(d, int) and (0 <= d <= 9)))]
    assert not invalid_digits, f"Invalid digit(s): {invalid_digits}"

    assert len(ops) == exp_nb_ops, f"Invalid number of operators: expected {exp_nb_ops}, got {len(ops)}"
    ops = [o.strip() for o in ops]
    invalid_ops = [o for o in ops if o not in VALID_OPS]
    assert not invalid_ops, f"Invalid operator(s): {invalid_ops}"

    dit = iter(digits)  # need short..
    oit = iter(ops)     # ..names sry

    if shape == "cycle":
        puzzle_str = textwrap.dedent(f"""
            {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}
            {get_next(oit)}       {get_next(oit)}
            {get_next(dit)}       {get_next(dit)}
            =       =
            {get_next(dit)}       {get_next(dit)}
            {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}
        """)
    else:
        puzzle_str = textwrap.dedent(f"""
            {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}       {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}
            {get_next(oit)}       {get_next(oit)}       {get_next(oit)}       {get_next(oit)}
            {get_next(dit)}       {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}       {get_next(dit)}
            =       =       =       =
            {get_next(dit)}       {get_next(dit)}       {get_next(dit)}       {get_next(dit)}
            {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}       {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}
                {get_next(oit)}               {get_next(oit)}
                {get_next(dit)}               {get_next(dit)}
                =               =
            {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}       {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}
            {get_next(oit)}       {get_next(oit)}       {get_next(oit)}       {get_next(oit)}
            {get_next(dit)}       {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}       {get_next(dit)}
            =       =       =       =
            {get_next(dit)}       {get_next(dit)}       {get_next(dit)}       {get_next(dit)}
            {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}       {get_next(dit)} {get_next(oit)} {get_next(dit)} = {get_next(dit)}
        """)

    if bool_print:
        print(puzzle_str)

    return puzzle_str


# pylint: disable=too-many-locals
def display_init_and_sol(shape: str, digits_in: List, digits_out: List[int], ops: List[str]) -> None:
    """Display a puzzle alongside its solved version on the terminal

    The two representations are printed side by side, with color
    highlighting to differentiate elements.

    Parameters
    ----------
    shape : {"cycle", "grid"}
        Shape of the puzzle.
    digits_in : list
        Initial digits or placeholders of the puzzle.
    digits_out : list of int
        Solved digits corresponding to the same positions.
    ops : list of str
        List of operators used in the puzzle.
    """
    str_init   = display_puzzle(shape, digits_in,  ops, False)
    str_solved = display_puzzle(shape, digits_out, ops, False)

    color_map = {"=": f"{BLD}={DEF}",
                 "_": f"{RED}_{DEF}",
                 "+": f"{YLW}+{DEF}",
                 "-": f"{YLW}-{DEF}",
                 "*": f"{YLW}*{DEF}"}

    # align text with puzzles given puzzle shape, text to display and arbitrary gap;
    # overkillingly generic because cumbersomely abstruse code is so funny-haha
    word1, word2, word3 = "Puzzle", "->", "Solution"
    gap = 9
    width = len(str_init.splitlines()[-1])
    offset      = int(ceil((width-len(word1))/2))
    space_left  = int((width-len(word1))/2) + int(gap/2)  - ceil(len(word2)/2)
    space_right = int((width-len(word3))/2) + ceil(gap/2) - int(len(word2)/2)
    print(f"\n{" "*offset}{word1}{" "*space_left}{word2}{" "*space_right}{word3}")
    for row_i, row_s in zip(str_init.splitlines(), str_solved.splitlines()):
        row_out = f"{row_i.ljust(width)}{" "*gap}{row_s}"
        row_colored = "".join(color_map.get(c, c) for c in row_out)
        print(row_colored)
