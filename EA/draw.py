import numpy as np
import pygame

   

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
