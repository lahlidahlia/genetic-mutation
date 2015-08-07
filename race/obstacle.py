#!/usr/bin/env python
import math
import car
import pygame
import random


def generate_obstacle(window, amount, max_x, max_y, color):
    Obstacle.obstacle_list = []
    for i in range(amount):
        while True:
            ob = Obstacle(window, random.randrange(max_x), random.randrange(max_y), color)
            if not Obstacle.check_overlap_obstacle(ob):
                break
            else:
                Obstacle.obstacle_list.remove(ob)


def distance(x1, y1, x2, y2):
    """ Return the distance between 2 points """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class Obstacle:
    """ Obstacle class """

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

    @staticmethod
    def check_overlap_obstacle(obj):
        """ True if this object overlap with any other obstacle """
        if isinstance(obj, Obstacle):
            Obstacle.obstacle_list.remove(obj)
        for obstacle in Obstacle.obstacle_list:
            if distance(obj.position.x, obj.position.y, obstacle.position.x, obstacle.position.y) < (obj.radius + obstacle.radius):
                Obstacle.obstacle_list.append(obj)
                return True
        if isinstance(obj, Obstacle):
            Obstacle.obstacle_list.append(obj)
        return False
