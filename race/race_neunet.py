#!/usr/bin/env python
from neunet import *


class RaceNeuNet(NeuNet):
    """ Neural network for the race game """
    output_layer = None

    def __init__(self, input_size, weight_ls):
        """ Create the layers, inserting each to the front of the list """
        self.output_layer = NeuNetLayer(2)
        self.input_layer = NeuNetLayer(3, self.output_layer, weight_ls, input_size)

if __name__ == "__main__":
    ls = []
    #ls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    for _ in range(23):
        ls.append(1)
    neunet = RaceNeuNet(5, ls)
    print neunet.start([0, 0, 0, 0, 1])
    #import pdb; pdb.set_trace()
