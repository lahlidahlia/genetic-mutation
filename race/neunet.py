#!/usr/bin/env python
import abc
import random
import math

def sigmoid(x):
    return 1/(1 + math.exp(-x))


class Neuron:
    """ Defines a single neuron of a neural network """

    def __init__(self, input_ls, layer):
        """ Layer defines which layer this neuron belongs to """
        self.inputs = input_ls
        self.weights = []  # Bias is always last
        for _ in range(len(self.inputs)):
            self.weights.append(random.random()*2-1)

    def feed_forward(self):
        """ Calculates the result and returns the activation """
        result = 0
        print "weights: {}".format(self.weights)
        print "inputs: {}".format(self.inputs)
        for i, w in zip(self.inputs, self.weights):
            result += i * w
        print "result: {}".format(result)
        return self.activate(result)

    def activate(self, x):
        return sigmoid(x)


class NeuNetLayer:
    """ Defines a layer of a neural network """

    def __init__(self, amount, next_layer=None, input_ls=[], weight_ls=[]):
        """ Create a neural network layer with the specified
            amount of neurons. If input_ls is given, give each
            neurons the input list. If next_layer is not given,
            the layer will be treated as an output layer and
            will return each neuron's value with feed_forward"""
        # Next layer is the layer to be fed forward to
        self.neurons = []
        self.next_layer = next_layer
        for _ in range(amount):
            neuron = Neuron(input_ls, self)
            self.neurons.append(neuron)
            if weight_ls:
                for _ in range(len(input_ls)-1):
                    neuron.weights.append(weight_ls.pop())

    def feed_forward(self, weight_ls):
        """ Feeds the layer's inputs to the next layer's neurons
            If layer is an output layer, return the output of each
            neurons as a list """
        if not self.next_layer:
            ret_ls = []
            for neuron in self.neurons:
                ret_ls.append(neuron.feed_forward())
                print "{}: {}".format("input list", neuron.inputs)
                print neuron.feed_forward()
            return ret_ls

        # If not output
        for next_neuron in self.next_layer.neurons:
            next_neuron.inputs = []
            for neuron in self.neurons:
                next_neuron.inputs.append(neuron.feed_forward())
                next_neuron.weights.append(weight_ls.pop())
                print "weight_ls: {}".format((weight_ls))
            next_neuron.inputs.append(1)  # Bias
            #print next_neuron.inputs
        return self.next_layer.feed_forward(weight_ls)


class NeuNet:
    """ Defines a whole meural network
        Probably should define your own NeuNet """

    __metaclass__ = abc.ABCMeta

    # Actually the first hidden layer,
    # as input layer immediately feed into that
    input_layer = None

    @abc.abstractmethod
    def __init__(self, input_ls):
        """ Create the whole neural network here
            Go make your own! """
        return

    def start_feed_forward(self, weight_ls):
        print self.input_layer.feed_forward(weight_ls)

