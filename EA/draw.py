import numpy as np
# import and init pygame
import pygame
import pydot 

import matplotlib.pyplot as plt
import matplotlib.image as mpimg



def draw_graph(edges, image='graph.png', sub_graph=None, path=None):
    if sub_graph == None:
        sub_graph = [1] * len(edges)
        
    graph = pydot.Dot(graph_type='graph')
    
    for i in range(len(edges)):
        for j in range(i):
            if edges[i][j] and sub_graph[i] and sub_graph[j]:
                edge = pydot.Edge("Node %d" % i, "Node %d" % j)
                #graph.add_edge(edge)
            elif sub_graph[i]:
                graph.add_node(pydot.Node("Node %d" % i))
    if path:
        s0 = path[0]
        for i, s in enumerate(path[1:]):
            graph.add_edge(pydot.Edge("Node %d" % s0, "Node %d" % s, 
                                  label='%d' % (i+1), fontsize="30.0", color="blue"))
            s0 = s

    graph.write_png(image)
    
#     img = mpimg.imread( image )
#     plt.imshow( img )
#     plt.show()
    
#     x = 800
#     y = 800
#     pygame.init() 
#     window = pygame.display.set_mode((x, y))
#     window.blit(pygame.image.load(image), (0, 0))
#     pygame.display.flip() 
#     while True: 
#         for event in pygame.event.get(): 
#             if event.type == pygame.QUIT:
#                 return
            
def draw_chess_table(t):
    n = len(t)
    x = 800 
    y = 800
    a = x/n
    
    pygame.init() 
    window = pygame.display.set_mode((x, y)) 
    
    for i in range(n):
        for j in range(n):
            color = (255, 255, 255)
            rect = (a * i, a* j, a, a)
            if (i+j) % 2 == 0:
                pygame.draw.rect(window, color, rect)
    
    queenImg = pygame.image.load('resources/queen.png')
    queenImg = pygame.transform.scale(queenImg, (a, a))
    for i, j in enumerate(t):
        window.blit(queenImg, (i * a, j * a))
        
    # Check for collisions
    x = np.zeros((n , n))
    for i, j in enumerate(t):
        x[i][j] = 1
 
    color = (0, 0, 255) 
    # diags
    for k in range(-n+1, n):
        # diag (i, i+k) (i+k, i)
        q_diag = sum([ x[i][i + k] for i in range(max(0, -k), min(n, n-k))])
        s = max(0, q_diag-1) 
        if  s > 0 :
            start = map(lambda x:a*x, (max(0, -k), max(0, -k)+k))
            end = map(lambda x:a*x, (min(n, n-k), min(n, n-k) + k)) 
            pygame.draw.line(window, color, start, end, 10)
        q_diag = sum([ x[n-i-1][i+k] for i in range(max(0,-k), min(n, n-k))])
        s = max(0, q_diag-1) 
        if  s > 0 :
            start = map(lambda x:a*x, (n-max(0, -k), max(0,-k)+k)) 
            end = map(lambda x:a*x, (n-min(n, n-k), min(n, n-k) + k) )
            pygame.draw.line(window, color, start, end, 10)

    # draw chess board
    pygame.display.flip() 
    while True: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                return
