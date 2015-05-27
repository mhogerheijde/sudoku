# vim: set fileencoding=UTF-8

from sudoku import Grid, Cell
from . import display
from solver import Solver

import argparse
import logging



original_solvable = """
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

solvable = """
. . . . . . . 4 .
. 4 . . . 6 9 . 8
. 3 . . 7 4 . 2 6
7 . . . . . 2 . .
. . . 5 . 1 . . .
. . 1 . . . . . 3
4 7 . 9 8 . . 6 .
6 . 8 2 . . . 9 .
. 2 . . . . . . .
"""

solvable2 = """
. 9 . . 7 3 . . 5
4 . 8 2 . . 3 . .
. . 5 . . . . . .
. . 7 3 . . 5 8 .
. . . . 1 . . . .
. 4 3 . . 7 6 . .
. . . . . . 2 . .
. . 6 . . 5 9 . 4
3 . . 1 4 . . 7 .
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

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(1, gettext('%s: error: %s\n') % (self.prog, message))

def solve():


    grid = Grid()
    grid.readState(solvable2)

    solver = Solver(grid)

    print unicode(solver)
    while solver.currentStep < 20 and not solver.isSolved():
        solver.step()
        print unicode(solver)




def parse_args(args=None):
    parser = ArgumentParser(
            description='Solve a sudoku.',
            formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
            help='show debugging output')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true',
            help='makes this command quiet, outputting only errors. This also mutes --debug.')

    return parser.parse_args(args)


def setup_logging(args):

    logging.basicConfig(format='%(message)s', level=logging.ERROR)

    loglevel = logging.INFO
    if args.quiet:
        loglevel = logging.ERROR
    elif args.debug:
        loglevel = logging.DEBUG

    logging.getLogger("sudoku_solver").setLevel(loglevel)

def main():
    # print u"Sudoku Solver™\n\n"
    args = parse_args()
    setup_logging(args)
    solve()


if __name__ == 'main':
    main()
