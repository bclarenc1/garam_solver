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
ops    = []

# Constants
DGT_BG = "#ffffff"
OPE_BG = "#cce5ff"
DGT_BOX_WIDTH = 2
PAD_DGT_X, PAD_DGT_Y = 5, 5
PAD_OPE_X, PAD_OPE_Y = 3, 5
PAD_EQL_X, PAD_EQL_Y = 5, 5
OPE_ENUM = ["+", "-", "*"]


def check_valid_input(val) -> bool:
    """Return true iff input is either a single digit or an empty string."""
    return (val == "") or (val.isdigit() and len(val) == 1)

valid_cmd = (root.register(check_valid_input), "%P")


def make_digit_entry() -> tk.Entry:
    """Create a new digit entry widget."""
    return tk.Entry(root, width=2, justify="center", bg=DGT_BG, validate="key", validatecommand=valid_cmd)


def make_operator() -> tk.StringVar:
    """Create a new operator widget for."""
    return tk.StringVar(value=OPE_ENUM[0])


def make_label(text="=") -> tk.Label:
    """Create a new label widget."""
    return tk.Label(root, text=text, font=("Arial", 14))


def build_cycle() -> Tuple[List, List[str]]:
    """Generate the HMI for user to enter cycle inputs.

    Output
    ------
    A 2-element tuple made of:
    - digits (list)  : list of inputs digits (ints) or placeholders "_"
    - ops (list[str]): list of input operators ("+", "-" or "*")
    """
    root.title("Mini-Garam")

    # Containers for user entries
    txtbox_a1  = make_digit_entry()
    cbbox_oab1 = make_operator()
    box_oab1   = tk.OptionMenu(root, cbbox_oab1, *OPE_ENUM)
    txtbox_b1  = make_digit_entry()
    txtbox_c1  = make_digit_entry()
    cbbox_oa12 = make_operator()
    box_oa12   = tk.OptionMenu(root, cbbox_oa12, *OPE_ENUM)
    cbbox_oc12 = make_operator()
    box_oc12   = tk.OptionMenu(root, cbbox_oc12, *OPE_ENUM)
    txtbox_a2  = make_digit_entry()
    txtbox_c2  = make_digit_entry()
    txtbox_a3  = make_digit_entry()
    txtbox_c3  = make_digit_entry()
    txtbox_a4  = make_digit_entry()
    cbbox_oab4 = make_operator()
    box_oab4   = tk.OptionMenu(root, cbbox_oab4, *OPE_ENUM)
    txtbox_b4  = make_digit_entry()
    txtbox_c4  = make_digit_entry()
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
        """Store input values."""
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


def build_grid() -> Tuple[List, List[str]]:
    """Generate the HMI for user to enter grid inputs.

    Output
    ------
    A 2-element tuple made of:
    - digits (list)  : list of inputs digits (ints) or placeholders "_"
    - ops (list[str]): list of input operators ("+", "-" or "*")
    """
    root.title("Full grid Garam")

    # Containers for user entries
    txtbox_a1  = make_digit_entry()
    cbbox_oab1 = make_operator()
    box_oab1   = tk.OptionMenu(root, cbbox_oab1, *OPE_ENUM)
    txtbox_b1  = make_digit_entry()
    txtbox_c1  = make_digit_entry()
    txtbox_e1  = make_digit_entry()
    cbbox_oef1 = make_operator()
    box_oef1   = tk.OptionMenu(root, cbbox_oef1, *OPE_ENUM)
    txtbox_f1  = make_digit_entry()
    txtbox_g1  = make_digit_entry()

    cbbox_oa12 = make_operator()
    box_oa12   = tk.OptionMenu(root, cbbox_oa12, *OPE_ENUM)
    cbbox_oc12 = make_operator()
    box_oc12   = tk.OptionMenu(root, cbbox_oc12, *OPE_ENUM)
    cbbox_oe12 = make_operator()
    box_oe12   = tk.OptionMenu(root, cbbox_oe12, *OPE_ENUM)
    cbbox_og12 = make_operator()
    box_og12   = tk.OptionMenu(root, cbbox_og12, *OPE_ENUM)

    txtbox_a2  = make_digit_entry()
    txtbox_c2  = make_digit_entry()
    cbbox_ocd2 = make_operator()
    box_ocd2   = tk.OptionMenu(root, cbbox_ocd2, *OPE_ENUM)
    txtbox_d2  = make_digit_entry()
    txtbox_e2  = make_digit_entry()
    txtbox_g2  = make_digit_entry()

    txtbox_a3  = make_digit_entry()
    txtbox_c3  = make_digit_entry()
    txtbox_e3  = make_digit_entry()
    txtbox_g3  = make_digit_entry()

    txtbox_a4  = make_digit_entry()
    cbbox_oab4 = make_operator()
    box_oab4   = tk.OptionMenu(root, cbbox_oab4, *OPE_ENUM)
    txtbox_b4  = make_digit_entry()
    txtbox_c4  = make_digit_entry()
    txtbox_e4  = make_digit_entry()
    cbbox_oef4 = make_operator()
    box_oef4   = tk.OptionMenu(root, cbbox_oef4, *OPE_ENUM)
    txtbox_f4  = make_digit_entry()
    txtbox_g4  = make_digit_entry()

    cbbox_ob45 = make_operator()
    box_ob45   = tk.OptionMenu(root, cbbox_ob45, *OPE_ENUM)
    cbbox_of45 = make_operator()
    box_of45   = tk.OptionMenu(root, cbbox_of45, *OPE_ENUM)

    txtbox_b5  = make_digit_entry()
    txtbox_f5  = make_digit_entry()

    txtbox_a6  = make_digit_entry()
    cbbox_oab6 = make_operator()
    box_oab6   = tk.OptionMenu(root, cbbox_oab6, *OPE_ENUM)
    txtbox_b6  = make_digit_entry()
    txtbox_c6  = make_digit_entry()
    txtbox_e6  = make_digit_entry()
    cbbox_oef6 = make_operator()
    box_oef6   = tk.OptionMenu(root, cbbox_oef6, *OPE_ENUM)
    txtbox_f6  = make_digit_entry()
    txtbox_g6  = make_digit_entry()

    cbbox_oa67 = make_operator()
    box_oa67   = tk.OptionMenu(root, cbbox_oa67, *OPE_ENUM)
    cbbox_oc67 = make_operator()
    box_oc67   = tk.OptionMenu(root, cbbox_oc67, *OPE_ENUM)
    cbbox_oe67 = make_operator()
    box_oe67   = tk.OptionMenu(root, cbbox_oe67, *OPE_ENUM)
    cbbox_og67 = make_operator()
    box_og67   = tk.OptionMenu(root, cbbox_og67, *OPE_ENUM)

    txtbox_a7  = make_digit_entry()
    txtbox_c7  = make_digit_entry()
    cbbox_ocd7 = make_operator()
    box_ocd7   = tk.OptionMenu(root, cbbox_ocd7, *OPE_ENUM)
    txtbox_d7  = make_digit_entry()
    txtbox_e7  = make_digit_entry()
    txtbox_g7  = make_digit_entry()

    txtbox_a8  = make_digit_entry()
    txtbox_c8  = make_digit_entry()
    txtbox_e8  = make_digit_entry()
    txtbox_g8  = make_digit_entry()

    txtbox_a9  = make_digit_entry()
    cbbox_oab9 = make_operator()
    box_oab9   = tk.OptionMenu(root, cbbox_oab9, *OPE_ENUM)
    txtbox_b9  = make_digit_entry()
    txtbox_c9  = make_digit_entry()
    txtbox_e9  = make_digit_entry()
    cbbox_oef9 = make_operator()
    box_oef9   = tk.OptionMenu(root, cbbox_oef9, *OPE_ENUM)
    txtbox_f9  = make_digit_entry()
    txtbox_g9  = make_digit_entry()

    txtboxes = [txtbox_a1, txtbox_b1, txtbox_c1,            txtbox_e1, txtbox_f1, txtbox_g1,
                txtbox_a2,            txtbox_c2, txtbox_d2, txtbox_e2,            txtbox_g2,
                txtbox_a3,            txtbox_c3,            txtbox_e3,            txtbox_g3,
                txtbox_a4, txtbox_b4, txtbox_c4,            txtbox_e4, txtbox_f4, txtbox_g4,
                           txtbox_b5,                                  txtbox_f5,
                txtbox_a6, txtbox_b6, txtbox_c6,            txtbox_e6, txtbox_f6, txtbox_g6,
                txtbox_a7,            txtbox_c7, txtbox_d7, txtbox_e7,            txtbox_g7,
                txtbox_a8,            txtbox_c8,            txtbox_e8,            txtbox_g8,
                txtbox_a9, txtbox_b9, txtbox_c9,            txtbox_e9, txtbox_f9, txtbox_g9]

    cbboxes  = [cbbox_oab1, cbbox_oef1,
                cbbox_oa12, cbbox_oc12, cbbox_oe12, cbbox_og12,
                cbbox_ocd2,
                cbbox_oab4, cbbox_oef4,
                cbbox_ob45, cbbox_of45,
                cbbox_oab6, cbbox_oef6,
                cbbox_oa67, cbbox_oc67, cbbox_oe67, cbbox_og67,
                cbbox_ocd7,
                cbbox_oab9, cbbox_oef9]

    # Place them on the grid
    crow = 0  # current row
    txtbox_a1.grid(   row=crow, column=0,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_oab1.grid(    row=crow, column=1,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_b1.grid(   row=crow, column=2,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=3,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_c1.grid(   row=crow, column=4,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_e1.grid(   row=crow, column=8,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_oef1.grid(    row=crow, column=9,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_f1.grid(   row=crow, column=10, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=11, padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_g1.grid(   row=crow, column=12, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1
    box_oa12.grid(row=crow, column=0,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    box_oc12.grid(row=crow, column=4,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    box_oe12.grid(row=crow, column=8,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    box_og12.grid(row=crow, column=12, padx=PAD_OPE_X, pady=PAD_OPE_Y)
    crow += 1
    txtbox_a2.grid(   row=crow, column=0,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_c2.grid(   row=crow, column=4,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_ocd2.grid(    row=crow, column=5,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_d2.grid(   row=crow, column=6,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=7,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_e2.grid(   row=crow, column=8,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_g2.grid(   row=crow, column=12, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1
    make_label().grid(row=crow, column=0,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    make_label().grid(row=crow, column=4,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    make_label().grid(row=crow, column=8,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    make_label().grid(row=crow, column=12, padx=PAD_EQL_X, pady=PAD_EQL_Y)
    crow += 1
    txtbox_a3.grid(row=crow, column=0,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_c3.grid(row=crow, column=4,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_e3.grid(row=crow, column=8,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_g3.grid(row=crow, column=12, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1
    txtbox_a4.grid(   row=crow, column=0,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_oab4.grid(    row=crow, column=1,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_b4.grid(   row=crow, column=2,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=3,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_c4.grid(   row=crow, column=4,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_e4.grid(   row=crow, column=8,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_oef4.grid(    row=crow, column=9,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_f4.grid(   row=crow, column=10, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=11, padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_g4.grid(   row=crow, column=12, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1
    box_ob45.grid(row=crow, column=2,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    box_of45.grid(row=crow, column=10, padx=PAD_OPE_X, pady=PAD_OPE_Y)
    crow += 1
    txtbox_b5.grid(row=crow, column=2,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_f5.grid(row=crow, column=10, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1
    make_label().grid(row=crow, column=2,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    make_label().grid(row=crow, column=10, padx=PAD_EQL_X, pady=PAD_EQL_Y)
    crow += 1
    txtbox_a6.grid(   row=crow, column=0,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_oab6.grid(    row=crow, column=1,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_b6.grid(   row=crow, column=2,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=3,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_c6.grid(   row=crow, column=4,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_e6.grid(   row=crow, column=8,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_oef6.grid(    row=crow, column=9,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_f6.grid(   row=crow, column=10, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=11, padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_g6.grid(   row=crow, column=12, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1
    box_oa67.grid(row=crow, column=0,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    box_oc67.grid(row=crow, column=4,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    box_oe67.grid(row=crow, column=8,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    box_og67.grid(row=crow, column=12, padx=PAD_OPE_X, pady=PAD_OPE_Y)
    crow += 1
    txtbox_a7.grid(   row=crow, column=0,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_c7.grid(   row=crow, column=4,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_ocd7.grid(    row=crow, column=5,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_d7.grid(   row=crow, column=6,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=7,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_e7.grid(   row=crow, column=8,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_g7.grid(   row=crow, column=12, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1
    make_label().grid(row=crow, column=0,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    make_label().grid(row=crow, column=4,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    make_label().grid(row=crow, column=8,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    make_label().grid(row=crow, column=12, padx=PAD_EQL_X, pady=PAD_EQL_Y)
    crow += 1
    txtbox_a8.grid(row=crow, column=0,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_c8.grid(row=crow, column=4,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_e8.grid(row=crow, column=8,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_g8.grid(row=crow, column=12, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1
    txtbox_a9.grid(   row=crow, column=0,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_oab9.grid(    row=crow, column=1,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_b9.grid(   row=crow, column=2,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=3,  padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_c9.grid(   row=crow, column=4,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    txtbox_e9.grid(   row=crow, column=8,  padx=PAD_DGT_X, pady=PAD_DGT_Y)
    box_oef9.grid(    row=crow, column=9,  padx=PAD_OPE_X, pady=PAD_OPE_Y)
    txtbox_f9.grid(   row=crow, column=10, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    make_label().grid(row=crow, column=11, padx=PAD_EQL_X, pady=PAD_EQL_Y)
    txtbox_g9.grid(   row=crow, column=12, padx=PAD_DGT_X, pady=PAD_DGT_Y)
    crow += 1

    def get_values() -> None:
        """Store input values."""
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
    btn_OK.grid(row=crow, column=0, columnspan=13)

    # Display window
    root.mainloop()

    return (digits, ops)
