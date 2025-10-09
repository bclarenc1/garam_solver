# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

from dataclasses import dataclass
from typing import Dict, Callable, List, Optional
import tkinter as tk

@dataclass
class Element:
    """Parent class for Cell, Operator and EqualLabel classes."""
    name: str
    row: int
    col: int
    widget: Optional[object] = None  # placeholder for any widget


@dataclass
class Cell(Element):
    """Represent a cell that visually contains a digit."""
    digit_in:  Optional[str] = None  # initial digit, or "_" if to be solved for
    digit_out: Optional[str] = None  # digit in the solved puzzle
    padx: int = 5
    pady: int = 5


@dataclass
class Operator(Element):
    """Operator between 2 cells."""
    var: Optional[object] = None  # tk.StringVar (if a widget is attached)
    symbol: Optional[str] = None  # "+", "-" or "*"
    padx: int = 3
    pady: int = 5


@dataclass
class EqualLabel(Element):
    """'=' sign between an expression and its numerical value."""
    text: str = "="
    padx: int = 5
    pady: int = 5


class Puzzle:
    """Contain cells, operators and ='s; layout dict provides positions and orders."""
    def __init__(self, layout: Dict):
        self.cells: Dict[str, Cell] = {
            name: Cell(name, *coords)
            for name, coords in layout["cells"].items()
        }
        self.ops: Dict[str, Operator] = {
            name: Operator(name, *coords)
            for name, coords in layout["ops"].items()
        }
        self.labels: Dict[str, EqualLabel] = {
            name: EqualLabel(name, row, col, text="=")
            for name, (row, col) in layout["labels"].items()
        }
        self.digits_order: List[str] = layout["digits_order"]
        self.ops_order:    List[str] = layout["ops_order"]

    def attach_widgets(self, root: tk.Tk,
                       make_digit_entry: Callable[[], tk.Entry],
                       make_operator: Callable[[], tk.StringVar],
                       make_label: Callable[[str], tk.Label],
                       valid_ops: List[str]):
        """Create and place widgets for each element.

        - make_digit_entry: callable to create a tk.Entry
        - make_operator:    callable to create and return a tk.StringVar
        - make_label:       callable to create a tk.Label
        - valid_ops:        list of valid operators for tk.OptionMenu
        """
        # cells -> Entry
        for cell in self.cells.values():
            widget = make_digit_entry()
            cell.widget = widget
            widget.grid(row=cell.row, column=cell.col, padx=cell.padx, pady=cell.pady)

        # operators -> StringVar + OptionMenu
        for op in self.ops.values():
            var = make_operator()
            op.var = var
            op.widget = tk.OptionMenu(root, var, *valid_ops)
            op.widget.grid(row=op.row, column=op.col, padx=op.padx, pady=op.pady)

        # labels -> Label
        for lbl in self.labels.values():
            widget = make_label(lbl.text)
            lbl.widget = widget
            widget.grid(row=lbl.row, column=lbl.col, padx=lbl.padx, pady=lbl.pady)

    def get_digits(self):
        """Return the list of digits in the expected order."""
        out = []
        for name in self.digits_order:
            key = self.cells[name]
            if key.widget:
                val = key.widget.get().strip()
            else:
                val = key.digit_in if key.digit_in is not None else "_"
            out.append(int(val) if val.isdigit() else "_")
        return out

    def get_ops(self):
        """Return the list of operators in the expected order."""
        out = []
        for name in self.ops_order:
            o = self.ops[name]
            if o.var:
                out.append(o.var.get().strip())
            else:
                out.append(o.symbol if o.symbol is not None else "+")
        return out
