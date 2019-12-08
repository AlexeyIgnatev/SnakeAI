from copy import deepcopy
from random import random
import NeuralNet.Options as Options


class Generation:
    def __init__(self):
        self.genomes = []

    def add_genome(self, genome):
        i = 0
        for i in range(len(self.genomes)):
            if genome.score > self.genomes[i].score:
                break
        self.genomes.insert(i, genome)

    @staticmethod
    def breed(g1, g2, nb_child):
        """
        Скрещивание геномов для создания детей
        """
        data = []
        for nb in range(nb_child):
            child = deepcopy(g1)
            for i in range(len(g2.network['weights'])):
                # Скрещивание геномов
                if random() <= 0.5:
                    child.network['weights'] = g2.network['weights']
            # Выполнение мутации на некоторых весах
            for i in range(len(child.network['weights'])):
                if random() <= Options.mutation_rate:
                    child.network['weights'][i] += random() * Options.mutation_range * 2 - Options.mutation_range
            data.append(child)
        return data

    def generate_next_generation(self):
        next_gen = []

        for i in range(round(Options.elitism * Options.population)):
            if len(next_gen) < Options.population:
                next_gen.append(deepcopy(self.genomes[i]['network']))

        for i in range(round(Options.random_behaviour * Options.population)):
            n = deepcopy(self.genomes[0]['network'])
            for k in range(len(n['weights'])):
                n['weights'][k] = Options.random_clamped()
            if len(next_gen) < Options.population:
                next_gen.append(n)

        max_index = 0
        while True:
            for i in range(max_index):
                child = self.breed(self.genomes[i], self.genomes[max_index], Options.nb_child)
                for c in child:
                    next_gen.append(c.network)
                    if len(next_gen) >= Options.population:
                        return next_gen
            max_index += 1
            if max_index > len(self.genomes) - 1:
                max_index = 0