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
            raise ImpossibleEliminationException("No options left after elimiation")

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

    def __init__(self, cells=None, row=None, column=None, block=None):
        self.row = row
        self.column = column
        self.block = block

        if (row is not None and (column is not None or block is not None)) \
            or (column is not None and (row is not None or block is not None)) \
            or (block is not None and (row is not None or column is not None)):
            raise Exception("Illegal state: cannot have a group in multiple orientations")

        if cells == None:
            self.cells =  []
        else:
            self.cells = cells

    def __str__(self):
        cells = ""
        for cell in self.cells:
            cells += "\t{}\n".format(cell)

        location = "??"
        if this.row is not None:
            location = "row: {}".format(this.row)
        elif this.column is not None:
            location = "column: {}".format(this.column)
        elif this.block is not None:
            location = "block: {}".format(this.block)

        result = "Group<{}; size: {}; cells:\n{}>".format(location, len(self.cells), cells)

        return result

    def addCell(self, cell):
        if cell in self.cells:
            raise Exception("Cell {} already in this Group", cell)
        self.cells.append(cell)

    def solveCell(self, cell):
        if cell not in self.cells:
            raise Exception("Cell not managed by this group")

        for c in self.cells:

            if not c is cell:
                # Yes, Identity check, I want the same object.
                c.eliminate(cell.value)



class Grid(object):
    """
    Grid represents the entire Sudoku-grid. Keeps track of all Cells and the
    Groups they are a member of. Traditionally, each Cell is part of three
    Groups: The "horziontal", the "vertical" and the "block" group.
    """



    def __init__(self):
        # All the cells in the grid
        self.cells = OrderedDict()

        # Sub-orientation of the grid
        self.rows = {}     # Index of all the rows (by row-number)
        self.columns = {}  # Index of all the columns (by column-number)
        self.blocks = {}   # Index of all the blocks (by block-number)
        # All the groups in one list for easy access.
        self.groups = []

        # Bookkeeping of unsolved cells.
        self.unsolved = []

        for vertical in SUDOKU_RANGE:
            for horizontal in SUDOKU_RANGE:
                # New cell at spot (vertical, horizontal)
                coordinates = (vertical, horizontal)

                # Create new cell
                cell = Cell(coordinates)

                # Add cell to groups and lookup-lists
                self.cells[coordinates] = cell

                # Add cells to the appropriate groups
                self._getRow(coordinates).addCell(cell)
                self._getColumn(coordinates).addCell(cell)
                self._getBlock(coordinates).addCell(cell)
                # All cells are in unsolved state initially
                self.unsolved.append(cell)




    def __str__(self):
        cells = ""
        for vertical, horizontal in self.cells:
            cell = self.cells[(vertical, horizontal)]
            cells += "\t{}\n".format(str(cell))

        return "Grid<Size: {}, Cells: \n{}\n>".format(len(self.cells), cells)

    def solveCell(self, cell, value):
        logger.debug("  - Solving cell {} to {}".format(cell, value))
        # Set cell to actual value
        cell.set(value)

        # Keep all groups up-to-date
        self._getRow(cell.coordinates).solveCell(cell)
        self._getColumn(cell.coordinates).solveCell(cell)
        self._getBlock(cell.coordinates).solveCell(cell)

        # Do bookkeeping of unsolved cells
        self.unsolved.remove(cell)


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
            new_group = Group(block=blockNo)
            self.blocks[blockNo] = new_group
            self.groups.append(new_group)

        return self.blocks[blockNo]

    def _getRow(self, coordinates):
        vertical, horizontal = coordinates
        if not vertical in self.rows:
            new_group = Group(row=vertical)
            self.rows[vertical] = new_group
            self.groups.append(new_group)

        return self.rows[vertical]

    def _getColumn(self, coordinates):
        vertical, horizontal = coordinates
        if not horizontal in self.columns:
            new_group = Group(column=horizontal)
            self.columns[horizontal] = new_group
            self.groups.append(new_group)


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

            for cellno, cellValue in enumerate(cells):
                if not str(cellValue).isdigit():
                    continue

                if int(cellValue) not in SUDOKU_POSSIBILITIES:
                    raise Exception("Invalid cell value '{}': line {}, position {}", cellValue, lineno, cellno)

                self.cells[(lineno, cellno)].possibilities = [ int(cellValue) ]




class ImpossibleEliminationException(Exception):
    pass
