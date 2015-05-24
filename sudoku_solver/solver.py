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
        self.history = {}
        self.assumption = None
        self.invalidAssumptions = []

    def isSolved(self):
        return len(self.grid.unsolved) == 0

    def step(self):
        logger.debug(" **** STEP {} ****  ".format(self.currentStep))
        if self.isSolved():
            raise Exception("Sudoku is sovled already")

        self._make_history()


        try:
            logger.debug(" **** ELIMINATION ****  ")
            self._eliminate()
            logger.debug(" **** INFERRING ****  ")
            self._infer()
        except sudoku.ImpossibleEliminationException, e:
            if self.assumption is None:
                # We have an Elimination exception, but we didn't make
                # any assumptions: Sudoku must be invalid.
                raise UnsolvableSudkouException(e)
            else:
                # We made an assumption, but now our grid is unsolvable,
                # thus our assumption must be invalid.
                logger.debug("ImpossibleElimination after assumption: %s", self.assumption)
                self.invalidAssumptions.append(self.assumption)
                self.grid = self.history[self.assumption['step']]
                self.assumption = None

        current = display.serialise(self.grid)
        previous = display.serialise(self.history[self.currentStep])
        if current == previous:
            logger.debug("Previous state is equal to current state, make an assumption")
            assumption = self._create_assumption()
            logger.debug("Assumption: %s", assumption)
            self.assumption = assumption
            self.grid.cells[assumption['coordinates']].possibilities = [assumption['value']]

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

    def _cells_with_possible_value(self, group, value):
        result = []
        for cell in group.cells:
            if value in cell.possibilities and cell.value is None:
                result.append(cell)
        return result


    def _make_history(self):
        self.history[self.currentStep] = copy.deepcopy(self.grid)

    def _create_assumption(self):

        validAssumption = False
        unsolvedCell = 0
        unusedOption = 0
        while not validAssumption:


            cell = self.grid.unsolved[unsolvedCell]
            assumption = {
                'value': cell.possibilities[unusedOption],
                'coordinates': cell.coordinates,
                'step': self.currentStep
            }
            logger.debug("Generated assumption: %s", assumption)


            if len(self.invalidAssumptions) > 0:
                for invalid in self.invalidAssumptions:
                    if invalid['coordinates'] == assumption['coordinates'] and invalid['value'] == assumption['value']:
                        # Current assumption is invalid
                        unusedOption +=1
                        if unusedOption >= len(cell.possibilities):
                            unusedOption = 0
                            unsolvedCell += 1

                            if unsolvedCell >= len(self.grid.unsolved):
                                raise UnsolvableSudkouException("Exhausted all possibilities to assume")
                    else:
                        validAssumption = True
            else:
                validAssumption = True


        return assumption


    def __str__(self):
        step = "Step {}".format(self.currentStep) if self.currentStep != 0 else "Start"
        result = " ** {} ({})".format(step, green("solved") if self.isSolved() else red("unsolved") )
        result += u"\n [{}]".format(sha256(display.serialise(self.grid)).hexdigest())
        return result + "\n" + display.full(self.grid)


class UnsolvableSudkouException(Exception):
    pass

