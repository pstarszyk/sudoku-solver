import numpy as np
from ortools.sat.python import cp_model
from config.core import config
from typing import List


def solve_board(*, board: List[List[int]]) -> List[List[int]]:
    model = cp_model.CpModel()
    X = np.array([[[None for _ in range(9)] for _ in range(9)] for _ in range(9)])

    # Variables
    for row in range(9):
        for col in range(9):
            for num in range(9):
                if num + 1 == board[row][col]:
                    X[row, col, num] = model.NewIntVar(1, 1, 'x_%s%s%s' % (row + 1, col + 1, num + 1))
                elif num + 1 != board[row][col] and board[row][col] != 0:
                    X[row, col, num] = model.NewIntVar(0, 0, 'x_%s%s%s' % (row + 1, col + 1, num + 1))
                else:
                    X[row, col, num] = model.NewIntVar(0, 1, 'x_%s%s%s' % (row + 1, col + 1, num + 1))

    # Constraints
    for i in range(9):
        for row in range(9):
            model.Add(sum(X[row, :, i]) == 1)
        for col in range(9):
            model.Add(sum(X[:, col, i]) == 1)
        for col in range(9):
            model.Add(sum(X[i, col, :]) == 1)
        for h in range(3):
            for v in range(3):
                model.Add(sum(sum(X[h * 3:(h + 1) * 3, v * 3:(v + 1) * 3, i])) == 1)

    try:
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        sol = [[None for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                for num in range(9):
                    if solver.Value(X[row, col, num]) == 1:
                        sol[row][col] = num + 1
                        break

    except Exception as e:
        print(e)
        sol = board

    return sol