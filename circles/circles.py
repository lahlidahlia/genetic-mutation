import random
import math
import genetics
from collections import namedtuple

Vector = namedtuple('Vector', 'x y r')


class Circle(genetics.Genetics):
    """ Circle Class """
    BIT_SIZE = 27
    CROSSOVER_RATE = 0.7
    MUTATION_RATE = 0.1
    POPULATION = 50
    # Score subtracted for overlapping
    OVERLAP_PENALTY = 5
    static_circle_list = []

    def __init__(self, circle_list):
        self.static_circle_list = circle_list

    def parse_chromo(self, chromo):
        """ Parse chromo into string values stored in Vector"""
        x, left_over = self.convert_chromo_int(chromo, 10)
        y, left_over = self.convert_chromo_int(left_over, 10)
        r, _ = self.convert_chromo_int(left_over, 7)
        # Set minimum for r
        r += 2
        return Vector(x, y, r)

    def get_fitness_score(self, chromo):
        circle = self.parse_chromo(chromo)
        score = circle.r
        score -= self.check_for_overlap(circle, self.static_circle_list)*5
        if score < 0:
            score = 0
        return score

    def find_winner(self, population):
        return super(Circle, self).find_winner(population)

    def generate_random_circle(self, min_radius, max_radius, amount, max_x,
                               max_y):
        """ Generate non-overlapping circles """
        # [[Vector(x,y,r)], ...]
        ret = []
        for _ in range(amount):
            while True:
                circle = Vector(
                    random.randrange(max_x),
                    random.randrange(max_y),
                    random.randrange(min_radius, max_radius))
                if not self.check_for_overlap(circle, ret):
                    break
            ret.append(circle)
        return ret

    def check_for_overlap(self, given_circle, circle_ls):
        """ Given a list of circle, check the given circle for overlap
            given_circle should be a vector
            Returns number of circle overlapped"""
        amnt = 0
        for circle in circle_ls:
            if(self.distance(given_circle.x, given_circle.y, circle.x,
                             circle.y) < circle.r + given_circle.r):
                amnt += 1
        if amnt:
            return amnt
        else:
            return False

    def distance(self, x1, y1, x2, y2):
        """ Return the distance between 2 points """
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
