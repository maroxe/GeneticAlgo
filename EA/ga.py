import numpy as np
import random
from scipy.stats import bernoulli
import pygame

clock = pygame.time.Clock()

def default_mutation(l, x):
    bits_to_change = random.sample(range(len(x)), l)
    x_mut = list(x)
    for b in bits_to_change:
        x_mut[b] = random.choice([0, 1])
    return x_mut

def default_crossover(c, x, xx):
    parent = [x, xx]
    parent_choice = bernoulli.rvs(c, size=len(x))
    return [ parent[p][i] for i, p in enumerate(parent_choice) ]


class EA:
    def __init__(self, fitness, mutation=None, crossover=None):
        if not mutation:
            mutation = default_mutation
        if not crossover:
            crossover = default_crossover

            
        self.mutation = mutation
        self.crossover = crossover
        self.fitness = fitness
        

    def run(self, n, x_init, offspring_size=5, n_generations=10, p=None, c=None, self_adapt=False, max_fitness=None):
        # parameters
        if p is None:
            p = float(offspring_size) / n   # mutation probability
        if c is None:
            c = 1. / offspring_size         
        F = 1.5
        
        # initialization
        x = x_init

        fit_x = self.fitness(x)
        # optimization
        for _ in range(n_generations):
        #while fit_x < 0:
            # mutation
            l = np.random.binomial(n, p)
            x_mut = [self.mutation(l, x) for _ in range(offspring_size)]
            xx = x_mut[ np.argmax(map(self.fitness, x_mut)) ] # x'
            

            # crossover
            if offspring_size > 1:
                y_cross = [self.crossover(c, x, xx) for _ in range(offspring_size)]
                y = y_cross[ np.argmax( map(self.fitness, y_cross) ) ]
            else:
                y = xx

            # selection
            fit_y = self.fitness(y)
            if fit_y > fit_x: 
                x = y
                fit_x = fit_y
                if(fit_x == max_fitness):
                    return x  
                
                if self_adapt: 
                    offspring_size = int(offspring_size * (F**0.25))+1
                    
                #yield x

            else:
                if self_adapt: 
                    offspring_size = int(offspring_size / F)
            if offspring_size <= 1: offspring_size = 1
            #list(pygame.event.get())
                    
        return x
  


