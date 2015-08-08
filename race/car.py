#!/usr/bin/env python
from collections import namedtuple
import math
import pygame
import obstacle
from genetics import Genetics
import local
import race_neunet

Vector = namedtuple('Vector', 'x y')


class Car(Genetics):
    """ Car class """
    # Display window
    window = None
    car_ls = []

    CROSSOVER_RATE = 0.7
    MUTATION_RATE = 0.1
    MAX_MUTATE = 0.5
    POPULATION = 10
    CHROMO_SIZE = 23

    MAX_SPEED = 10
    # Max turn speed
    MAX_D_DIRECTION = 50
    ELITES = 2

    # Contains weights
    population_ls = []
    population_fitness = []
    population_avg = []
    def __init__(self, x, y, color_chassis, input_size, weight_ls):
        self.position = Vector(x, y)
        # 0 = East
        self.direction = 90
        self.speed = 0
        # Radius of the car (because it's a circle)
        self.radius = 5
        # Change in direction, + is right, - is left from the bottom
        self.d_direction = 0
        self.color_chassis = color_chassis
        # Direction arrow
        self.color_direction = color_chassis
        # Direction arrow
        self.arrow_length = self.radius + self.radius*0.5
        self.neunet = race_neunet.RaceNeuNet(input_size, weight_ls)

        self.max_score = 0
        Car.car_ls.append(self)

        # Determines if car is stopped by something
        self.stopped = False

    def parse_chromo(self, chromo):
        pass

    def get_fitness_score(self, car):
        return local.SCREEN_HEIGHT - car.position.y

    @classmethod
    def score_population(cls, car_ls):
        cls.population_fitness = []
        for car in car_ls:
            cls.population_fitness.append(car.get_fitness_score(car))
        return cls.population_fitness

    def update(self):
        # Only move if the car isn't stopped
        if not self.stopped:
            self.direction += self.d_direction
            # Normalize direction to 0 - 360
            if self.direction > 360:
                self.direction - 360
            if self.direction < 0:
                self.direction + 360
            # Calculate position
            new_x = self.position.x + math.cos(math.radians(self.direction)) * self.speed
            new_y = self.position.y - math.sin(math.radians(self.direction)) * self.speed
            self.position = Vector(new_x, new_y)
            # Score updating
            score = local.SCREEN_HEIGHT - self.position.y
            if score > self.max_score:
                self.max_score = score
            # Check if collided with obstacle or boundary
            if obstacle.Obstacle.check_overlap_obstacle(self) or self.check_out_of_bound():
                self.stopped = True

    def check_out_of_bound(self):
        """ Check if object is out of bound """
        if(self.position.x + self.radius > local.SCREEN_WIDTH
                or self.position.x - self.radius < 0
                or self.position.y + self.radius > local.SCREEN_HEIGHT
                or self.position.y - self.radius < 0):
            return True
        return False
    def vector_closest_obs(self, obs_list):
        """ Returns the vector to the closest obstacle """
        closest_ob = None
        closest_dist = 99999
        for ob in obs_list:
            dist = obstacle.distance(self.position.x, self.position.y, ob.position.x, ob.position.y)
            if dist < closest_dist:
                closest_ob = ob
                closest_dist = dist
        return Vector(closest_ob.position.x - self.position.x, (closest_ob.position.x - self.position.x))

    def vectorize_direction(self):
        """ Turn direction into a vector """
        # Convert direction to radians for easier computation
        rad_dir = math.radians(self.direction)
        return Vector(math.cos(rad_dir), math.sin(rad_dir))

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
