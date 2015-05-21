# vim: set fileencoding=UTF-8

from sudoku import Grid, Cell
from . import display


random_sudoku_1 = """
1 2 ? 4 5 6 7 8 9
2 3 4 5 6 7 8 9 1
3 4 5 6 7 8 9 1 2
9 9 9 9 9 9 9 9 9
5 6 7 8 9 1 2 3 4
6 7 8 9 1 2 3 4 5
7 8 ? 1 2 3 4 5 6
8 9 1 2 3 4 5 6 7
9 1 2 3 4 5 6 7 ?
"""

random_sudoku_2 = """
1 ? ? ? ? ? ? ? 9
? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ?
? ? ? ? ? ? ? ? ?
"""

def main():
	print u"Sudoku Solver™\n\n"

	grid = Grid()
	grid.readState(random_sudoku_2)


	# c = Cell((1, 2))
	# c.set(2)
	# print c

	print display.serialise(grid)
	print display.simple(grid)
	print display.default(grid)
	print display.full(grid)

	# print display.simple(grid)
	# print display.expanded(grid)

	# print grid.expandedString()




if __name__ == 'main':
	main()
