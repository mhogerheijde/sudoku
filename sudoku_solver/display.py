# vim: set fileencoding=UTF-8
import sudoku

import json
from termcolor import colored

grey = lambda x: colored(x, 'grey')
red = lambda x: colored(x, 'red')
green = lambda x: colored(x, 'green')

def serialise(element):
    if isinstance(element, sudoku.Grid):
        return _serialise_grid(element)
    elif isinstance(element, sudoku.Cell):
        return _serialise_cell(element)
    else:
        raise Exception("{} element is Grid nor Cell".format(type(element)))

def simple(element):
    if isinstance(element, sudoku.Grid):
        return _simple_grid(element)
    elif isinstance(element, sudoku.Cell):
        return _default_cell(element)

def default(element):
    if isinstance(element, sudoku.Grid):
        return _default_grid(element)
    elif isinstance(element, sudoku.Cell):
        return _default_cell(element)

def full(element):
    if isinstance(element, sudoku.Grid):
        return _full_grid(element)
    elif isinstance(element, sudoku.Cell):
        return _full_cell(element)

def _default_grid(grid):
    result = u"┏━┯━┯━┳━┯━┯━┳━┯━┯━┓\n"

    for vertical in sudoku.SUDOKU_RANGE:
        currentRow = ""
        for horizontal in sudoku.SUDOKU_RANGE:
            cell = grid.cells[(vertical, horizontal)]

            delim = u"│" if horizontal % 3 != 0 else u"┃"

            currentRow += delim + default(cell)

        result += currentRow + u"┃\n"

        if vertical == 8:
            result += u"┗━┷━┷━┻━┷━┷━┻━┷━┷━┛\n"
        elif vertical % 3 == 2:
            result += u"┣━┿━┿━╋━┿━┿━╋━┿━┿━┫\n"
        else:
            result += u"┠─┼─┼─╂─┼─┼─╂─┼─┼─┨\n"

    return result



def _full_grid(grid):
    result = grey(u" ┏━━━━━━━┯━━━━━━━┯━━━━━━━┳━━━━━━━┯━━━━━━━┯━━━━━━━┳━━━━━━━┯━━━━━━━┯━━━━━━━┓\n")

    separator = grey(u" ┃\n")

    for vertical in sudoku.SUDOKU_RANGE:
        currentRowString = ["", "", ""]
        for horizontal in sudoku.SUDOKU_RANGE:
            cell = grid.cells[(vertical, horizontal)]


            cellString = full(cell)

            delim = grey(u" │ ") if horizontal % 3 != 0 else grey(u" ┃ ")

            currentRowString[0] += delim + cellString[0]
            currentRowString[1] += delim + cellString[1]
            currentRowString[2] += delim + cellString[2]

        result += currentRowString[0] + separator + currentRowString[1] + separator + currentRowString[2] + separator

        if vertical == 8:
            result += grey(u" ┗━━━━━━━┷━━━━━━━┷━━━━━━━┻━━━━━━━┷━━━━━━━┷━━━━━━━┻━━━━━━━┷━━━━━━━┷━━━━━━━┛\n")
        elif vertical % 3 == 2:
            result += grey(u" ┣━━━━━━━┿━━━━━━━┿━━━━━━━╋━━━━━━━┿━━━━━━━┿━━━━━━━╋━━━━━━━┿━━━━━━━┿━━━━━━━┫\n")
        else:
            result += grey(u" ┠───────┼───────┼───────╂───────┼───────┼───────╂───────┼───────┼───────┨\n")

    return result

def _simple_grid(grid):
    result = "+---+---+---+\n"
    for vertical in sudoku.SUDOKU_RANGE:
        result += "|"
        for horizontal in sudoku.SUDOKU_RANGE:
            cell = grid.cells[(vertical, horizontal)]

            result += simple(cell)
            if horizontal % 3 == 2:
                result += "|"
        result += "\n"
        if vertical % 3 == 2:
            result += "+---+---+---+\n"
    return result

def _serialise_grid(grid):
    grid_list = {}
    for coordinates, cell in grid.cells.iteritems():

        cell_dict = {
            'coordinates': cell.coordinates,
            'value': cell.value,
            'possibilities': cell.possibilities
        }
        grid_list["{}x{}".format(coordinates[0], coordinates[1])] = cell_dict


    return json.dumps(grid_list, sort_keys=True)

def _serialise_cell(cell):
    return "? " if cell.value is None else str(cell.value) + " "

def _default_cell(cell):
    return " " if cell.value is None else str(cell.value)

def _full_cell(cell):
    result = ["     ", red(" ??? "), "     "]


    if cell.value is None and len(cell.possibilities) > 1:
        result = []
        current = ""
        for i, value in enumerate(sudoku.SUDOKU_POSSIBILITIES):
            if value in cell.possibilities:
                current += str(value)
            else:
                current += " "

            if i % 3 == 2:
                result.append(current)
                current = ""
            else:
                current += " "
    elif cell.value is None and len(cell.possibilities) == 1:
        result = [
         "     ",
         red("  {}  ".format(cell.possibilities[0])),
         "     ",
        ]
    elif not cell.value is None :
        result = [
         "     ",
         green("  {}  ".format(cell.value)),
         "     ",
        ]

    return result
