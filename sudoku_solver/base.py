# vim: set fileencoding=UTF-8

from sudoku import Grid, Cell
from . import display
from solver import Solver




solvable = """
9 2 . . 7 . 8 . 4
. . 3 . . 9 . . .
. . 8 6 4 1 9 . .
3 . 5 . . 7 . . .
7 . . 2 9 5 . . 1
. . . 3 . . 4 . 5
. . 2 9 3 6 7 . .
. . . 1 . . 2 . .
4 . 6 . 8 . . 5 3
"""

partially_solved = """
9 2 1 5 7 3 8 . 4
6 4 3 8 2 9 5 . .
5 7 8 6 4 1 9 . .
3 . 5 4 . 7 6 . .
7 . 4 2 9 5 . . 1
2 . . 3 . 8 4 . 5
. . 2 9 3 6 7 4 8
. . . 1 5 4 2 9 6
4 9 6 7 8 2 1 5 3
"""

def main():
    print u"Sudoku Solver™\n\n"

    grid = Grid()
    grid.readState(solvable)

    solver = Solver(grid)

    print " ** Unsolved"
    print unicode(solver)

    solver.step()
    print " ** Step 1"
    print unicode(solver)

    solver.step()
    print " ** Step 2"
    print unicode(solver)




if __name__ == 'main':
    main()
