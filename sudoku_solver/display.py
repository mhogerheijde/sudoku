# vim: set fileencoding=UTF-8
import sudoku


def serialise(element):
    if isinstance(element, sudoku.Grid):
        return _serialise_grid(element)
    elif isinstance(element, Cell):
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
    result = u" ┏━━━━━━━┯━━━━━━━┯━━━━━━━┳━━━━━━━┯━━━━━━━┯━━━━━━━┳━━━━━━━┯━━━━━━━┯━━━━━━━┓\n"

    for vertical in sudoku.SUDOKU_RANGE:
        currentRowString = ["", "", ""]
        for horizontal in sudoku.SUDOKU_RANGE:
            cell = grid.cells[(vertical, horizontal)]


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
    result = ""
    for coordinates in grid.cells:
        vertical, horizontal = coordinates
        result += serialise(grid.cells[coordinates])
        if (horizontal % 9 == 8):
            result += "\n"
    return result

def _serialise_cell(cell):
    return "? " if cell.value is None else str(cell.value) + " "

def _default_cell(cell):
    return " " if cell.value is None else str(cell.value)

def _full_cell(cell):
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

    return result
