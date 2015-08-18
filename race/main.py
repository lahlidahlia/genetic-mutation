#!/usr/bin/env python

import pygame
import sys
from pygame.locals import *
import car as Car
import obstacle
import random
import local
import copy

# Setup
pygame.display.init()
pygame.font.init()
fps_clock = pygame.time.Clock()
fps = 100
SCREEN_WIDTH = local.SCREEN_WIDTH
SCREEN_HEIGHT = local.SCREEN_HEIGHT

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("not Pong")

# Color
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
redColor = pygame.Color(255, 0, 0)
blueColor = pygame.Color(0, 0, 255)

font = pygame.font.SysFont("monospace", 20)


# Variables
obstacle_amount = 20
# Generate a new map after map_amount runs
map_amount = 10
# Start a new run after frame amount
frame_amount = 60
# How low can obstacles spawn
obstacle_spawn_min = 100

Car.Car.window = window

# Generate weight lists (chromosomes)
for _ in range(Car.Car.POPULATION):
    # Temp weight list
    weight_ls = []
    for _ in range(Car.Car.CHROMO_SIZE):
        weight_ls.append(random.random() * 2 - 1)
    # Add to the chromosome list (because the weights are chromosomes)
    Car.Car.population_ls.append(weight_ls)

obstacle.generate_obstacle(window, obstacle_amount, SCREEN_WIDTH, SCREEN_HEIGHT - obstacle_spawn_min, blackColor)
# Reset car list
Car.Car.car_list = []
# Get all the weights
weight_ls_ls = copy.deepcopy(Car.Car.population_ls)

# Generate cars
for i in range(Car.Car.POPULATION):
    Car.Car(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 25, redColor, 4, weight_ls_ls.pop())

counter = 0
reset = False
generation = 0
map_counter = 0

while True:
    # Reset the round after a certain amount of frames
    counter += 1
    if counter > frame_amount:
        reset = True
        counter = 0
    # Reset
    if reset:
        generation += 1
        #import pdb; pdb.set_trace()
        ls = Car.Car.score_population(Car.Car.car_ls)
        #print ls
        #print Car.Car.find_winner()

        Car.Car.generate_generation(Car.Car.ELITES)

        # Generate obstacle
        map_counter += 1
        if map_counter >= map_amount:
            map_counter = 0
            obstacle.generate_obstacle(window, obstacle_amount, SCREEN_WIDTH, SCREEN_HEIGHT - obstacle_spawn_min, blackColor)
        # Reset car list
        Car.Car.car_list = []
        # Get all the weights
        weight_ls_ls = copy.deepcopy(Car.Car.population_ls)

        # Delete cars
        for car in Car.Car.car_ls:
            del car
        Car.Car.car_ls = []
        # Create new cars
        for i in range(Car.Car.POPULATION):
            if i < Car.Car.ELITES:
                t_car = Car.Car(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 25, redColor, 4, weight_ls_ls.pop(0))
                t_car.is_elite = True
            else:
                Car.Car(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 25, blueColor, 4, weight_ls_ls.pop(0))
        reset = False
    window.fill(whiteColor)

    # Logic
    # Update cars in backward order so elites gets drawn last (aka on top of other cars)
    for car in Car.Car.car_ls[::-1]:
        v_closest = car.vector_closest_obs(obstacle.Obstacle.obstacle_list)
        v_dir = car.vectorize_direction()
        output = car.neunet.start([v_closest.x, v_closest.y, v_dir.x, v_dir.y])
        car.speed = output[0] * car.MAX_SPEED
        car.d_direction = (output[1] - 0.5) * car.MAX_D_DIRECTION
        car.update()
        #if car.is_elite:
        #    car.draw()
        car.draw()

    for ob in obstacle.Obstacle.obstacle_list:
        ob.draw()

    # Draw
    fps_label = font.render("FPS: {}".format(fps), 1, blackColor)
    generation_label = font.render("Generation: {}".format(generation), 1, blackColor)
    window.blit(fps_label, (SCREEN_WIDTH - 150, 10))
    window.blit(generation_label, (10, 10))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.display.quit()
            pygame.font.quit()
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))
            if event.key == K_LEFT:
                fps /= 5
            if event.key == K_RIGHT:
                fps *= 5
    pygame.display.update()
    fps_clock.tick(fps)
