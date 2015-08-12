import random
import abc
import heapq


class Genetics:
    __metaclass__ = abc.ABCMeta

    # Default variables, reset through extending as needed
    CROSSOVER_RATE = 0.7
    MUTATION_RATE = 0.1
    # Values are: binary, value (case sensitive)
    ENC_TYPE = "binary"
    # If enc_type is value, max_value defines how much the value can mutate
    MAX_MUTATE = 0
    POPULATION = 150
    CHROMO_SIZE = 23
    # Elites are how many well performing chromosomes gets transferred to
    # the next generation.
    ELITES = False

    # Class lists, try not to scramble these around,
    # they rely on correct ordering
    # Contains the chromosomes
    population_ls = []
    # Contains fitness score of each chromosome
    population_fitness = []
    population_avg = []

    def parse_chromo(self, chromo):
        """ Needs to be redefined if chromo needs to be parsed
            Parse the chromo into whatever format """
        pass

    @abc.abstractmethod
    def get_fitness_score(self, chromo):
        """ Return the fitness score (int) of a chromosome """
        pass

    @classmethod
    def find_winner(cls):
        """ Return the one with the best fitness score in the population """
        return cls.population_ls[cls.population_fitness.index(max(cls.population_fitness))]

    # CONVERSION
    def convert_chromo_table(self, chromo, step, table):
        """ Convert a step amount of bits at a time into values in table """
        # TODO: Allow splitting chromo
        # Table should follow format {"0000": foo, ...}
        ret = []
        for i in range(0, len(chromo), step):
            ret.append(table[chromo[i:i+step]])
        return ret

    @classmethod
    def convert_chromo_int(cls, chromo, step):
        """ Convert a step amount of bits at a time into int
            Returns the bits and left over bits"""
        ret = int(chromo[:step], 2)
        left_over = chromo[step:]
        return ret, left_over

    # GENERATION
    def generate_binary_chromo(self, length):
        """ Generate a string of random binary string of a given length """
        ret = ""
        for _ in range(length):
            ret += str(random.randrange(2))
        return ret

    # REPRODUCTION
    @classmethod
    def cross_over(cls, chromo_1, chromo_2, rate, size):
        """ Chance to cross 2 chromosomes
            Returns a tuple of 2 chromos """
        if(random.random() < rate):
            pos = random.randrange(size)
            t1 = chromo_1[pos:]
            t2 = chromo_2[pos:]
            chromo_1 = chromo_1[:pos] + t2
            chromo_2 = chromo_2[:pos] + t1
        return (chromo_1, chromo_2)

    @classmethod
    def mutate(cls, chromo):
        """ For each bit, have a <rate> chance to mutate it """
        if cls.ENC_TYPE == "binary":
            ret = ""
            for bit in chromo:
                if(random.random() < cls.MUTATION_RATE):
                    # Flip bit
                    ret += "1" if bit == "0" else "0"
                else:
                    ret += bit
            return ret

        if cls.ENC_TYPE == "value":
            ret = []
            for v in chromo:
                if(random.random() < cls.MUTATION_RATE):
                    # Add or subtract random amount from the number
                    ret.append(
                        v + (random.random() *
                             cls.MAX_MUTATE * 2 - cls.MAX_MUTATE))
                else:
                    ret.append(v)
            return ret

    @classmethod
    def reproduce(cls, chromo_1, chromo_2):
        """ Create 2 new chromos from 2 chromos """
        offspring_1, offspring_2 = cls.cross_over(chromo_1,
                                                  chromo_2,
                                                  cls.CROSSOVER_RATE,
                                                  cls.CHROMO_SIZE)
        offspring_1 = cls.mutate(offspring_1)
        offspring_2 = cls.mutate(offspring_2)
        return (offspring_1, offspring_2)

    @classmethod
    def choose_randomly_roulette(cls):
        """ Choose randomly between items in probability dict """
        # dict should follow the format: {item1: prob, item2: prob}
        prob_sum = 0
        #print cls.population_fitness
        #print cls.population_ls
        for v in cls.population_fitness:
            prob_sum += v
        r = random.random() * prob_sum
        sum_so_far = 0
        for k, v in zip(cls.population_ls, cls.population_fitness):
            #print k, v
            sum_so_far += v
            if(r < sum_so_far):
                # The chromo that "won"
                return k

    @classmethod
    def score_population(cls):
        """ Give each chromo in the population a score """
        cls.population_fitness = []
        for chromo in cls.population_ls:
            cls.population_fitness.append(cls.get_fitness_score(chromo))
        return cls.population_ls

    @classmethod
    def generate_generation(cls, elites=False):
        """ Generate a new generation using multiple factors

            Arguments:
            elites -- If given as an int, will retain a specified amount
                      of best performing chromosomes in the next generation

            Make sure to call score_population before this method
            """
        # population should follow format {chromo: score, ...}
        # Temp list
        new_population = []
        if elites:
            # Best performing chromosomes will be kept in the next generation
            elite_ls = cls.get_best(elites)
            for chromo in elite_ls:
                new_population.append(chromo)
        while(len(new_population) < cls.POPULATION):
            # Generates chromosomes until specified population is reached

            # Choose the chromosomes to breed
            parent_1 = cls.choose_randomly_roulette()
            parent_2 = cls.choose_randomly_roulette()
            # Reproduce (crossover and mutate)
            offspring_1, offspring_2 = cls.reproduce(parent_1,
                                                     parent_2)
            new_population.append(offspring_1)
            new_population.append(offspring_2)
        cls.population_ls = new_population
        return cls.population_ls

    @classmethod
    def get_best(cls, amount):
        """ Return the best performing chromosomes """
        ret = []
        # Find best scores
        fitness_ls = heapq.nlargest(amount, cls.population_fitness)
        for fitness in fitness_ls:
            ret.append(
                cls.population_ls[cls.population_fitness.index(fitness)])
        return ret

    # FITNESS
    def population_fitness_avg(self, population):
        """ Calculates the population's average fitness score """
        # population should be a dict that follows {chromo: score}
        sum = 0
        for v in population.values():
            sum += v
        sum /= float(len(population.values()))
        return sum
