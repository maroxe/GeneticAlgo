import ga
import numpy as np
from scipy.stats import bernoulli
import random
import draw
n = 20

def fitness(t, debug=False): 
    x = np.zeros((n , n))
    for i, j in enumerate(t):
        x[i][j] = 1
 
    s = 0

    # diags
    for k in range(-n + 1, n):
        # diag (i, i+k) (n-i-1, i+k)
        q_diag = sum([ x[i][i + k] for i in range(max(0, -k), min(n, n - k))])
        s += max(0, q_diag - 1) 
        q_diag = sum([ x[n - i - 1][i + k] for i in range(max(0, -k), min(n, n - k))])
        s += max(0, q_diag - 1)
    return -s 

def mutation(l, x):
    bits_to_change = random.sample(range(len(x)), l)
    rand_permutation = list(bits_to_change)
    random.shuffle(rand_permutation)

    x_mut = list(x)
    
    for i in range(l):
        x_mut[bits_to_change[i]] = x[rand_permutation[i]]
    return x_mut

def crossover(c, x, xx):
    parent = [x, xx]
    parent_choice = bernoulli.rvs(c, size=len(x))
    y = []
    for p in parent_choice:
        for b in parent[p]:
            if not (b in y):
                y.append(b)
                break

    return y

ea_algo = ga.EA(fitness=fitness, crossover=crossover, mutation=mutation)
x_init = range(n)

best_x = ea_algo.run(n, x_init, offspring_size=10, n_generations=1000)
print 'fitness = ', fitness(best_x, debug=False)

draw.draw_chess_table(best_x)

