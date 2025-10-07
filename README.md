# Garam solver
This tool is designed to solve any <a href="https://www.garamgame.com/garam/garam_en_ligne/master/index.html">Garam grid ↗</a>.

Garam is a numerical crossword-style puzzle: fill in the 44 cells so that all 20 arithmetic statements are simultaneously correct.

<img src="img/grid_in_out_example.png" alt="Garam grid illustration" width="690"/> <!-- nice x10 -->


# How to use the tool?
1. Go to the root directory
2. Run ```pip install -r requirements.txt``` to install the required package (only one)
3. Run ```python garam_solver.py``` to open an empty grid
4. Fill in the grid with the initial digits and operators
5. Click the ```Solve``` button (you probably guessed it)
6. The solution is displayed in plain text on the terminal
7. ???
8. Profit

Notes:
- In step 3, you may instead enter ```python garam_solver.py --mini``` to play with a mini-Garam (20 % of a full grid).
- Step 4 is tedious. In the future, a URL _may_ be used to auto-fill the grid instead of manually entering 20~40 values.

# OK, but what was the point of this?
Well, I could not find any solver for this (addictive) game, so I made this.

(You may this?...

_I_ made this.)
