import copy
import display
import logging
from termcolor import colored

import sudoku

green = lambda x: colored(x, 'green')
red = lambda x: colored(x, 'red')

logger = logging.getLogger(__name__)

class Solver(object):

    def __init__(self, grid):
        self.currentStep = 0
        self.grid = grid
        self.history = [ ]


    def step(self):
        logger.debug(" **** STEP {} ****  ".format(self.currentStep))
        if self.isSolved():
            raise Exception("Sudoku is sovled already")

        self._make_history()

        self._eliminate()

        self.currentStep += 1

    def _eliminate(self):
        for vertical, horizontal in self.grid.cells:
            cell = self.grid.cells[(vertical, horizontal)]
            if not cell.checked and cell.value != None:
                self.grid.setCell(cell, cell.value)
                cell.cecked = True



    def isSolved(self):
        return len(self.grid.unsolved) == 0


    def _make_history(self):
        self.history.append(self.grid)
        grid = copy.deepcopy(self.grid)
        self.grid = grid


    def __str__(self):
        step = "Step {}".format(self.currentStep) if self.currentStep != 0 else "Start"
        result = " ** {} ({})".format(step, green("solved") if self.isSolved() else red("unsolved") )
        result += u"\n [{}]".format(sha256(display.serialise(self.grid)).hexdigest())
        return result + "\n" + display.full(self.grid)


