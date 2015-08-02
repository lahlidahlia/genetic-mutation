import random
import math
import genetics
from collections import namedtuple

Vector = namedtuple('Vector', 'x y r')


class Circle(genetics.Genetics):
    """ Circle Class """
    BIT_SIZE = 30
    CROSSOVER_RATE = 0.7
    MUTATION_RATE = 0.2
    POPULATION = 150
    ELITES = 8
    max_x = 500
    max_y = 500
    static_circle_list = []

    def __init__(self, circle_list, max_x=500, max_y=500):
        self.static_circle_list = circle_list
        self.max_x = max_x
        self.max_y = max_y

    def parse_chromo(self, chromo):
        """ Parse chromo into string values stored in Vector"""
        x, left_over = self.convert_chromo_int(chromo, 10)
        y, left_over = self.convert_chromo_int(left_over, 10)
        r, _ = self.convert_chromo_int(left_over, 10)
        # Set minimum for radius
        r += 2
        if x > self.max_x:
            x = self.max_x
        if y > self.max_x:
            y = self.max_y
        return Vector(x, y, r)

    def get_fitness_score(self, chromo):
        circle = self.parse_chromo(chromo)
        score = circle.r
        if(self.check_for_overlap(circle, self.static_circle_list)
                or self.check_for_outside(circle)):
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

    def check_for_outside(self, circle):
        """ Check if circle is going outside of screen """
        if(circle.x + circle.r > self.max_x
                or circle.x - circle.r < 0
                or circle.y + circle.r > self.max_y
                or circle.y - circle.r < 0):
            return True
        return False

    def get_largest(self, n, d):
        """ Get the largest n values from a dict """
        ret = {}
        ls = sorted(d.values(), reverse=True)[:n]
        for i in ls:
            k = d.keys()
            v = d.values()
            index = v.index(i)
            ret[k[index]] = v[index]
        return ret

    def distance(self, x1, y1, x2, y2):
        """ Return the distance between 2 points """
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
