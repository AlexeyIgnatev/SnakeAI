import numpy as np
import random
import copy


class Matrix:
    def __init__(self, rows=0, cols=0, matrix=None):
        self.rows = rows
        self.cols = cols
        if matrix is None:
            self.matrix = np.zeros((rows, cols))
        else:
            self.matrix = matrix
            self.rows = len(matrix)
            self.cols = len(matrix[0])

    def output(self, n):
        for i in range(self.rows):
            for j in range(self.cols):
                print(self.matrix[i][j] + ' ')
        print()

    def dot(self, n_matrix):
        result = Matrix(self.rows, n_matrix.cols)
        if self.cols == n_matrix.rows:
            for i in range(self.rows):
                for j in range(n_matrix.cols):
                    summ = 0
                    for k in range(self.cols):
                        summ += self.matrix[i][k] * n_matrix.matrix[k][j]
                    result.matrix[i][j] = summ
        return result

    def randomize(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j] = random.triangular(-1, 1)

    @staticmethod
    def single_column_matrix_from_array(arr):
        n = Matrix(len(arr), 1)
        for i in range(len(arr)):
            n.matrix[i][0] = arr[i]
        return n

    def to_array(self):
        arr = np.zeros(self.rows * self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                arr[j + i * self.cols] = self.matrix[i][j]
        return arr

    def add_bias(self):
        n = Matrix(self.rows + 1, 1)
        for i in range(self.rows):
            n.matrix[i][0] = self.matrix[i][0]
        n.matrix[self.rows][0] = 1
        return n

    def activate(self):
        n = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                n.matrix[i][j] = Matrix.sigmoid(self.matrix[i][j])
        return n

    @staticmethod
    def relu(x):
        return max(0, x)

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def mutate(self, mutation_rate):
        for i in range(self.rows):
            for j in range(self.cols):
                rand = random.random()

                if rand < mutation_rate:
                    self.matrix[i][j] += random.triangular(-1, 1)
                    if self.matrix[i][j] > 1:
                        self.matrix[i][j] = 1
                    elif self.matrix[i][j] < -1:
                        self.matrix[i][j] = -1

    def crossover(self, partner):
        child = Matrix(self.rows, self.cols)

        rand_c = random.randint(0, self.cols - 1)
        rand_r = random.randint(0, self.rows - 1)

        for i in range(self.rows):
            for j in range(self.cols):
                if (i < rand_r) or (i == rand_r and j <= rand_c):
                    child.matrix[i][j] = self.matrix[i][j]
                else:
                    child.matrix[i][j] = partner.matrix[i][j]
        return child

    def clone(self):
        clone = Matrix(self.rows, self.cols)
        clone.matrix = copy.deepcopy(self.matrix)
        return clone
