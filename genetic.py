import operator
import string
import random
import __future__

target_num = 88
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
def parse_input(input_str):
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

def parse_chrom(chrom):
    ret = ""
    for i in range(0, len(chrom), 4):
        ret += gene_table[chrom[i:i+4]]
    return ret

def generate_chrom():
    ret = ""
    for _ in range(20):
        ret += str(random.randrange(2))
    return ret

print "Result: {}\n".format(parse_input(parse_chrom(generate_chrom())))
