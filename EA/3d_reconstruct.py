import numpy as np
from scipy.stats import bernoulli
from objloader import *
import pygame
import random
import ga

pygame.init()
viewport = (1024,768)
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
reference = project_obj(srf, (0, 50,0), "teddy.obj", "screen3.bmp")
max_fitness = np.sum(reference == reference)
print 'max=', max_fitness

def fitness(x):
    pixels = project_sphere(srf, (0, 50, 0), x, None)
    return  np.sum(pixels == reference)


def mutation(l, x, bit_range):
    bits_to_change = random.sample(range(len(x)), l)
    x_mut = np.copy(x)
    for i in range(l):
        x_mut[bits_to_change[i]] = np.random.randint(low=-boundary, high=boundary, size=3)
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
#1440000
#1306059


boundary = 30
n = 20
ea_algo = ga.EA(fitness=fitness, mutation=mutation)
x_init = np.random.randint(low=-boundary, high=boundary, size=(n, 3))
best_x =  ea_algo.run(n,x_init , offspring_size=5, n_generations=100,  p=0.7)
project_sphere(srf, (0, 50, 0), best_x, "bestx.bmp")
print fitness(best_x)
