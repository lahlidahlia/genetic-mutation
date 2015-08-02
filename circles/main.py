#!/usr/bin/env python

import pygame
import sys
import circles as Circle
from pygame.locals import *

pygame.display.init()
pygame.font.init()
fpsClock = pygame.time.Clock()
fps = 100
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

window = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_HEIGHT))
pygame.display.set_caption("pygame test")

whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
redColor = pygame.Color(255, 0, 0)

font = pygame.font.SysFont("monospace", 20)

# circle_ls = [Circle.Vector(187, 382, 46), Circle.Vector(490, 196, 30), Circle.Vector(224, 0, 25), Circle.Vector(438, 270, 47), Circle.Vector(197, 263, 40), Circle.Vector(76, 394, 45), Circle.Vector(499, 451, 49), Circle.Vector(203, 98, 35), Circle.Vector(111, 12, 32), Circle.Vector(37, 483, 40), Circle.Vector(377, 412, 29), Circle.Vector(278, 303, 44), Circle.Vector(298, 411, 39), Circle.Vector(21, 286, 38), Circle.Vector(66, 199, 27), Circle.Vector(16, 116, 49), Circle.Vector(446, 73, 37), Circle.Vector(91, 275, 30), Circle.Vector(491, 346, 27), Circle.Vector(321, 23, 27)]
circle = Circle.Circle(None)
circle_ls = circle.generate_random_circle(
    20, 40, 10, SCREEN_WIDTH, SCREEN_HEIGHT)
circle = Circle.Circle(circle_ls, SCREEN_WIDTH, SCREEN_HEIGHT)
for _ in range(circle.POPULATION):
    chromo = (circle.generate_chromo(circle.BIT_SIZE))
    circle.population_dict[chromo] = circle.get_fitness_score(chromo)
    # print circle.population_dict
    circle.population_avg.append(
        circle.population_fitness_avg(circle.population_dict))
gen_count = 0

while True:
    gen_count += 1
    # Generate population
    circle.population_dict = circle.generate_generation(
        circle.population_dict, 4)
    # Find fitness average
    circle.population_avg.append(
        circle.population_fitness_avg(circle.population_dict))
    # Display
    window.fill(whiteColor)
    for c in circle_ls:
        pygame.draw.circle(window, redColor, (c.x, c.y), c.r, 2)
#    for chromo in circle.population_dict.keys():
#        c = circle.parse_chromo(chromo)
#        pygame.draw.circle(window, blackColor, (c.x, c.y), c.r, 2)
#    winner = circle.parse_chromo(circle.find_winner(circle.population_dict))
#    pygame.draw.circle(window, blackColor, (winner.x, winner.y), winner.r)
    winners = circle.get_largest(4, circle.population_dict)
    for winner in winners:
        winner = circle.parse_chromo(winner)
        pygame.draw.circle(
            window, blackColor, (winner.x, winner.y), winner.r, 2)

    text = font.render("{}".format(gen_count), 1, blackColor)
    window.blit(text, (20, 20))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.display.quit()
            pygame.font.quit()
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    pygame.display.update()
    fpsClock.tick(fps)
