import pprint
import random
import abc
import heapq


class Genetics:
    __metaclass__ = abc.ABCMeta

    # Default variables, reset as needed
    CROSSOVER_RATE = 0.7
    MUTATION_RATE = 0.1
    POPULATION = 50
    CHROMO_SIZE = 0

    population_ls = []
    population_fitness = []
    population_avg = []


    @abc.abstractmethod
    def parse_chromo(self, chromo):
        """ Parse the chromo into whatever format """
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
    def generate_chromo(self, n):
        """ Generate a string of n bit """
        ret = ""
        for _ in range(n):
            ret += str(random.randrange(2))
        return ret

    # REPRODUCTION
    @classmethod
    def cross_over(cls, chromo_1, chromo_2, rate, size):
        """ Cross 2 chromosomes over, dependant on rate """
        if(random.random() < rate):
            pos = random.randrange(size)
            t1 = chromo_1[pos:]
            t2 = chromo_2[pos:]
            chromo_1 = chromo_1[:pos] + t2
            chromo_2 = chromo_2[:pos] + t1
        return (chromo_1, chromo_2)

    @classmethod
    def mutate(cls, chromo, rate):
        """ For each bit, have a <rate> chance to flip it """
        ret = ""
        for bit in chromo:
            if(random.random() < rate):
                ret += "1" if bit == "0" else "0"
            else:
                ret += bit
        return ret

    @classmethod
    def mutate_value(cls, chromo, rate, maximum):
        """ Mutate with value chromo """
        ret = []
        for v in chromo:
            if(random.random() < rate):
                ret.append(v + (random.random() * maximum * 2 - maximum))
            else:
                ret.append(v)
        return ret


    @classmethod
    def reproduce(cls, chromo_1, chromo_2, enc_type="binary", max_mutate=0):
        """ Create 2 new chromos from 2 chromos
            type can be "binary" or "values" """
        # print "1: {}. 2: {}".format(chromo_1, chromo_2)
        # print chromo_1, chromo_2
        offspring_1, offspring_2 = cls.cross_over(
                                                chromo_1,
                                                chromo_2,
                                                cls.CROSSOVER_RATE,
                                                cls.CHROMO_SIZE)
        if enc_type == "binary":
            offspring_1 = cls.mutate(offspring_1, cls.MUTATION_RATE)
            offspring_2 = cls.mutate(offspring_2, cls.MUTATION_RATE)
        elif enc_type == "values":
            offspring_1 = cls.mutate_value(offspring_1, cls.MUTATION_RATE, max_mutate)
            offspring_2 = cls.mutate_value(offspring_2, cls.MUTATION_RATE, max_mutate)
        # print "1: {}. 2: {}".format(offspring_1, offspring_2)

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
    def generate_generation(cls, enc_type="binary", elites=False, max_mutate=0):
        """ Generate a new generation using multiple factors
            If elites is given as an int, will also include elites
            number of best scoring chromo in the next gen
            type can be "binary" or "values"
            Need to run score_population to assign fitness """
        # population should follow format {chromo: score, ...}
        # Temp list
        new_population = []
        if type(elites) == int:
            #import pdb; pdb.set_trace()
            elite_ls = cls.get_largest(elites)
            for chromo in elite_ls:
                new_population.append(chromo)
                print "Generate : {}".format(chromo)
                print ""
        while(len(new_population) < cls.POPULATION):
            parent_1 = cls.choose_randomly_roulette()
            parent_2 = cls.choose_randomly_roulette()
            #print parent_1, parent_2
            # print "{}, {}".format(parent_1, parent_2)
            offspring_1, offspring_2 = cls.reproduce(parent_1,
                                                  parent_2,
                                                  enc_type,
                                                  max_mutate)
            # print "{}, {}".format(offspring_1, offspring_2)
            new_population.append(offspring_1)
            new_population.append(offspring_2)
        cls.population_ls = new_population
        return cls.population_ls

    @classmethod
    def get_largest(cls, amount):
        """ Get the best performing chromosome """
        fitness_ls = heapq.nlargest(amount, cls.population_fitness)
        print "Largest: {}".format(fitness_ls)
        print ""
        ret = []
        for fitness in fitness_ls:
            print "Fitness weight: {}".format(cls.population_ls[cls.population_fitness.index(fitness)])
            ret.append(cls.population_ls[cls.population_fitness.index(fitness)])
        return ret

    @classmethod
    def score_population(cls):
        """ Give each chromo in the population a score """
        cls.population_fitness = []
        for chromo in cls.population_ls:
            cls.population_fitness.append(cls.get_fitness_score(chromo))
        return cls.population_ls

    # FITNESS
    def population_fitness_avg(self, population):
        """ Calculates the population's average fitness score """
        # population should be a dict that follows {chromo: score}
        sum = 0
        for v in population.values():
            sum += v
        sum /= float(len(population.values()))
        return sum
