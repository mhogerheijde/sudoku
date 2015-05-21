from . import Grid, Cell, SUDOKU_RANGE, SUDOKU_POSSIBILITIES


def compact(element):
    if isinstance(element, Grid):
        return _compact_grid(element)
    elif isinstance(element, Cell):
        return _compact_cell(element)

def simple(element):
    if isinstance(element, Grid):
        return _simple_grid(element)
    elif isinstance(element, Cell):
        return _simple_cell(element)

def expanded(element):
    if isinstance(element, Grid):
        return _expanded_grid(element)
    elif isinstance(element, Cell):
        return _expanded_cell(element)


def _expanded_grid(grid):
    result = " +-------+-------+-------++-------+-------+-------++-------+-------+-------+\n"
    for vertical, row in enumerate(grid.cells):
        currentRowString = ["", "", ""]
        for horizontal, cell in enumerate(row):

            cellString = expanded(cell)

            delim = " | " if horizontal % 3 != 0 or horizontal == 0 else " || "

            currentRowString[0] += delim + cellString[0]
            currentRowString[1] += delim + cellString[1]
            currentRowString[2] += delim + cellString[2]

        result += currentRowString[0] + " |\n" + currentRowString[1] + " |\n" + currentRowString[2] + " |\n"

        if vertical % 3 == 2 and vertical != 8:
            result += " +=======+=======+=======++=======+=======+=======++=======+=======+=======+\n"
        else:
            result += " +-------+-------+-------++-------+-------+-------++-------+-------+-------+\n"

    return result

def _expanded_cell(cell):
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

def _simple_cell(cell):
    return "?" if cell.value is None else str(cell.value)


def _compact_grid(grid):
    result = ""
    for rows in grid.cells:
        for cell in rows:
            result += compact(cell)
        result += "\n"
    return result

def _compact_cell(cell):
    return "?" if cell.value is None else str(cell.value)
