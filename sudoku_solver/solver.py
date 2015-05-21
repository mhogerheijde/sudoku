import copy
import display


class Solver(object):

    def __init__(self, grid):
        self.currentStep = 0
        self.grid = grid
        self.history = [ ]


    def step(self):
        self._make_history()

        self._eliminate()

        self.currentStep += 1

    def _eliminate(self):
        for vertical, horizontal in self.grid.cells:
            cell = self.grid.cells[(vertical, horizontal)]
            if cell.value != None:
                self.grid.setCell(cell, cell.value)



    def _make_history(self):
        self.history.append(self.grid)
        grid = copy.deepcopy(self.grid)
        self.grid = grid


    def __str__(self):
        return display.full(self.grid)
