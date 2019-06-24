from Snake import Snake
import random
from evolution_graph import scores
from config import fps
from time import sleep, time


class Population:
    def __init__(self, size):
        self.snakes = []
        for i in range(size):
            self.snakes.append(Snake())
        self.best_snake = self.snakes[0]
        self.score = 0
        self.high_score = 0
        self.best_fitness = 0
        self.gen = 1
        self.mutation_rate = 0.05
        self.sleep_rate = 1 / fps
        self.live_snakes = 0

    def update(self):  # update all the snakes in the generation
        for i in self.snakes:
            if not i.dead:
                i.look()
                i.think()
                i.move()
                self.live_snakes += 1

    def update_score(self, score, score_text):
        if score != self.best_snake.score:
            score = self.best_snake.score
            score_text.text = 'Score: {}'.format(score)

    def update_high_score(self, high_score, high_score_text):
        if high_score > self.high_score:
            self.high_score = high_score
            high_score_text.text = 'High score: {}'.format(high_score)

    def update_gen(self, gen_text):
        gen_text.text = 'Generation: {}'.format(self.gen)

    def evolution(self, canvas_weights, canvas_nodes, canvas_shake, canvas_food, gen_text, score_text, high_score_text):
        while True:
            self.best_snake.brain.show_weights(canvas_weights)
            while True:
                t0 = time()
                self.live_snakes = 0
                self.update()
                self.best_snake.show(canvas_shake)
                self.best_snake.food.show(canvas_food)
                self.best_snake.brain.show_nodes(self.best_snake.vision, self.best_snake.decision, canvas_nodes)
                print(self.best_snake.decision)
                self.update_score(self.score, score_text)
                if self.live_snakes <= 1 and self.best_snake.dead:
                    self.natural_selection()
                    self.update_high_score(self.score, high_score_text)
                    self.score = 3
                    self.update_gen(gen_text)
                    break
                else:
                    t0 = self.sleep_rate - (time() - t0)
                    if t0 > 0:
                        sleep(t0)

    def set_best_snake(self):
        _max = 0
        max_index = 0
        for i in range(len(self.snakes)):
            if self.snakes[i].fitness > _max:
                _max = self.snakes[i].fitness
                max_index = i
        if _max > self.best_fitness:
            self.best_fitness = _max
            self.best_snake = self.snakes[max_index].clone()
        else:
            self.best_snake = self.best_snake.clone()

    def select_parent(self):
        return random.choice(self.snakes)

    def natural_selection(self):
        self.calculate_fitness()
        self.set_best_snake()

        new_snakes = [self.best_snake]

        for i in range(len(self.snakes) - 1):
            child = self.select_parent().crossover(self.select_parent())
            child.mutate(self.mutation_rate)
            new_snakes.append(child)
        del self.snakes
        self.snakes = new_snakes
        scores.append(self.score)
        self.score = 3
        self.gen += 1

    def mutate(self):
        for i in self.snakes[1:]:
            i.mutate(self.mutation_rate)

    def calculate_fitness(self):
        for i in self.snakes:
            i.calculate_fitness()
