#!/usr/bin/env python
from collections import namedtuple
import math
import car
import pygame
import random


def generate_obstacle(window, amount, max_x, max_y, color):
    for i in range(amount):
        while True:
            ob = Obstacle(window, random.randrange(max_x), random.randrange(max_y), color)
            if(not ob.check_overlap_obstacle()):
                break
            else:
                Obstacle.obstacle_list.remove(ob)


def distance(x1, y1, x2, y2):
    """ Return the distance between 2 points """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class Obstacle:
    """ Obstacle class """

    position = None
    radius = 20  # Circular obstacle

    window = None  # Display window
    color = None

    obstacle_list = []

    def __init__(self, window, x, y, color):
        self.window = window
        self.color = color
        self.position = car.Vector(x, y)
        Obstacle.obstacle_list.append(self)

    def draw(self):
        pygame.draw.circle(self.window,
                           self.color,
                           (int(self.position.x),
                               int(self.position.y)),
                           self.radius, 1)

    def check_overlap_obstacle(self):
        """ True if this object overlap with any other obstacle """
        Obstacle.obstacle_list.remove(self)
        for obstacle in Obstacle.obstacle_list:
            if distance(self.position.x, self.position.y, obstacle.position.x, obstacle.position.y) < (self.radius + obstacle.radius):
                Obstacle.obstacle_list.append(self)
                return True
        Obstacle.obstacle_list.append(self)
        return False
