import numpy as np
from scipy.stats import bernoulli
from objloader import *
import pygame
import random
import ga
 


top_view = ( 50, 0, 0)
side_view = (0, 50, 0)

pygame.init()
viewport = (800,600)
model = "torus.obj"
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
top_reference = project_obj(srf, top_view, model, "top_view.bmp")
side_reference = project_obj(srf, side_view, model, "side_view.bmp")

max_fitness = np.sum(top_reference == top_reference) + np.sum(side_reference  == side_reference)
print 'max=', max_fitness

def fitness(x):
    top_pixels = project_sphere(srf, top_view, x, None)
    side_pixels = project_sphere(srf, side_view, x, None)
    return  np.sum(top_reference == top_pixels) + np.sum(side_reference ==side_pixels)


def mutation(l, x, bit_range):
    bits_to_change = random.sample(range(len(x)), l)
    x_mut = np.copy(x)
    for i in range(l):
        x_mut[bits_to_change[i]] = x_mut[bits_to_change[i]] + np.random.randint(low=-2, high=+2, size=3)
    return x_mut

def crossover(c, x, xx):
    parent = [x, xx]
    parent_choice = bernoulli.rvs(c, size=len(x))
    y = []

    for i, p in enumerate(parent_choice):
        y.append(parent[p][i])
    return y



boundary = 20
n = 1000
ea_algo = ga.EA(fitness=fitness, mutation=mutation)
x_init = np.random.randint(low=-boundary, high=boundary, size=(n, 3))
best_x =  ea_algo.run(n,x_init , offspring_size=5, n_generations=100,  p=0.5)
project_sphere(srf, top_view, best_x, "best_top.bmp")
project_sphere(srf, side_view, best_x, "best_side.bmp")

print fitness(best_x)
render_spheres(srf, best_x, side_view)