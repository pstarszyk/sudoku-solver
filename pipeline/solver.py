import cvxpy as cp
import numpy as np

from config.core import config
from typing import List


def solve_board(*, board: List[List[int]]) -> List[List[int]]:
    board = np.array(board)
    X = dict()
    for k in range(9):
        X['X%s' % (k + 1)] = cp.Variable((9, 9), boolean=True)

    constraints = list()
    exp = 0
    for k in range(9):
        exp += X['X%s' % (k + 1)]
    constraints.append(exp >= 1)
    constraints.append(exp <= 1)

    for k in range(9):
        lower_bound = np.zeros((9, 9))
        lower_bound[np.where(board == k + 1)] = 1
        constraints.append(lower_bound <= X['X%s' % (k + 1)])
        for i in range(9):
            constraints.append(cp.sum(X['X%s' % (k + 1)][i, :]) >= 1)
            constraints.append(cp.sum(X['X%s' % (k + 1)][i, :]) <= 1)
        for j in range(9):
            constraints.append(cp.sum(X['X%s' % (k + 1)][:, j]) >= 1)
            constraints.append(cp.sum(X['X%s' % (k + 1)][:, j]) <= 1)
        for i in range(3):
            for j in range(3):
                constraints.append(cp.sum(X['X%s' % (k + 1)][i * 3:(i + 1) * 3, j * 3:(j + 1) * 3]) >= 1)
                constraints.append(cp.sum(X['X%s' % (k + 1)][i * 3:(i + 1) * 3, j * 3:(j + 1) * 3]) <= 1)

    try:
        objective = cp.Minimize(1)
        prob = cp.Problem(objective, constraints)
        prob.solve(solver=config.pipeline_config.solver_mappings['solver'])
        sol = np.zeros((9, 9), dtype=int)
        for k in range(9):
            sol += np.rint(np.multiply(X['X%s' % (k + 1)].value, k + 1)).astype(int)
        sol = sol.tolist()

    except Exception as e:
        print(e)
        sol = board.tolist()

    return sol