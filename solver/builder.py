"""
Builder module for Garam solver GUI input forms.

This module defines functions to dynamically construct Tkinter interfaces
used to input a Garam puzzle (single cycle or full grid).
Each entry widget captures digits and operators forming the puzzle structure.

The resulting lists of digits and operators are returned for further
processing by the solver module.

Modules
-------
tkinter : Used for creating the graphical interface.

Functions
---------
build_puzzle(shape) -> Tuple[List, List[str]]
    Launch the UI to enter a puzzle.
make_digit_entry() -> tk.Entry
    Create and configure a new Entry widget for digit input.
make_operator() -> tk.StringVar
    Create a new operator selector variable (bound to an OptionMenu).
make_label(text="=") -> tk.Label
    Create a label widget, typically displaying "=".
check_valid_input(val) -> bool
    Validate digit inputs to ensure single-digit or empty string.
"""

from typing import List, Tuple
import tkinter as tk

from .puzzle import Puzzle
from .constants import VALID_OPS

# Main window
root = tk.Tk()

# Constants: graphical and operators
DGT_BG = "#ffffff"
OPE_BG = "#cce5ff"
DGT_BOX_WIDTH = 2
PAD_DGT_X, PAD_DGT_Y = 5, 5
PAD_OPE_X, PAD_OPE_Y = 3, 5
PAD_EQL_X, PAD_EQL_Y = 5, 5

CYCLE_LAYOUT = {
    "cells": {"a1":(0,0), "b1":(0,2), "c1":(0,4),
              "a2":(2,0),             "c2":(2,4),
              "a3":(4,0),             "c3":(4,4),
              "a4":(6,0), "b4":(6,2), "c4":(6,4)},

    "ops": {"oab1":(0,1), "oa12":(1,0), "oc12":(1,4), "oab4":(6,1)},

    "labels": {"ebc1":(0,3), "ea23":(3,0), "ec23":(3,4), "ebc4":(6,3)},

    "digits_order": ["a1", "b1", "c1", "a2", "c2", "a3", "c3", "a4", "b4", "c4"],

    "ops_order": ["oab1", "oa12", "oc12", "oab4"]
}

GRID_LAYOUT = {
    "cells":  {"a1":(0,0),  "b1":(0,2),  "c1":(0,4),               "e1":(0,8),  "f1":(0,10),  "g1":(0,12),
               "a2":(2,0),               "c2":(2,4),  "d2":(2,6),  "e2":(2,8),                "g2":(2,12),
               "a3":(4,0),               "c3":(4,4),               "e3":(4,8),                "g3":(4,12),
               "a4":(6,0),  "b4":(6,2),  "c4":(6,4),               "e4":(6,8),  "f4":(6,10),  "g4":(6,12),
                            "b5":(8,2),                                         "f5":(8,10),
               "a6":(10,0), "b6":(10,2), "c6":(10,4),              "e6":(10,8), "f6":(10,10), "g6":(10,12),
               "a7":(12,0),              "c7":(12,4), "d7":(12,6), "e7":(12,8),               "g7":(12,12),
               "a8":(14,0),              "c8":(14,4),              "e8":(14,8),               "g8":(14,12),
               "a9":(16,0), "b9":(16,2), "c9":(16,4),              "e9":(16,8), "f9":(16,10), "g9":(16,12)},

    "ops": {"oab1":(0,1),  "oef1":(0,9),
            "oa12":(1,0),  "oc12":(1,4),  "oe12":(1,8),  "og12":(1,12),
            "ocd2":(2,5),
            "oab4":(6,1),  "oef4":(6,9),
            "ob45":(7,2),  "of45":(7,10),
            "oab6":(10,1), "oef6":(10,9),
            "oa67":(11,0), "oc67":(11,4), "oe67":(11,8), "og67":(11,12),
            "ocd7":(12,5),
            "oab9":(16,1), "oef9":(16,9)},

    "labels": {"ebc1":(0,3),  "efg1":(0,11),
               "ede2":(2,7),
               "ea23":(3,0),  "ec23":(3,4),   "ee23":(3,8),  "eg23":(3,12),
               "ebc4":(6,3),  "efg4":(6,11),
               "eb56":(9,2),  "ef56":(9,10),
               "ebc6":(10,3), "efg6":(10,11),
               "ede7":(12,7),
               "ea78":(13,0), "ec78":(13,4),  "ee78":(13,8), "eg78":(13,12),
               "ebc9":(16,3), "efg9":(16,11)},

    "digits_order": ["a1", "b1", "c1", "e1", "f1", "g1", "a2", "c2", "d2", "e2", "g2",
                     "a3", "c3", "e3", "g3", "a4", "b4", "c4", "e4", "f4", "g4",
                     "b5", "f5",
                     "a6", "b6", "c6", "e6", "f6", "g6", "a7", "c7", "d7", "e7", "g7",
                     "a8", "c8", "e8", "g8", "a9", "b9", "c9", "e9", "f9", "g9"],

    "ops_order": ["oab1", "oef1", "oa12", "oc12", "oe12", "og12", "ocd2", "oab4", "oef4",
                  "ob45", "of45",
                  "oab6", "oef6", "oa67", "oc67", "oe67", "og67", "ocd7", "oab9", "oef9"]
}

def check_valid_input(val) -> bool:
    """Return True iff input is either a single digit or an empty string."""
    return (val == "") or (val.isdigit() and len(val) == 1)

valid_cmd = (root.register(check_valid_input), "%P")


def make_digit_entry() -> tk.Entry:
    """Create and return a new digit entry widget."""
    return tk.Entry(root, width=2, justify="center", bg=DGT_BG,
                    validate="key", validatecommand=valid_cmd)


def make_operator() -> tk.StringVar:
    """Create and return a new operator variable for OptionMenu."""
    return tk.StringVar(value=VALID_OPS[0])


def make_label(text="=") -> tk.Label:
    """Create and return a label widget."""
    return tk.Label(root, text=text, font=("Arial", 14))


def build_puzzle(shape) -> Tuple[List, List[str]]:
    """Create and display the UI for entering a puzzle (cycle or grid).

    The layout allows the user to enter single-digit values and select
    operators between them. When the user validates the form, the input
    values and operators are collected and returned.

    Parameters
    ----------
    shape : {"cycle", "grid"}
        Shape of the puzzle.

    Returns
    -------
    tuple of list and list[str]
        A tuple containing:
        - digits : list
            Input digits as integers or placeholders "_".
        - ops : list of str
            Selected operators ("+", "-", "*").
    """
    assert shape in ["cycle", "grid"], "'shape' must be either 'cycle' or 'grid'"

    if shape == "cycle":
        root.title("Mini-Garam")
        puzzle = Puzzle(CYCLE_LAYOUT)
        columnspan = 5
    else:
        root.title("Full grid Garam")
        puzzle = Puzzle(GRID_LAYOUT)
        columnspan = 13
    puzzle.attach_widgets(root, make_digit_entry, make_operator, make_label, VALID_OPS)

    # Containers for digits and operators
    digits = []
    ops = []

    def get_values() -> None:
        """Store input values from the GUI and close the window."""
        digits.clear()
        ops.clear()
        digits.extend(puzzle.get_digits())
        ops.extend(puzzle.get_ops())
        root.destroy()

    # OK button
    btn_ok = tk.Button(root, text="Solve", justify="right", command=get_values)
    last_row = max(c.row for c in puzzle.cells.values()) + 1
    btn_ok.grid(row=last_row, column=0, columnspan=columnspan)

    # Display window
    root.mainloop()

    return (digits, ops)
