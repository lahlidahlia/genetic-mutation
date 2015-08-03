import random
import abc


class Genetics:
    __metaclass__ = abc.ABCMeta

    # Default variables, reset as needed
    CROSSOVER_RATE = 0.7
    MUTATION_RATE = 0.1
    POPULATION = 50

    population_dict = {}
    population_avg = []

    @abc.abstractmethod
    def parse_chromo(self, chromo):
        """ Parse the chromo into whatever format """
        pass

    @abc.abstractmethod
    def get_fitness_score(self, chromo):
        """ Return the fitness score (int) of a chromosome """
        pass

    @abc.abstractmethod
    def find_winner(self, population):
        """ Return the one with the best fitness score in the population """
        k_ls = []
        v_ls = []
        for k, v in population.iteritems():
            k_ls.append(k)
            v_ls.append(v)
        return k_ls[v_ls.index(max(v_ls))]

    # CONVERSION
    def convert_chromo_table(self, chromo, step, table):
        """ Convert a step amount of bits at a time into values in table """
        # TODO: Allow splitting chromo
        # Table should follow format {"0000": foo, ...}
        ret = []
        for i in range(0, len(chromo), step):
            ret.append(table[chromo[i:i+step]])
        return ret

    def convert_chromo_int(self, chromo, step):
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
    def cross_over(self, chromo_1, chromo_2, rate):
        """ Cross 2 chromosomes over, dependant on rate """
        if(random.random() < rate):
            pos = random.randrange(20)
            t1 = chromo_1[pos:]
            t2 = chromo_2[pos:]
            chromo_1 = chromo_1[:pos] + t2
            chromo_2 = chromo_2[:pos] + t1
        return (chromo_1, chromo_2)

    def mutate(self, chromo, rate):
        """ For each bit, have a <rate> chance to flip it """
        ret = ""
        for bit in chromo:
            if(random.random() < rate):
                ret += "1" if bit == "0" else "0"
            else:
                ret += bit
        return ret

    def reproduce(self, chromo_1, chromo_2):
        """ Create 2 new chromos from 2 chromos """
        # print "1: {}. 2: {}".format(chromo_1, chromo_2)
        offspring_1, offspring_2 = self.cross_over(
                                                chromo_1,
                                                chromo_2,
                                                self.CROSSOVER_RATE)
        offspring_1 = self.mutate(offspring_1, self.MUTATION_RATE)
        offspring_2 = self.mutate(offspring_2, self.MUTATION_RATE)
        # print "1: {}. 2: {}".format(offspring_1, offspring_2)

        return (offspring_1, offspring_2)

    def choose_randomly_roulette(self, probability_dict):
        """ Choose randomly between items in probability dict """
        # dict should follow the format: {item1: prob, item2: prob}
        prob_sum = 0
        for v in probability_dict.values():
            prob_sum += v
        r = random.random() * prob_sum
        sum_so_far = 0
        for k, v in probability_dict.iteritems():
            sum_so_far += v
            if(r < sum_so_far):
                # The chromo that "won"
                return k

    def generate_generation(self, population, elites=False):
        """ Generate a new generation using multiple factors
            If elites is given as an int, will also include elites
            number of best scoring chromo in the next gen"""
        # population should follow format {chromo: score, ...}
        new_population = {}
        if elites:
            new_population.update(self.get_largest(elites, population))
        while(len(new_population) < self.POPULATION):
            parent_1 = self.choose_randomly_roulette(population)
            parent_2 = self.choose_randomly_roulette(population)
            # print "{}, {}".format(parent_1, parent_2)
            offspring_1, offspring_2 = self.reproduce(parent_1,
                                                      parent_2)
            new_population[offspring_1] = self.get_fitness_score(offspring_1)
            new_population[offspring_2] = self.get_fitness_score(offspring_2)
            # print "{}, {}".format(offspring_1, offspring_2)
        population = new_population
        return population

    # FITNESS
    def population_fitness_avg(self, population):
        """ Calculates the population's average fitness score """
        # population should be a dict that follows {chromo: score}
        sum = 0
        for v in population.values():
            sum += v
        sum /= float(len(population.values()))
        return sum
