#!/usr/bin/env python
from collections import namedtuple
import math
import pygame

Vector = namedtuple('Vector', 'x y')


class Car:
    """ Car class """
    position = Vector(0, 0)
    direction = 90  # 0 = East
    speed = 5

    radius = 20  # Radius of the car (because it's a circle)
    d_direction = 0  # Change in direction, + is right, - is left from the bottom

    window = None  # Display window
    color_chassis = None
    color_direction = None  # Direction arrow
    arrow_length = 0  # Direction arrow

    def __init__(self, window, x, y, color_chassis):
        self.position = Vector(x, y)
        self.window = window
        self.color_chassis = color_chassis
        self.color_direction = color_chassis

    def update(self):
        self.direction += self.d_direction
        new_x = self.position.x + math.cos(math.radians(self.direction)) * self.speed
        new_y = self.position.y - math.sin(math.radians(self.direction)) * self.speed
        self.position = Vector(new_x, new_y)
        self.arrow_length = self.radius + 5

    def draw(self):
        pygame.draw.circle(self.window,
                           self.color_chassis,
                           (int(self.position.x), int(self.position.y)),
                           self.radius,
                           1)
        pygame.draw.line(self.window,
                         self.color_direction,
                         (int(self.position.x), int(self.position.y)),
                         (int(self.position.x + math.cos(math.radians(self.direction)) * self.arrow_length),
                             int(self.position.y - math.sin(math.radians(self.direction)) * self.arrow_length)))
