import numpy as np
import random
from scipy.stats import bernoulli

def default_mutation(l, x, bit_range):
    bits_to_change = random.sample(range(len(x)), l)
    x_mut = list(x)
    for b in bits_to_change:
        x_mut[b] = random.choice(bit_range)
    return x_mut

def default_crossover(c, x, xx):
    parent = [x, xx]
    parent_choice = bernoulli.rvs(c, size=len(x))
    return [ parent[p][i] for i, p in enumerate(parent_choice) ]


class EA:
    def __init__(self, fitness, bit_range=None, mutation=None, crossover=None):
        if not mutation:
            mutation = default_mutation
        if not crossover:
            crossover = default_crossover
        if not bit_range:
            bit_range = [0, 1]
            
        mutation = mutation
        bit_range = bit_range 
        crossover = crossover
        fitness = fitness
        

    def run(self, n=10, x_init=None, offspring_size=5, n_generations=10, p=None, c=None, self_adapt=False):
        # parameters
        if p is None:
            p = float(offspring_size) / n   # mutation probability
        if c is None:
            c = 1. / offspring_size         
        F = 1.5
        
        # initialization
        if not x_init:
            x_init = [ random.choice(bit_range) for _ in range(n)]
        x = x_init

        fit_x = fitness(x)
        # optimization
        for _ in range(n_generations):
        #while fit_x < 0:
            # mutation
            l = np.random.binomial(n, p)
            x_mut = [mutation(l, x, bit_range) for _ in range(offspring_size)]
            xx = x_mut[ np.argmax(map(fitness, x_mut)) ] # x'
            

            # crossover
            y_cross = [crossover(c, x, xx) for _ in range(offspring_size)]
            y = y_cross[ np.argmax( map(fitness, y_cross) ) ]
            
            # selection
            fit_y = fitness(y)
            if fit_y > fit_x: 
                x = y
                fit_x = fit_y
                if self_adapt: offspring_size = int(offspring_size / F)
            else:
                if self_adapt: offspring_size = int(offspring_size * (F**0.25))
            if offspring_size <= 1: offspring_size = 1
            
        return x
  

