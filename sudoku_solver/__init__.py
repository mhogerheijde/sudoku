# vim: set fileencoding=UTF-8

SUDOKU_POSSIBILITIES = range(1, 10)
SUDOKU_RANGE = range(0, 9)

class Cell(object):
    """
    Represents a single cell in a Sudoku-grid. It keeps track of all
    available values it can hold.
    """

    def __init__(self, coordinates=None):
        self.possibilities = SUDOKU_POSSIBILITIES
        self.value = None
        # Sanity check
        v, h = coordinates
        self.coordinates = (v, h)

    def __str__(self):
        value = "?" if self.value is None else str(self.value)
        return "Cell< ({},{}) : {} >".format(self.coordinates[0], self.coordinates[1], value)

    def eliminate(self, value):
        if self.value == None:
            raise Exception("Can't eliminate values from fixed cell")
        try:
            self.possibilities.remove(value)
        except:
            # Don't care if not in list.
            pass

    def set(self, value):
        if not self.value is None:
            raise Exception("This cell already has a value")

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

    def addCell(self, cell):
        self.cells.append(cell)


class Grid(object):
    """
    Grid represents the entire Sudoku-grid. Keeps track of all Cells and the
    Groups they are a member of. Traditionally, each Cell is part of three
    Groups: The "horziontal", the "vertical" and the "block" group.
    """
    def __init__(self):
        self.cells = []
        self.rows = [Group() for x in SUDOKU_RANGE]
        self.columns = [Group() for x in SUDOKU_RANGE]
        self.blocks = [Group() for x in SUDOKU_RANGE]

        for vertical in SUDOKU_RANGE:
            new_row = []

            for horizontal in SUDOKU_RANGE:
                # New cell at spot (vertical, horizontal)
                new_cell = Cell((vertical, horizontal))

                # Add to current row
                new_row.append(new_cell)
                self.rows[vertical].addCell(new_cell)
                self.columns[horizontal].addCell(new_cell)

            self.cells.append(new_row)

    def __str__(self):
        result = ""
        for rows in self.cells:
            for cell in rows:
                result += str(cell) + " "
            result += "\n"
        return result


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
                if str(cell) == "?":
                    continue

                if int(cell) not in SUDOKU_POSSIBILITIES:
                    raise Exception("Invalid cell value '{}': line {}, position {}", cell, lineno, cellno)


                self.cells[lineno][cellno].set(cell)




