# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=invalid-name
# pylint: disable=line-too-long


"""Methods for building cycles and grids"""

from typing import List, Tuple
import tkinter as tk

# Main window
root = tk.Tk()

# Containers for digits and operators
digits = []
ops   = []

# Constants
DGT_BG = "#ffffff"
OPE_BG = "#cce5ff"
DGT_BOX_WIDTH = 2
PAD_DGT_X, PAD_DGT_Y = 5, 5
PAD_OPE_X, PAD_OPE_Y = 3, 5
PAD_EQL_X, PAD_EQL_Y = 5, 5
OPE_ENUM = ["+", "-", "*"]

def make_label(text="=") -> tk.Label:
    """Create a new label widget."""
    return tk.Label(root, text=text, font=("Arial", 14))


def check_valid_input(val) -> bool:
    """Return true iff input is either a single digit or an empty string."""
    return (val == "") or (val.isdigit() and len(val) == 1)


valid_cmd = (root.register(check_valid_input), "%P")

def build_cycle() -> Tuple[List, List[str]]:
    """Generate the HMI for user to enter inputs.

    Output
    ------
    A 2-element tuple made of:
    - digits (list)  : list of inputs digits (ints) or placeholders "_"
    - ops (list[str]): list of input operators ("+", "-" or "*")
    """

    root.title("Single-cycle Garam")

    # Containers for user entries
    txtbox_a1  = tk.Entry(root, width=2, justify="center", bg=DGT_BG, validate="key", validatecommand=valid_cmd)
    cbbox_oab1 = tk.StringVar(value=OPE_ENUM[0])
    box_oab1   = tk.OptionMenu(root, cbbox_oab1, *OPE_ENUM)
    txtbox_b1  = tk.Entry(root, width=2, justify="center", bg=DGT_BG, validate="key", validatecommand=valid_cmd)
    txtbox_c1  = tk.Entry(root, width=2, justify="center", bg=DGT_BG, validate="key", validatecommand=valid_cmd)
    cbbox_oa12 = tk.StringVar(value=OPE_ENUM[0])
    box_oa12   = tk.OptionMenu(root, cbbox_oa12, *OPE_ENUM)
    cbbox_oc12 = tk.StringVar(value=OPE_ENUM[0])
    box_oc12   = tk.OptionMenu(root, cbbox_oc12, *OPE_ENUM)
    txtbox_a2  = tk.Entry(root, width=2, justify="center", bg=DGT_BG, validate="key", validatecommand=valid_cmd)
    txtbox_c2  = tk.Entry(root, width=2, justify="center", bg=DGT_BG, validate="key", validatecommand=valid_cmd)
    txtbox_a3  = tk.Entry(root, width=2, justify="center", bg=DGT_BG, validate="key", validatecommand=valid_cmd)
    txtbox_c3  = tk.Entry(root, width=2, justify="center", bg=DGT_BG, validate="key", validatecommand=valid_cmd)
    txtbox_a4  = tk.Entry(root, width=2, justify="center", bg=DGT_BG, validate="key", validatecommand=valid_cmd)
    cbbox_oab4 = tk.StringVar(value=OPE_ENUM[0])
    box_oab4   = tk.OptionMenu(root, cbbox_oab4, *OPE_ENUM)
    txtbox_b4  = tk.Entry(root, width=2, justify="center", bg=DGT_BG, validate="key", validatecommand=valid_cmd)
    txtbox_c4  = tk.Entry(root, width=2, justify="center", bg=DGT_BG, validate="key", validatecommand=valid_cmd)
    txtboxes = [txtbox_a1, txtbox_b1, txtbox_c1, txtbox_a2, txtbox_c2, txtbox_a3, txtbox_c3, txtbox_a4, txtbox_b4, txtbox_c4]
    cbboxes  = [cbbox_oab1, cbbox_oa12, cbbox_oc12, cbbox_oab4]

    # Place them on the grid
    crow = 0  # current row
    txtbox_a1.grid(   row=crow, column=0, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_oab1.grid(    row=crow, column=1, padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_b1.grid(   row=crow, column=2, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=3, padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_c1.grid(   row=crow, column=4, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1
    box_oa12.grid(row=crow, column=0, padx=PAD_OPE_X, pady=PAD_OPE_Y)
    box_oc12.grid(row=crow, column=4, padx=PAD_OPE_X, pady=PAD_OPE_Y)
    crow += 1
    txtbox_a2.grid(row=crow, column=0, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_c2.grid(row=crow, column=4, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1
    make_label().grid(row=crow, column=0, padx=PAD_EQL_X, pady=PAD_EQL_Y)
    make_label().grid(row=crow, column=4, padx=PAD_EQL_X, pady=PAD_EQL_Y)
    crow += 1
    txtbox_a3.grid(row=crow, column=0, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_c3.grid(row=crow, column=4, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1
    txtbox_a4.grid(   row=crow, column=0, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_oab4.grid(    row=crow, column=1, padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_b4.grid(   row=crow, column=2, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=3, padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_c4.grid(   row=crow, column=4, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1

    def get_values() -> None:
        """Store input values"""
        for txtbox in txtboxes:
            digit = txtbox.get().strip()
            if digit == "":
                digit = "_"
            else:
                digit = int(digit)
            digits.append(digit)
        for cbbox in cbboxes:
            ops.append(cbbox.get().strip())

        root.destroy()


    # OK button
    btn_OK = tk.Button(root, text="Solve", justify="right", command=get_values)
    btn_OK.grid(row=crow, column=0, columnspan=5)

    # Display window
    root.mainloop()

    return (digits, ops)
