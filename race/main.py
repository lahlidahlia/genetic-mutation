#!/usr/bin/env python

import pygame
import sys
from pygame.locals import *
import car as Car
import obstacle

pygame.display.init()
pygame.font.init()
fps_clock = pygame.time.Clock()
fps = 30
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
redColor = pygame.Color(255, 0, 0)

font = pygame.font.SysFont("monospace", 20)

car = Car.Car(window, SCREEN_WIDTH / 2, SCREEN_HEIGHT/2, redColor)

obstacle.generate_obstacle(window, 10, SCREEN_WIDTH, SCREEN_HEIGHT, blackColor)

while True:
    window.fill(whiteColor)
    car.update()
    for ob in obstacle.Obstacle.obstacle_list:
        ob.draw()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.display.quit()
            pygame.font.quit()
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                car.d_direction = -5
            elif event.key == K_RIGHT:
                car.d_direction = 5
            elif event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
    car.draw()
    pygame.display.update()
    fps_clock.tick(fps)
