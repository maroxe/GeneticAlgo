import random
import draw
import ga
from resources import graph_examples
from copy import deepcopy

n = 5
vertices = range(n)
edges = graph_examples.graph2
nb_edges = sum ([edges[i][j] for i in range(n) for j in range(n) if i != j]) / 2
# edges = np.zeros((n, n))
# 
# edges symetric
# for i in range(n):
#     friends = random.sample(vertices, 3)
#     for f in friends:
#         edges[i][f] = True
#         edges[f][i] = True

#draw.draw_graph(edges)

x_init = [ [] for _ in vertices]

def find_match_and_remove(Mv, e):
    f = None
    k = len(Mv)-1
    while k >= 0 and f is None:
        i, j = Mv[k]
        if i == e:
            f = j
        if j == e:
            f = i
        k -= 1
    if f != None:
        Mv.pop(k+1)
    return f
        
def mutation(l, x, bit_range):
    x_mut = list(x)
    for _ in range(l):  
        v = random.randint(0, n-1)
        if deg(v) == 2:
            i, j = [w for w in vertices if edges[v][w] and v != w]
            x_mut[v] = [(i,j)]
        else:
            e = random.choice([i for i in vertices if i != v and edges[v][i]])
            f = find_match_and_remove(x_mut[v], e)
            
            ee = random.choice([i for i in vertices if (not i in[ v, e, f]) and edges[v][i]])
            ff = find_match_and_remove(x_mut[v], ee)
            
            x_mut[v].append( (e, ee) )
            if f and ff:
                x_mut[v].append( (f, ff) )
    return x_mut

def deg(v):
    return sum([edges[v][i] for i in vertices if i != v])

def fitness(x):
    path = reconstruct_path(x)
    cycles_penality = len(path) - nb_edges  
    return - sum( [deg(v)/2 - len(x[v]) for v in vertices] ) + cycles_penality

def reconstruct_path(xx):
    x = deepcopy(xx)
    v = 0
    try:
        (i,j) = x[v][0]
    except IndexError:
        return []
    path = [i, v]
    
    while j != None:
        j = find_match_and_remove(x[v], i)
        path.append(j)
        i, v = v, j
    return path
    
ea_algo = ga.EA(fitness=fitness, mutation=mutation)
best_x = ea_algo.run(n=n, x_init=x_init, offspring_size=4, n_generations=100)

print 'fitness = ', fitness(best_x)
print best_x
print reconstruct_path(best_x)

draw.draw_graph(edges, 'graph.png')




