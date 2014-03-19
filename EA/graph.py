import numpy as np
import pydot 
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
    return edges

def draw_graph(edges, image='graph.png', sub_graph=None, path=None):
    if sub_graph == None:
        sub_graph = [1] * len(edges)
        
    graph = pydot.Dot(graph_type='graph')
    
    for i in range(len(edges)):
        for j in range(i):
            if edges[i][j]:
                edge = pydot.Edge("Node %d" % i, "Node %d" % j)
                graph.add_edge(edge)
            elif sub_graph[i]:
                graph.add_node(pydot.Node("Node %d" % i))
    if path:
        s0 = path[0]
        for i, s in enumerate(path[1:]):
            graph.add_edge(pydot.Edge("Node %d" % s0, "Node %d" % s, 
                                  label='%d' % (i+1), fontsize="30.0", color="blue"))
            s0 = s

    graph.write_png(image)