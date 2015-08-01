#!/usr/bin/env python

import pygame
import sys
import function
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()
fps = 60
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

window = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_HEIGHT))
pygame.display.set_caption("pygame test")

whiteColor = pygame.Color(255, 255, 255)
redColor = pygame.Color(255, 0, 0)

circle_ls = function.generate_random_circle(25, 50, 20, SCREEN_WIDTH, SCREEN_HEIGHT)

while True:
    window.fill(whiteColor)
    for circle in circle_ls:
        pygame.draw.circle(window, redColor, (circle.x, circle.y), circle.r, 2)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    pygame.display.update()
    fpsClock.tick(fps)
