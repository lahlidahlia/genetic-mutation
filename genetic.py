import operator
import string
import random
import __future__

TARGET_NUMBER = 88
CROSS_OVER_RATE = 0.7
MUTATION_RATE = 0.1
POPULATION = 20

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
def parse_chrom(chrom):
    input_str = chrom_to_string(chrom)
    operators = ['+', '-', '*', '/']
    #State of characters sequence needs to alternate
    is_state_number = True
    filtered_string = ""
    print "Input: " + input_str
    for i in input_str:
        if is_state_number and i in string.digits:
            filtered_string += i
            is_state_number = not is_state_number
        elif not is_state_number and i in operators:
            filtered_string += i
            is_state_number = not is_state_number
    #Remove the last character if not digit
    if filtered_string[-1:] not in string.digits:
        filtered_string = filtered_string[:-1]
    print "Filtered: " + filtered_string
    #All the compile stuffs is to make sure it eval the digits as if they were float, otherwise, just a normal eval function
    return eval(compile(filtered_string, '<string>', 'eval', __future__.division.compiler_flag))

def chrom_to_string(chrom):
    ret = ""
    for i in range(0, len(chrom), 4):
        ret += gene_table[chrom[i:i+4]]
    return ret

def generate_chrom():
    ret = ""
    for _ in range(20):
        ret += str(random.randrange(2))
    return ret

def cross_over(chrom_1, chrom_2, rate):
    #cross 2 chromosomes over, dependant on rate
    if(random.random() < rate):
        pos = random.randrange(20)
        t1 = chrom_1[pos:]
        t2 = chrom_2[pos:]
        chrom_1 = chrom_1[:pos] + t2
        chrom_2 = chrom_2[:pos] + t1
        return (chrom_1, chrom_2)

def mutate(chrom, rate):
    #Each bit in the chrom has a chance to flip its bit
    ret = ""
    for bit in chrom:
        if(random.random() < rate):
            ret += "1" if bit == "0" else "0"
        else:
            ret += bit
    return ret

def produce_offspring(chrom_1, chrom_2):
    print "1: {}. 2: {}".format(chrom_1, chrom_2)
    offspring_1, offspring_2 = cross_over(chrom_1, chrom_2, CROSS_OVER_RATE)
    offspring_1 = mutate(offspring_1, MUTATION_RATE)
    offspring_2 = mutate(offspring_2, MUTATION_RATE)
    print "1: {}. 2: {}".format(offspring_1, offspring_2)

    return (offspring_1, offspring_2)

def get_fitness_score(chrom):
    result = parse_chrom(chrom)
    if(result == TARGET_NUMBER):
        return True
    else:
        return 1 / (TARGET_NUMBER - result)

def choose_randomly(probability_dict):
    #dict should follow the format: {item1: prob, item2: prob}
    prob_sum = 0
    for v in probability_dict.values():
        prob_sum += v
    r = random.randrange(prob_sum)
    sum_so_far = 0
    for k, v in probability_dict.iteritems():
        sum_so_far += v
        if(r < sum_so_far):
            return k


#if __name__ == "__main__":
#    #{chromosome: fitness_score}
#    population = {}
#    for i in range(POPULATION):
#        chrom = generate_chrom()
#        population[chrom] = fi
#
#    for chrom in population:
#        
