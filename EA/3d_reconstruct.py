import numpy as np
from objloader import *
import pygame


pygame.init()
viewport = (100,100)
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
reference = project_obj(srf, (0, 50, 0), "teddy.obj", "screen.bmp")

def fitness(x):
    pixels = project_sphere(srf, (0, 50, 0), x, "screen2.bmp")
    return - np.sum(pixels == reference)

boundary = 20
n = 1000
x_init = np.random.randint(low=-boundary, high=boundary, size=(n, 3))
print fitness(x_init)
