import numpy as np
from ortools.sat.python import cp_model
from typing import List


class BoardSolver:
    def __init__(
            self,
            board: List[List[int]]
    ):
        self._board = board
        self._model = cp_model.CpModel()
        self._solver = cp_model.CpSolver()
        self._variables = None
        self._solution = None

    @property
    def solution(self):
        if not self._solution:
            self._solve_board()
        return self._solution

    def _solve_board(self):
        self._set_variables()
        self._set_constraints()
        self._solve()

    def _set_variables(self):
        self._variables = np.array([[[None for _ in range(9)] for _ in range(9)] for _ in range(9)])

        for row in range(9):
            for col in range(9):
                for num in range(9):
                    if num + 1 == self._board[row][col]:
                        self._variables[row, col, num] = self._model.NewIntVar(1, 1, 'x_%s%s%s' % (row + 1, col + 1, num + 1))
                    elif num + 1 != self._board[row][col] and self._board[row][col] != 0:
                        self._variables[row, col, num] = self._model.NewIntVar(0, 0, 'x_%s%s%s' % (row + 1, col + 1, num + 1))
                    else:
                        self._variables[row, col, num] = self._model.NewIntVar(0, 1, 'x_%s%s%s' % (row + 1, col + 1, num + 1))

    def _set_constraints(self):
        for i in range(9):
            for row in range(9):
                self._model.Add(sum(self._variables[row, :, i]) == 1)
            for col in range(9):
                self._model.Add(sum(self._variables[:, col, i]) == 1)
            for col in range(9):
                self._model.Add(sum(self._variables[i, col, :]) == 1)
            for h in range(3):
                for v in range(3):
                    self._model.Add(sum(sum(self._variables[h * 3:(h + 1) * 3, v * 3:(v + 1) * 3, i])) == 1)

    def _solve(self):
        self._solution = [[None for _ in range(9)] for _ in range(9)]

        try:
            self._solver.Solve(self._model)

            for row in range(9):
                for col in range(9):
                    for num in range(9):
                        if self._solver.Value(self._variables[row, col, num]) == 1:
                            self._solution[row][col] = num + 1
                            break
        except:
            self._solution = self._board