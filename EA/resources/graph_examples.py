import numpy as np
import random

graph1 = [[False, True, False, True, True, False, False, True], [True, False, True, False, True, True, False, False], [False, True, False, True, False, True, True, False], [True, False, True, False, False, False, True, True], [True, True, False, False, False, False, False, False], [False, True, True, False, False, False, False, False], [False, False, True, True, False, False, False, False], [True, False, False, True, False, False, False, False]]
graph2 = [
            [True, True, True, True, True],
            [True, True, True, True, False],
            [True, True, True, True, False],
            [True, True, True, True, True],
            [True, False, False, True, True],
           ]
def graph3(n):
    edges = np.zeros((n, n))
    vertices = range(n)
    for i in range(n):
        friends = random.sample(vertices, 3)
        for f in friends:
            edges[i][f] = True
            edges[f][i] = True