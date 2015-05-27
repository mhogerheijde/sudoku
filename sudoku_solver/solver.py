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
        self.parentAssumption = None
        self.assumptions = {}
        self.invalidAssumptions = []

    def isSolved(self):
        return len(self.grid.unsolved) == 0

    def step(self):
        logger.debug(" **** STEP {} ****  ".format(self.currentStep))
        if self.isSolved():
            raise Exception("Sudoku is sovled already")

        self._make_history()


        try:
            self._eliminate()
            self._infer()
            # self._hidden_twin()
            # self._naked_twin()

        except sudoku.ImpossibleEliminationException, e:
            if parentAssumption is None:
                # We have an Elimination exception, but we didn't make
                # any assumptions: Sudoku must be invalid.
                raise UnsolvableSudkouException(e)
            else:
                # We made an assumption, but now our grid is unsolvable,
                # thus our assumption must be invalid.
                logger.debug("ImpossibleElimination after assumptions: %s", self.assumptions)
                self.invalidAssumptions.append(self.assumption)
                self.grid = self.history[self.assumption['step']]
                # TODO it would be quicker to make a new assumption immediately
                self.assumption = None

        current = display.serialise(self.grid)
        previous = display.serialise(self.history[self.currentStep])
        if current == previous:
            logger.debug("Previous state is equal to current state, make an assumption")
            # if self.assumption is None:
            #     assumption = self._create_assumption()
            #     logger.debug("Assumption: %s", assumption)
            #     self.assumption = assumption
            #     self.grid.cells[assumption['coordinates']].possibilities = [assumption['value']]
            # else:
            #     # TODO Make this work with a chain of assumptions
            #     logger.debug("We already made an assumption, but we didn't end up in a solved or erroneous state.")
            #     raise UnsolvableSudkouException("Sorry, unable to make multiple assumptions in a row")

            for group in self.grid.groups:
                twins = self._find_twins(group)
                logger.debug("Found %s twins for %s", len(twins), group)

                for pair in twins:
                    logger.debug("Found %s || \n      %20s\n      %20s", pair, twins[pair][0], twins[pair][1])

                logger.debug("\n\n\n")


            raise Exception("Not making assumptions")

        self.currentStep += 1



    ############################################################################
    # Solving strategies
    ############################################################################


    def _eliminate(self):
        """
        Simple bookkeeping strategy that follows directly from the rules of
        Sudoku: A number can only be present once in a column, row or group;
        thus if we know a cell to hold a certain value, all other cells in the
        same column, row and group can't hold that value any-more.
        """

        logger.debug(" **** ELIMINATION ****  ")

        # We're changing the content of the list unsolved during iteration
        # so make a copy of the list, we do want the cells, so a shallow copy.
        for cell in copy.copy(self.grid.unsolved):
            # Loop over all cells not yet solved. (This includes cells that
            # only have one possible value left; these are not "processed" yet
            # and therefore don't have the status "solved")
            logger.debug("Working on cell: {}".format(cell))
            if len(cell.possibilities) == 1:
                # There is only one possibility left. Solve this cell to that
                # value. "solving" will also cross out this value in other cells
                # that now can't hold that value any-more
                self.grid.solveCell(cell, cell.possibilities[0])

    def _infer(self):
        """
        Strategy that checks if a certain value can only be present in 1 cell
        for a certain group. Even though this cell might have some other possible
        values, since this is the only cell to have this certain value as a
        possibility it therefore must have that specific value.
        """

        logger.debug(" **** INFERRING ****  ")

        # Loop over all groups (rows, columns and blocks)
        for group in self.grid.groups:
            for value in sudoku.SUDOKU_RANGE:
                # Within a group, check if there is a cell that is the only
                # cell to have a certain value left as a possibility
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

    def _naked_twin(self):
        logger.debug(" **** NAKED-TWIN ****  ")
        for group in self.grid.groups:
            logger.debug("Working on group %s", group)
            self._find_twins(group)

    def _find_twins(self, group):

        possible_twins = {}
        for cell in group.cells:

            count = len(cell.possibilities)
            sorted_options = sorted(cell.possibilities)
            pairs = []
            if count < 2:
                # If we don't have at least a pair, this is not fruitful
                continue
            else:
                # use sorted list, to make sure created Tuples are the same
                # when 2 numbers are the same (e.g. (1,2) would have the same
                # meaning as (2,1), but they aren't the same for Python)
                pairs = [tuple(sorted_options[x:x+2]) for x in range(len(sorted_options)-1)]

            for pair in pairs:

                if pair in possible_twins:
                    # We are stepping through pairs in an ordered manner
                    continue

                possible_twins[pair] = [cell]

                for candidate_cell in group.cells:
                    if cell is candidate_cell:
                        continue # Not interested in comparing to itself

                    if all(x in candidate_cell.possibilities for x in pair):
                        # the current Tuple is contained within candidate_cell
                        logger.debug("Cell %s is a match for %s", candidate_cell, pair)
                        if candidate_cell not in possible_twins[pair]:
                            possible_twins[pair].append(candidate_cell)




        twins = {}
        for pair in possible_twins:
            if len(possible_twins[pair]) == 2:
                twins[pair] = possible_twins[pair]

        return twins




    def _hidden_twin(self):
        logger.debug(" **** HIDDEN-TWIN ****  ")
        pass

    ############################################################################
    # Helper methods
    ############################################################################


    def _make_history(self):
        self.history[self.currentStep] = copy.deepcopy(self.grid)

    def _create_assumption(self):

        logger.debug("Current invalid assumptions: %s", self.invalidAssumptions)

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


            foundInvalid = False
            if len(self.invalidAssumptions) > 0:
                for invalid in self.invalidAssumptions:
                    if invalid['coordinates'] == assumption['coordinates'] and invalid['value'] == assumption['value']:
                        # Current assumption is invalid
                        foundInvalid = True
                        unusedOption +=1
                        if unusedOption >= len(cell.possibilities):
                            unusedOption = 0
                            unsolvedCell += 1

                            if unsolvedCell >= len(self.grid.unsolved):
                                raise UnsolvableSudkouException("Exhausted all possibilities to assume")

            validAssumption = not foundInvalid


        return assumption


    def __str__(self):
        step = "Step {}".format(self.currentStep) if self.currentStep != 0 else "Start"
        result = " ** {} ({})".format(step, green("solved") if self.isSolved() else red("unsolved") )
        result += u"\n [{}]".format(sha256(display.serialise(self.grid)).hexdigest())
        return result + "\n" + display.full(self.grid)


class UnsolvableSudkouException(Exception):
    pass

