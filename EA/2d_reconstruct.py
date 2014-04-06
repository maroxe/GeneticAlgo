from math import log
import numpy as np
import pygame
import random
import ga
import benchmark
import cProfile
from decbingray import *

n = 256
def array2d(surface):
    """pygame.numpyarray.array2d(Surface): return array
 
    copy pixels into a 2d array
 
    Copy the pixels from a Surface into a 2D array. The bit depth of the
    surface will control the size of the integer values, and will work
    for any type of pixel format.
 
    This function will temporarily lock the Surface as pixels are copied
    (see the Surface.lock - lock the Surface memory for pixel access
    method).
    """
    bpp = surface.get_bytesize()
    try:
        dtype = (np.uint8, np.uint16, np.int32, np.int32)[bpp - 1]
    except IndexError:
        raise ValueError("unsupported bit depth %i for 2D array" % (bpp * 8,))
    size = surface.get_size()
    array = np.empty(size, dtype)
    pygame.pixelcopy.surface_to_array(array, surface)
    return array

def list_to_int(bit_list):
    return bin2dec(''.join(map(str, bit_list)))


def draw_image(image, size):
    srf.fill((0, 0, 0))
    myimage = pygame.image.load(image)
    myimage.convert()
    myimage = pygame.transform.scale(myimage, size)
    srf.blit(myimage, (0, 0))
    pygame.display.flip()
    
def list_to_sphere(s):
        offset = 0
        x = s[offset:offset + max_x]
        offset += max_x
        y = s[offset:offset + max_y]; offset += max_y
        radius = s[offset:offset + max_r]; offset += max_r
        grey = s[offset:offset + max_grey]; offset += max_grey
        alpha = s[offset:offset + max_alpha]
        s = x, y, radius, grey, alpha
        return map(list_to_int, s)
        
# @benchmark.time_it('drawing spheres')
def draw_spheres(spheres):
    srf.fill((0, 0, 0))
    d = sum(dim)
    
    for i in range(n):
        s = spheres[i * d: (i + 1) * d]
        x, y, radius, grey, alpha = list_to_sphere(s)
        alphasurface.fill((0, 0, 0, 0))
        pygame.draw.circle(alphasurface, (grey, grey, grey, alpha), (x, y), radius)
        srf.blit(alphasurface, (0, 0))
    pygame.display.flip()

def fitness(x):
    draw_spheres(x)
    pixels = array2d(srf)
    return -np.linalg.norm((reference_pixels - pixels) / M)



pygame.init()
viewport = (128, 128)
image = "resources/bachir.png"
srf = pygame.display.set_mode(viewport)
alphasurface = srf.convert_alpha()
draw_image(image, viewport)
pygame.image.save(srf, "resources/frames/source.jpg")
reference_pixels = array2d(srf)

M = float(srf.map_rgb(255, 255, 255))
# log2
max_x, max_y = map(lambda x: int(log(x, 2)), viewport)
max_r = 5
max_grey = 8
max_alpha = 8
dim = (max_x, max_y, max_r, max_grey, max_alpha)
x_init = np.random.random_integers(0, 1, n * sum(dim))
def run(): 
    ea_algo = ga.EA(fitness=fitness)
    for i, best_x in  enumerate(ea_algo.run(n, x_init , offspring_size=10, n_generations=100000, p=0.5, c=0.8, self_adapt=False)):
        try:
            pygame.image.save(srf, "resources/frames/frame%d.jpg" % i)
            pygame.image.save(srf, "resources/frames/last_frame.jpg")
        except pygame.error.SaveJPEG:
            print 'Couldn\'t save frame%d.jpg' % i 

cProfile.run('run()', 'resources/restats')
print 'finished'

# print 'fitness = ', fitness(best_x)
# total_time = sum(benchmark.benchmarks.values())
# for k,v in benchmark.benchmarks.iteritems():
#     print k, ':', v/total_time * 100, '%'
