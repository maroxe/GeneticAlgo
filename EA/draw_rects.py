import pygame

def draw_rects(srf, rects):
    for rect in rects:
        box = pygame.Rect(*rect)
        pygame.draw.rect(srf, (x,0,y), box, 0)
        