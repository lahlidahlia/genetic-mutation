import string
import __future__
import genetics


class EquationGenerator(genetics.Genetics):
    TARGET_NUMBER = 60
    CROSSOVER_RATE = 0.7
    MUTATION_RATE = 0.1
    POPULATION = 50

    gene_table = {'0000': '0',
                  '0001': '1',
                  '0010': '2',
                  '0011': '3',
                  '0100': '4',
                  '0101': '5',
                  '0110': '6',
                  '0111': '7',
                  '1000': '8',
                  '1001': '9',
                  '1010': '+',
                  '1011': '-',
                  '1100': '*',
                  '1101': '/',
                  '1110': 'X',
                  '1111': 'X'}

    def parse_chromo(self, chromo, with_log=False):
        super(EquationGenerator, self).parse_chromo(chromo)
        input_ls = self.convert_chromo_table(chromo, 4, self.gene_table)
        input_str = ""
        for i in input_ls:
            input_str += i
        operators = ['+', '-', '*', '/']
        # State of characters sequence needs to alternate
        is_state_number = True
        filtered_string = ""
        if with_log:
            print "Input: " + input_str
        for i in input_str:
            if is_state_number and i in string.digits:
                filtered_string += i
                is_state_number = not is_state_number
            elif not is_state_number and i in operators:
                filtered_string += i
                is_state_number = not is_state_number
        # Remove the last character if not digit
        if filtered_string[-1:] not in string.digits:
            filtered_string = filtered_string[:-1]
        if with_log:
            print "Filtered: " + filtered_string
        # All the compile stuffs is to make sure it eval the digits as if they
        # were float, otherwise, just a normal eval function
        try:
            ret = eval(compile(
                filtered_string,
                '<string>',
                'eval',
                __future__.division.compiler_flag))
        except:
            ret = 0
        return ret

    def get_fitness_score(self, chromo):
        result = self.parse_chromo(chromo)
        if(result == self.TARGET_NUMBER):
            return 2
        else:
            return 10 / float((self.TARGET_NUMBER - result))

    def find_winner(self, population):
        for chromo in population.keys():
            if self.parse_chromo(chromo) == self.TARGET_NUMBER:
                return chromo
        return False

if __name__ == "__main__":
    equation = EquationGenerator()
    winning_chromo = ""
    population_avg = []
    population = {}
    for i in range(equation.POPULATION):
        chromo = equation.generate_chromo(20)
        population[chromo] = equation.get_fitness_score(chromo)
    population_avg.append(equation.population_fitness_avg(population))

    while not winning_chromo:
        population = equation.generate_generation(
            population,
            equation.POPULATION,
            equation.CROSSOVER_RATE,
            equation.MUTATION_RATE)
        t_population_avg = equation.population_fitness_avg(population)
        population_avg.append(t_population_avg)
        winner = equation.find_winner(population)
        if winner:
            winning_chromo = winner
            break

    for i, j in zip(population_avg, range(len(population_avg))):
        print "{}: {}".format(j, i)
    print equation.parse_chromo(winning_chromo, True)
