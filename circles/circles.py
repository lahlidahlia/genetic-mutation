import random
import math
import genetics
from collections import namedtuple

Vector = namedtuple('Vector', 'x y r')


class Circle(genetics.Genetics):
    """ Circle Class """
    CROSSOVER_RATE = 0.7
    MUTATION_RATE = 0.2
    POPULATION = 150
    ELITES = 8
    CHROMO_SIZE = 30
    max_x = 500
    max_y = 500
    # List of pre-gen circles
    static_circle_list = []


    def __init__(self, max_x=500, max_y=500):
        self.max_x = max_x
        self.max_y = max_y

    @classmethod
    def parse_chromo(cls, chromo):
        """ Parse chromo into string values stored in Vector"""
        x, left_over = cls.convert_chromo_int(chromo, 10)
        y, left_over = cls.convert_chromo_int(left_over, 10)
        r, _ = cls.convert_chromo_int(left_over, 10)
        # Set minimum for radius
        r += 2
        if x > cls.max_x:
            x = cls.max_x
        if y > cls.max_x:
            y = cls.max_y
        return Vector(x, y, r)

    @classmethod
    def get_fitness_score(cls, chromo):
        circle = cls.parse_chromo(chromo)
        score = circle.r
        if(cls.check_for_overlap(circle, cls.static_circle_list)
                or cls.check_for_outside(circle)):
            score = 1
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

    @classmethod
    def check_for_overlap(cls, given_circle, circle_ls):
        """ Given a list of circle, check the given circle for overlap
            given_circle should be a vector
            Returns number of circle overlapped"""
        amnt = 0
        for circle in circle_ls:
            if(cls.distance(given_circle.x, given_circle.y, circle.x,
                             circle.y) < circle.r + given_circle.r):
                amnt += 1
        if amnt:
            return amnt
        else:
            return False

    @classmethod
    def check_for_outside(cls, circle):
        """ Check if circle is going outside of screen """
        if(circle.x + circle.r > cls.max_x
                or circle.x - circle.r < 0
                or circle.y + circle.r > cls.max_y
                or circle.y - circle.r < 0):
            return True
        return False

    @classmethod
    def distance(self, x1, y1, x2, y2):
        """ Return the distance between 2 points """
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
