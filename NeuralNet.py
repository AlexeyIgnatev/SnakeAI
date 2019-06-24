from Matrix import Matrix
from config import size
from kivy.graphics import Color, Line, Ellipse
from config import x, y, w, h


class NeuralNet:
    def __init__(self, input_nodes, hidden_nodes, output_nodes, hidden_layers):
        self.i_nodes = input_nodes
        self.h_nodes = hidden_nodes
        self.o_nodes = output_nodes
        self.h_layers = hidden_layers

        self.weights = []
        self.weights.append(Matrix(self.h_nodes, self.i_nodes + 1))

        for i in range(1, self.h_layers):
            self.weights.append(Matrix(self.h_nodes, self.h_nodes + 1))

        self.weights.append(Matrix(self.o_nodes, self.h_nodes + 1))

        for w in self.weights:
            w.randomize()

    def mutate(self, mr):
        for w in self.weights:
            w.mutate(mr)

    def output(self, inputs_arr):
        inputs = Matrix.single_column_matrix_from_array(inputs_arr)
        curr_bias = inputs.add_bias()
        for i in range(self.h_layers):
            hidden_ip = self.weights[i].dot(curr_bias)
            hidden_op = hidden_ip.activate()
            curr_bias = hidden_op.add_bias()

        output_ip = self.weights[-1].dot(curr_bias)
        output = output_ip.activate()

        return output.to_array()

    def crossover(self, partner):
        child = NeuralNet(self.i_nodes, self.h_nodes, self.o_nodes, self.h_layers)
        for i in range(len(self.weights)):
            child.weights[i] = self.weights[i].crossover(partner.weights[i])
        return child

    def clone(self):
        clone = NeuralNet(self.i_nodes, self.h_nodes, self.o_nodes, self.h_layers)
        for i in range(len(self.weights)):
            clone.weights[i] = self.weights[i].clone()
        return clone

    def load(self, weights_arr):
        for i in range(len(self.weights)):
            self.weights[i] = weights_arr[i]

    def pull(self):
        model = []
        for i in self.weights:
            model.append(i.clone())
        return model

    def show_nodes(self, vision, decision, canvas):
        space = size / 5
        n_size = (h - (space * (self.i_nodes - 2))) / self.i_nodes
        n_space = (w - (len(self.weights) * n_size)) / len(self.weights)
        h_buff = (h - (space * (self.h_nodes - 1)) - (n_size * self.h_nodes)) / 2
        o_buff = (h - (space * (self.o_nodes - 1)) - (n_size * self.o_nodes)) / 2

        vision = vision[::-1]
        decision = decision[::-1]

        max_index = 0
        for i in range(1, len(decision)):
            if decision[i] > decision[max_index]:
                max_index = i

        lc = 0  # Layer Count
        canvas.clear()
        with canvas:
            # Draw nodes
            for i in range(self.i_nodes):  # Draw inputs
                if vision[i] != 0:
                    Color(1, 1, 0, 1)
                else:
                    Color(1, 1, 1, 1)
                x0 = x
                y0 = y + (i * (n_size + space))
                Ellipse(pos=(x0, y0), size=(n_size, n_size))
            lc += 1

            Color(1, 1, 1, 1)

            for a in range(self.h_layers):  # Draw hidden
                x0 = x + (lc * n_size) + (lc * n_space)
                for i in range(self.h_nodes):
                    y0 = y + h_buff + (i * (n_size + space))
                    Ellipse(pos=(x0, y0), size=(n_size, n_size))
                lc += 1

            x0 = x + (lc * n_size) + (lc * n_space)
            for i in range(self.o_nodes):  # Draw outputs
                if i == max_index:
                    Color(1, 1, 0, 1)
                else:
                    Color(1, 1, 1, 1)
                y0 = y + o_buff + (i * (n_size + space))
                Ellipse(pos=(x0, y0), size=(n_size, n_size))

    def show_weights(self, canvas):
        space = size / 5
        n_size = (h - (space * (self.i_nodes - 2))) / self.i_nodes
        n_space = (w - (len(self.weights) * n_size)) / len(self.weights)
        h_buff = (h - (space * (self.h_nodes - 1)) - (n_size * self.h_nodes)) / 2
        o_buff = (h - (space * (self.o_nodes - 1)) - (n_size * self.o_nodes)) / 2

        lc = 1
        canvas.clear()
        with canvas:
            # Draw weights
            x0 = x + n_size
            y0 = y + n_size / 2
            for i in range(self.weights[0].rows):
                for j in range(self.weights[0].cols - 1):  # Input to hidden
                    if self.weights[0].matrix[i][j] < 0:
                        Color(1, 0, 0, 1)
                    else:
                        Color(0, 0, 1, 1)
                    Line(points=(x0, y0 + j * (n_size + space), x0 + n_space,
                                 y0 + h_buff + i * (space + n_size)))

            lc += 1

            y0 = y + h_buff + (n_size / 2)
            for a in range(1, self.h_layers):
                x0 = x + (lc * n_size) + ((lc - 1) * n_space)
                for i in range(self.weights[a].rows):  # Hidden to hidden
                    for j in range(self.weights[a].cols - 1):
                        if self.weights[a].matrix[i][j] < 0:
                            Color(1, 0, 0, 1)
                        else:
                            Color(0, 0, 1, 1)
                        Line(points=(x0,
                                     y0 + (j * (space + n_size)),
                                     x0 + n_space,
                                     y0 + (i * (space + n_size))))
                lc += 1

            x0 = x + (lc * n_size) + ((lc - 1) * n_space)
            for i in range(self.weights[-1].rows):
                for j in range(self.weights[-1].cols - 1):  # Hidden to output
                    y0 = y + (n_size / 2)
                    if self.weights[-1].matrix[i][j] < 0:
                        Color(1, 0, 0, 1)
                    else:
                        Color(0, 0, 1, 1)
                    Line(points=(x0,
                                 y0 + h_buff + (j * (space + n_size)),
                                 x0 + n_space,
                                 y0 + o_buff + (i * (space + n_size))))
