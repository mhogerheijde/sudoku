# vim: set fileencoding=UTF-8
from sudoku import Grid, Cell, SUDOKU_RANGE, SUDOKU_POSSIBILITIES


def serialise(element):
    if isinstance(element, Grid):
        return _serialise_grid(element)
    elif isinstance(element, Cell):
        return _serialise_cell(element)

def simple(element):
    if isinstance(element, Grid):
        return _simple_grid(element)
    elif isinstance(element, Cell):
        return _default_cell(element)

def default(element):
    if isinstance(element, Grid):
        return _default_grid(element)
    elif isinstance(element, Cell):
        return _default_cell(element)

def full(element):
    if isinstance(element, Grid):
        return _full_grid(element)
    elif isinstance(element, Cell):
        return _full_cell(element)

def _default_grid(grid):
    result = u"┏━┯━┯━┳━┯━┯━┳━┯━┯━┓\n"

    for vertical, row in enumerate(grid.cells):
        currentRow = ""
        for horizontal, cell in enumerate(row):

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
    result = u" ┏━━━━━━━┯━━━━━━━┯━━━━━━━┳━━━━━━━┯━━━━━━━┯━━━━━━━┳━━━━━━━┯━━━━━━━┯━━━━━━━┓\n"
    for vertical, row in enumerate(grid.cells):
        currentRowString = ["", "", ""]
        for horizontal, cell in enumerate(row):

            cellString = full(cell)

            delim = u" │ " if horizontal % 3 != 0 else u" ┃ "

            currentRowString[0] += delim + cellString[0]
            currentRowString[1] += delim + cellString[1]
            currentRowString[2] += delim + cellString[2]

        result += currentRowString[0] + u" ┃\n" + currentRowString[1] + u" ┃\n" + currentRowString[2] + u" ┃\n"

        if vertical == 8:
            result += u" ┗━━━━━━━┷━━━━━━━┷━━━━━━━┻━━━━━━━┷━━━━━━━┷━━━━━━━┻━━━━━━━┷━━━━━━━┷━━━━━━━┛\n"
        elif vertical % 3 == 2:
            result += u" ┣━━━━━━━┿━━━━━━━┿━━━━━━━╋━━━━━━━┿━━━━━━━┿━━━━━━━╋━━━━━━━┿━━━━━━━┿━━━━━━━┫\n"
        else:
            result += u" ┠───────┼───────┼───────╂───────┼───────┼───────╂───────┼───────┼───────┨\n"

    return result

def _simple_grid(grid):
    result = "+---+---+---+\n"
    for vertical in SUDOKU_RANGE:
        result += "|"
        row = grid.cells[vertical]
        for horizontal in SUDOKU_RANGE:
            cell = row[horizontal]
            result += simple(cell)
            if horizontal % 3 == 2:
                result += "|"
        result += "\n"
        if vertical % 3 == 2:
            result += "+---+---+---+\n"
    return result

def _serialise_grid(grid):
    result = ""
    for rows in grid.cells:
        for cell in rows:
            result += serialise(cell)
        result += "\n"
    return result

def _serialise_cell(cell):
    return "? " if cell.value is None else str(cell.value) + " "

def _default_cell(cell):
    return " " if cell.value is None else str(cell.value)

def _full_cell(cell):
    result = []
    current = ""
    for i, value in enumerate(SUDOKU_POSSIBILITIES):
        if value in cell.possibilities:
            current += str(value)
        else:
            current += " "

        if i % 3 == 2:
            result.append(current)
            current = ""
        else:
            current += " "

    return result
