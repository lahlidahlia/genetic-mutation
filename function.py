import random
import math
from collections import namedtuple

Vector = namedtuple('Vector', 'x y r')
def generate_random_circle(min_radius, max_radius, amount, max_x, max_y):
    """ Generate non-overlapping circles """
    # [[Vector(x,y,r)], ...]
    ret = []
    for _ in range(amount):
        while True:
             circle = Vector(random.randrange(max_x),
                             random.randrange(max_y),
                             random.randrange(min_radius, max_radius))
             if not check_for_overlap(circle, ret):
                 break
        ret.append(circle)
    return ret

def check_for_overlap(given_circle, ls):
    """ Given a list of circle, check the given circle for overlap """
    for circle in ls:
        if(distance(given_circle.x, given_circle.y, circle.x, circle.y) < circle.r + given_circle.r):
            return True
    return False

def distance(x1, y1, x2, y2):
    """ Return the distance between 2 points """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
