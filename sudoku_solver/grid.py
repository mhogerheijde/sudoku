import sys


SUDOKU_POSSIBILITIES = range(1, 10)
SUDOKU_RANGE = range(0, 9)

class Cell(object):

    def __init__(self):
        self.possibilities = SUDOKU_POSSIBILITIES
        self.value = None

    def __str__(self):
        return "?" if self.value is None else self.value


    def set(self, value):
        if not self.value is None:
            raise Exception("This cell already has a value")

        if int(value) not in self.possibilities:
            raise Exception("This cell can only be set to {}".format(self.possibilities))

        self.possibilities = [ value ]
        self.value = int(value)


class Group(object):

    def __init__(self, cells):
        self.cells = cells


class SudokuGrid(object):

    def __init__(self):
        self.cells = []
        for vertical in SUDOKU_RANGE:
            new_row = []
            for horizontal in SUDOKU_RANGE:
                new_row.append(Cell())

            self.cells.append(new_row)

    def __str__(self):

        result = "+---+---+---+\n"
        for vertical in SUDOKU_RANGE:
            result += "|"
            row = self.cells[vertical]
            for horizontal in SUDOKU_RANGE:
                cell = row[horizontal]
                result += str(cell)
                if horizontal % 3 == 2:
                    result += "|"
            result += "\n"
            if vertical % 3 == 2:
                result += "+---+---+---+\n"
        return result


