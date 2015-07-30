#!/usr/bin/env python

import pygame, sys
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("pygame test")

whiteColor = pygame.Color(255, 255, 255)
redColor = pygame.Color(255, 0, 0)

window.fill(whiteColor)

pygame.draw.circle(window, redColor, (500, 500), 100)





pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
