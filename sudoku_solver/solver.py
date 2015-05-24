import copy
import display
import logging
from termcolor import colored
from hashlib import sha256

import sudoku

green = lambda x: colored(x, 'green')
red = lambda x: colored(x, 'red')

logger = logging.getLogger(__name__)

class Solver(object):

    def __init__(self, grid):
        self.currentStep = 0
        self.grid = grid
        self.history = []


    def step(self):
        logger.debug(" **** STEP {} ****  ".format(self.currentStep))
        if self.isSolved():
            raise Exception("Sudoku is sovled already")

        self._make_history()

        logger.debug(" **** ELIMINATION ****  ")
        self._eliminate()
        logger.debug(" **** INFERRING ****  ")
        self._infer()



        current_sha = sha256(display.serialise(self.grid)).hexdigest()
        previous_sha = sha256(display.serialise(self.history[-1])).hexdigest()
        if current_sha == previous_sha:
            raise Exception("Previous state is exactly the same as current.")

        self.currentStep += 1

    def _eliminate(self):
        for cell in copy.copy(self.grid.unsolved):
            # We're changing the content of unsolved
            logger.debug("Working on cell: {}".format(cell))
            if len(cell.possibilities) == 1:
                self.grid.solveCell(cell, cell.possibilities[0])

    def _infer(self):
        for i in self.grid.rows:
            self._infer_group(self.grid.rows[i])
        for i in self.grid.columns:
            self._infer_group(self.grid.columns[i])
        for i in self.grid.blocks:
            self._infer_group(self.grid.blocks[i])



    def _infer_group(self, group):
        for value in sudoku.SUDOKU_RANGE:
            cells = self._cells_with_possible_value(group, value)
            if len(cells) == 1:
                cell = cells[0]
                logger.debug("{} is the only cell to contain {}".format(cell, value))
                cell.possibilities = [value]
                # self.grid.solveCell(cell, value)

    def _cells_with_possible_value(self, group, value):
        result = []
        for cell in group.cells:
            if value in cell.possibilities and cell.value is None:
                result.append(cell)
        return result


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


class UnsolveableSudkouException(Exception):
    pass

