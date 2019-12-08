from NeuralNet.Generations import Generations
from NeuralNet.Network import Network
import NeuralNet.Options as Options
from NeuralNet.Genome import Genome


class NeuralNet:
    def __init__(self):
        self.generations = Generations()

    def restart(self):
        self.generations = Generations()

    def next_generation(self):
        networks = []
        if len(self.generations.generations) == 0:
            networks = self.generations.first_generation()
        else:
            networks = self.generations.next_generation()

        nns = []
        for i in networks:
            nn = Network()
            nn.set_save(i)
            nns.append(nn)

        if Options.low_historic:
            if len(self.generations.generations >= 2):
                for i in self.generations.generations[-2].genomes:
                    del i['network']
        if Options.historic != -1:
            # даление старых поколений
            if len(self.generations.generations) > Options.historic + 1:
                for i in range(len(self.generations.generations) - (Options.historic + 1)):
                    self.generations.generations.pop(0)
        return nns

    def network_score(self, network, score):
        self.generations.add_genome(Genome(score, network.get_save()))
