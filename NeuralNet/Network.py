from NeuralNet.Layer import Layer
from NeuralNet.Options import activation


class Network:
    def __init__(self):
        self.layers = []

    def perceptron_generation(self, nb_input, hidden, nb_output):
        self.layers = []
        previous_neurons = nb_input
        for nb_hidden in hidden:
            layer = Layer()
            layer.populate(nb_hidden, previous_neurons)
            previous_neurons = nb_hidden
            self.layers.append(layer)
        layer = Layer()
        layer.populate(nb_output, previous_neurons)
        self.layers.append(layer)

    def compute(self, inputs):
        out = inputs
        for i in self.layers:
            out = i.dot(out)
            out = [[activation(x[0])] for x in out]
        return out

    def get_save(self):
        data = {
            'neurons': [],
            'weights': []
        }
        data['neurons'].append(len(self.layers[0].neurons[0]))
        for layer in self.layers:
            data['neurons'].append(len(layer.neurons))
            for neuron in layer.neurons:
                for weight in neuron:
                    data['weights'].append(weight)
        return data

    def set_save(self, save):
        previous_neurons = save['neurons'][0]
        index = 0
        self.layers = []
        for i in save['neurons'][1:]:
            layer = Layer()
            layer.create(i, previous_neurons)
            for neuron in layer.neurons:
                for k in range(previous_neurons):
                    neuron[k] = save['weights'][index]
                    index += 1
            previous_neurons = i
            self.layers.append(layer)


# a = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
# n = Network()
# n.perceptron_generation(10, [5, 5], 2)
#