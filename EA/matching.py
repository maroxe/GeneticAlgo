import ga
import draw
import numpy as np
import pydot
from collections import Counter
from operator import itemgetter

def draw_graph(edges, vertices, M=None, image='graph.png'):
    if not M:
        M = [0] * len(edges)
        
    graph = pydot.Dot(graph_type='graph')
    
    for v in vertices: 
        graph.add_node(pydot.Node("Node %d" % v))
        
    for i, (e,f) in enumerate(edges):
        color = "red" if  M[i] else "black"
        edge = pydot.Edge("Node %d" % e, "Node %d" % f, color=color)
        graph.add_edge(edge)
           
    graph.write_png(image)
    
n = 10
vertices = range(n)
#edges = [ (i,j) if i < j else (j,i) for i,j in np.random.randint(n, size=(2*n, 2)) if i != j ]
edges = [(i, i+1) if i+1 < n else (n-1, 0) for i in range(n)]
edges = map(itemgetter(0), Counter(edges).items())
m = len(edges)



def deg(M):
    deg_m = np.zeros(m)
    for i, (e, f) in enumerate(edges):
        if M[i]:
            deg_m[e] += 1
            deg_m[f] += 1
    return sum([max(0, d-1) for d in deg_m])

def fitness(M): 
    return sum(M) - m * deg(M)

ea_algo = ga.EA(fitness=fitness)

max_graph = ea_algo.run(n=len(edges), offspring_size=10, n_generations=100, self_adapt=True)
print 'fitness = ', fitness(max_graph), ', score = ', sum(max_graph)
draw_graph(edges, vertices, M=max_graph, image='resources/graph.png')



