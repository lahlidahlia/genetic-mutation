#!/usr/bin/env python


class Neuron:
    """ Defines a single neuron of a neural network """

    inputs = []  # Bias is always last
    weights = []  # Bias is always last

    def __init__(self, input_ls, layer):
        """ Layer defines which layer this neuron belongs to """
        self.inputs = input_ls
        layer.neurons.append(self)

    def feed_forward(self):
        """ Calculates the result and returns the activation """
        result = 0
        for i, w in zip(self.inputs, self.weights):
            result += i * w
        return self.activate(result)

    def activate(self, result):
        return result > 0


class NeuNetLayer:
    """ Defines a layer of a neural network """

    neurons = []
    next_layer = None

    def __init__(self, next_layer):
        self.next_layer = next_layer

    def feed_forward(self):
        """ Feeds the layer's inputs to the next layer's neurons """
        for next_neuron in self.next_layer:
            next_neuron.inputs = []
            for neuron in self.neurons:
                next_neuron.inputs.append(neuron.feed_forward())
            next_neuron.inputs.append(1)  # Bias
