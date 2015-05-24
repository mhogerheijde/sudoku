# vim: set fileencoding=UTF-8
from collections import OrderedDict
from copy import copy
import logging

logger = logging.getLogger(__name__)

SUDOKU_POSSIBILITIES = range(1, 10)
SUDOKU_RANGE = range(0, 9)

class Cell(object):
    """
    Represents a single cell in a Sudoku-grid. It keeps track of all
    available values it can hold.
    """

    def __init__(self, coordinates=None):
        self.possibilities = copy(SUDOKU_POSSIBILITIES)
        self.coordinates = coordinates
        self.value = None
        self.checked = False

    def __str__(self):
        value = "?" if self.value is None else str(self.value)
        vertical, horizontal = self.coordinates
        return "Cell< ({},{}) : {} | {}>".format(vertical, horizontal, value, self.possibilities)

    def eliminate(self, value):
        try:
            self.possibilities.remove(value)
        except:
            # Don't care if not in list.
            pass

        if len(self.possibilities) == 0:
            raise Exception("No options left after elimiation")
        elif len(self.possibilities) == 1:
            self.set(self.possibilities[0])

    def set(self, value):
        if not self.value is None and self.value != int(value):
            raise Exception("This cell already has a value {}, which differs from {}".format(self.value, value))

        if int(value) not in self.possibilities:
            raise Exception("This cell can only be set to {}".format(self.possibilities))

        self.possibilities = [ int(value) ]
        self.value = int(value)


class Group(object):
    """
    A Group represents a logical collection of Cells, for which the Sudoku
    rule "All possible values must occur exactly once." holds. In other words:
    when one of the cells in a Group has a specific value, others cells in
    the same group can't have that value any more.
    """

    def __init__(self, cells=None):

        self.solved = False

        if cells == None:
            self.cells =  []
        else:
            self.cells = cells

    def __str__(self):
        cells = ""
        for cell in self.cells:
            cells += "\t{}\n".format(cell)
        result = "Group<size:{} cells:\n{}>".format(len(self.cells), cells)

        return result

    def addCell(self, cell):
        if cell in self.cells:
            raise Exception("Cell {} already in this Group", cell)
        self.cells.append(cell)

    def setCell(self, cell, value):
        if cell not in self.cells:
            raise Exception("Cell not managed by this group")

        cell.set(value)
        for c in self.cells:

            if not c is cell:
                # Yes, Identity check, I want the same object.
                c.eliminate(value)



class Grid(object):
    """
    Grid represents the entire Sudoku-grid. Keeps track of all Cells and the
    Groups they are a member of. Traditionally, each Cell is part of three
    Groups: The "horziontal", the "vertical" and the "block" group.
    """



    def __init__(self):
        self.cells = OrderedDict()
        self.rows = {}
        self.columns = {}
        self.blocks = {}

        for vertical in SUDOKU_RANGE:
            for horizontal in SUDOKU_RANGE:
                # New cell at spot (vertical, horizontal)
                cell = Cell((vertical, horizontal))

                # Add cell to groups and lookup-lists
                self.cells[(vertical, horizontal)] = cell

                coordinates = (vertical, horizontal)

                self._getRow(coordinates).addCell(cell)
                self._getColumn(coordinates).addCell(cell)
                self._getBlock(coordinates).addCell(cell)



    def __str__(self):
        cells = ""
        for vertical, horizontal in self.cells:
            cell = self.cells[(vertical, horizontal)]
            cells += "\t{}\n".format(str(cell))

        return "Grid<Size: {}, Cells: \n{}\n>".format(len(self.cells), cells)

    def setCell(self, cell, value):
        self._getRow(cell.coordinates).setCell(cell, value)
        self._getColumn(cell.coordinates).setCell(cell, value)
        self._getBlock(cell.coordinates).setCell(cell, value)

    def _getBlock(self, coordinates):
        # Calculate block number. Groups of nine in a square,
        # starting with block 0 at the top left.
        # 012
        # 345
        # 678
        # Where each number is a block of 3 by 3 cells.
        vertical, horizontal = coordinates
        blockNo = 3 * int(vertical / 3) + (horizontal / 3)

        if not blockNo in self.blocks:
            self.blocks[blockNo] = Group()

        return self.blocks[blockNo]

    def _getRow(self, coordinates):
        vertical, horizontal = coordinates
        if not vertical in self.rows:
            self.rows[vertical] = Group()

        return self.rows[vertical]

    def _getColumn(self, coordinates):
        vertical, horizontal = coordinates
        if not horizontal in self.columns:
            self.columns[horizontal] = Group()

        return self.columns[horizontal]

    def readState(self, state):
        lines = state.strip().split("\n")
        if len(lines) != len (SUDOKU_RANGE):
            raise Exception("Invalid sudoku format: must contain {} lines; {} lines given", len(SUDOKU_RANGE),
                len(lines))

        for lineno, line in enumerate(lines):
            cells = line.strip().split()
            if len(cells) != len (SUDOKU_RANGE):
                raise Exception("Invalid sudoku format: {} values given, {} expected in line {} '{}'",
                    len(cells), len(SUDOKU_RANGE), lineno, line)

            for cellno, cell in enumerate(cells):
                if not str(cell).isdigit():
                    continue

                if int(cell) not in SUDOKU_POSSIBILITIES:
                    raise Exception("Invalid cell value '{}': line {}, position {}", cell, lineno, cellno)

                self.cells[(lineno, cellno)].set(cell)




