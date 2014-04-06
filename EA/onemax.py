import ga
import numpy as np
from matplotlib import pyplot as plt

i = 0

def fitness(x):
    global i
    i += 1
    return sum(x)

N = 10000

n = 20
ea_algo = ga.EA(fitness=fitness)
x_init = np.random.random_integers(0, 1, size=n) 
offspring_size = range(1, n, 1)
time = [0] * len(offspring_size)

for j in range(len(offspring_size)):
    for _ in range(N):
        i = 0
        x = ea_algo.run(n, x_init, offspring_size=offspring_size[j], n_generations=100, max_fitness=n)
    time[j] = i 
    print 'step'
    
plt.plot(offspring_size, time)
plt.show()