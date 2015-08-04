#!/usr/bin/env python
from neunet import *


class RaceNeuNet(NeuNet):
    """ Neural network for the race game """
    output_layer = None

    def __init__(self, input_ls, weight_ls):
        """ Create the layers, inserting each to the front of the list """
        self.output_layer = NeuNetLayer(2)
        self.input_layer = NeuNetLayer(3, self.output_layer, input_ls, weight_ls)
        self.start_feed_forward(weight_ls)

if __name__ == "__main__":
    ls = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    neunet = RaceNeuNet([1, 2, 3, 4, 1], ls)
    #import pdb; pdb.set_trace()
