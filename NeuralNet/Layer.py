from numpy import dot, zeros
from NeuralNet.Options import random_clamped


class Layer:
    def __init__(self):
        self.neurons = []

    def dot(self, inputs):
        return dot(self.neurons, inputs)

    def populate(self, nb_neurons, nb_inputs):
        self.create(nb_neurons, nb_inputs)
        self.randomize()

    def create(self, nb_neurons, nb_inputs):
        self.neurons = zeros((nb_neurons, nb_inputs))

    def randomize(self):
        for i in range(len(self.neurons)):
            for j in range(len(self.neurons[0])):
                self.neurons[i][j] = random_clamped()
