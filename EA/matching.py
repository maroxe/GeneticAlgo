import random
import ga
import draw
import numpy as np

n = 10
edges = np.zeros((n, n))
# edges symetric
vertices = range(n)
for i in range(n):
    friends = random.sample(vertices, 3)
    for f in friends:
        edges[i][f] = True
        edges[f][i] = True

draw.draw_graph(edges)

def deg(sub_graph, v):
    return sum([edges[v][w] for w in range(n) if v != w and sub_graph[w]])

def fitness(M): 
    return sum(M) - len(M) * sum([max(0, deg(M, v) - 1) for v in range(n) if M[v] ])

ea_algo = ga.EA(fitness=fitness)

max_graph = ea_algo.run(n=n, offspring_size=3, n_generations=1000)
draw.draw_graph(edges, 'max_graph.png', max_graph)



"""
N = 100
for n in range(10, 31, 10):
    for lamb in range(2, 7):
        print 'n = %d lambda = %d' % (n, lamb), \
            timeit.timeit('ga.run(n=%d, offspring_size=%d, N=10)' % (n, lamb), 'import ga', number=N)
    print '-' * 10
#print timeit.timeit('ga.run(n=50, lamb=5, N=10, adapt_lamb=True)', 'import ga', number=N)

"""
