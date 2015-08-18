#!/usr/bin/env python
from neunet import *


class RaceNeuNet(NeuNet):
    """ Neural network for the race game """
    output_layer = None

    def __init__(self, input_size, weight_ls):
        """ Create the layers, inserting each to the front of the list """
        super(RaceNeuNet, self).__init__(input_size, weight_ls)
        self.output_layer = NeuNetLayer(2)
        self.first_hidden_layer = NeuNetLayer(3, self.output_layer, weight_ls, input_size)

if __name__ == "__main__":
    ls = []
    for _ in range(23):
        ls.append(1)
    neunet = RaceNeuNet(4, ls)
    print neunet.start([0, 0, 0, 0])
