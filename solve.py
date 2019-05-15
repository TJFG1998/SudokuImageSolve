import numpy as np
import sys
from copy import deepcopy
import resize

# len
N = 9

# MATRIZ DO JOGO
field = resize.cellCatch()

#da print da matrix
def print_field(field):
    m = np.asmatrix(field)
    m.shape = (9,9)
    print(m)

#lea matriz do jogo
def read(field):
    state = deepcopy(field)
    for i in range(N):# loopa a matriz
        for j in range(N):
            if state[i][j] == 0:
                state[i][j] = set(range(1,10))#enche com os numeros de 0-10
    return state


state = read(field)

# verifica se esta completo
def done(state):
    for row in state:
        for cell in row:
            if isinstance(cell, set):
                return False
    return True

# atividade em concreto
def propagate_step(state):
    new_units = False
    for i in range(N):
        row = state[i]
        values = set([x for x in row if not isinstance(x, set)])
        for j in range(N):
            if isinstance(state[i][j], set):
                state[i][j] -= values
                if len(state[i][j]) == 1:
                    val = state[i][j].pop()
                    state[i][j] = val
                    values.add(val)
                    new_units = True
                elif len(state[i][j]) == 0:
                    return False, None

    for j in range(N):
        column = [state[x][j] for x in range(N)]
        values = set([x for x in column if not isinstance(x, set)])
        for i in range(N):
            if isinstance(state[i][j], set):
                state[i][j] -= values
                if len(state[i][j]) == 1:
                    val = state[i][j].pop()
                    state[i][j] = val
                    values.add(val)
                    new_units = True
                elif len(state[i][j]) == 0:
                    return False, None

    for x in range(3):
        for y in range(3):
            values = set()
            for i in range(3 * x, 3 * x + 3):
                for j in range(3 * y, 3 * y + 3):
                    cell = state[i][j]
                    if not isinstance(cell, set):
                        values.add(cell)
            for i in range(3 * x, 3 * x + 3):
                for j in range(3 * y, 3 * y + 3):
                    if isinstance(state[i][j], set):
                        state[i][j] -= values
                        if len(state[i][j]) == 1:
                            val = state[i][j].pop()
                            state[i][j] = val
                            values.add(val)
                            new_units = True
                        elif len(state[i][j]) == 0:
                            return False, None
    return True, new_units

#loop de resolução
def propagate(state):
    while True:
        solvable, new_unit = propagate_step(state)
        if not solvable:
            return False
        if not new_unit:
            return True


def solve(state):
    solvable = propagate(state)
    if not solvable:
        return None
    if done(state):
        return state
    for i in range(N):
        for j in range(N):
            cell = state[i][j]
            if isinstance(cell, set):
                for value in cell:
                    new_state = deepcopy(state)
                    new_state[i][j] = value
                    solved = solve(new_state)
                    if solved is not None:
                        return solved
                return None

print_field(solve(state))