from NeuralNet.Generation import Generation
from NeuralNet.Options import population, network
from NeuralNet.Network import Network


class Generations:
    def __init__(self):
        self.generations = []
        current_generation = Generation()

    def first_generation(self):
        out = []
        for i in range(population):
            nn = Network()
            nn.perceptron_generation(network[0], network[1], network[2])
            out.append(nn.get_save())
        self.generations.append(Generation())
        return out

    def next_generation(self):
        if len(self.generations) == 0:
            return False
        gen = self.generations[-1].generate_next_generation()
        self.generations.append(Generation())
        return gen

    def add_genome(self, genome):
        if len(self.generations) == 0:
            return False
        self.generations[-1].add_genome(genome)