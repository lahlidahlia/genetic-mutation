#!/usr/bin/env python

import pygame
import sys
from pygame.locals import *
import car as Car
import race_neunet as Neunet
import obstacle
import random
import local

# Setup
pygame.display.init()
pygame.font.init()
fps_clock = pygame.time.Clock()
fps = 30
SCREEN_WIDTH = local.SCREEN_WIDTH
SCREEN_HEIGHT = local.SCREEN_HEIGHT

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Color
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
redColor = pygame.Color(255, 0, 0)

font = pygame.font.SysFont("monospace", 20)

reset = False
counter = 0

Car.Car.window = window

# Generate weight lists (chromosomes)
for _ in range(Car.Car.POPULATION):
    # Temp weight list
    weight_ls = []
    for _ in range(23):
        weight_ls.append(random.random() * 2 - 1)
    # Add to the chromosome list (because the weights are chromosomes)
    Car.Car.population_ls.append(weight_ls)

obstacle.generate_obstacle(window, 10, SCREEN_WIDTH, SCREEN_HEIGHT, blackColor)
# Reset car list
Car.Car.car_list = []
# Get all the weights
weight_ls_ls = Car.Car.population_ls[::]

# Generate cars
for _ in range(Car.Car.POPULATION):
    car = Car.Car(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 25, redColor, 4, weight_ls_ls.pop())
    print "WEIGHT: {}".format(Car.Car.population_ls)

reset = False

while True:
    # Reset the round after a certain amount of time
    counter += 1
    if counter > fps*1:
        reset = 1
        counter = 0
    # Reset
    if reset:
        Car.Car.score_population(Car.Car.car_ls)
        Car.Car.generate_generation("values")

        # Generate obstacle
        obstacle.generate_obstacle(window, 10, SCREEN_WIDTH, SCREEN_HEIGHT, blackColor)
        # Reset car list
        Car.Car.car_list = []
        # Get all the weights
        weight_ls_ls = Car.Car.population_dict.values()

        for _ in range(Car.Car.POPULATION):
            car = Car.Car(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 25, redColor, 4, weight_ls_ls.pop())
        reset = False
    window.fill(whiteColor)

    # Logic
    v_closest = car.vector_closest_obs(obstacle.Obstacle.obstacle_list)
    v_dir = car.vectorize_direction()
    output = car.neunet.start([v_closest.x, v_closest.y, v_dir.x, v_dir.y])
    car.speed = output[0]
    car.d_direction = output[1]
    print output

    # Update
    car.update()

    # Draw
    for ob in obstacle.Obstacle.obstacle_list:
        ob.draw()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.display.quit()
            pygame.font.quit()
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
#            elif event.key == K_LEFT:
#                car.d_direction = -5
#            elif event.key == K_RIGHT:
#                car.d_direction = 5
    car.draw()
    pygame.display.update()
    fps_clock.tick(fps)
