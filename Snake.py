from config import window_size, size
from Vector import Vector
from Food import Food
from NeuralNet import NeuralNet
from config import hidden_nodes, hidden_layers
import numpy as np

from kivy.graphics import Color, Rectangle


class Snake:
    def __init__(self):
        self.body = []  # snakes body
        self.vision = []
        self.decision = []
        self.head = Vector(800, 800 / 2)
        self.body.append(Vector(800, window_size[1] / 2 - size))
        self.body.append(Vector(800, window_size[1] / 2 - size * 2))
        self.prev_pos = Vector(800, window_size[1] / 2 - size * 3)
        self.score = 3
        self.life_left = 200  # amount of moves the snake can make before it dies
        self.life_time = 0  # amount of time the snake has been alive
        self.x_vel = 0
        self.y_vel = size
        self.fitness = 0
        self.dead = False

        self.food = Food()
        while self.body_collide(self.food.pos.x, self.food.pos.y) or (
                self.food.pos.x == self.head.x and self.food.pos.y == self.head.y):
            self.food = Food()
        self.brain = NeuralNet(24, hidden_nodes, 4, hidden_layers)

    def body_collide(self, x, y):  # check if a position collides with the snakes body
        for i in self.body:
            if x == i.x and y == i.y:
                return True
        return False

    def food_collide(self, x, y):  # check if a position collides with the food
        return x == self.food.pos.x and y == self.food.pos.y

    @staticmethod
    def wall_collide(x, y):  # check if a position collides with the wall
        return x >= window_size[0] - size or x < window_size[0] / 3 + size or y >= window_size[
            1] - size or y < size

    def show(self, canvas_snake):  # show the snake
        canvas_snake.clear()
        with canvas_snake:
            Color(1, 1, 1, 1)
            for i in self.body:
                Rectangle(pos=(i.x, i.y), size=(size, size))
            if self.dead:
                Color(.5, .5, .5, 1)
            Rectangle(pos=(self.head.x, self.head.y), size=(size, size))

    def move(self):  # move the snake
        if not self.dead:
            self.life_left -= 1
            self.life_time += 1

            if self.food_collide(self.head.x, self.head.y):
                self.eat()
            self.shift_body()

            if self.wall_collide(self.head.x, self.head.y) or self.body_collide(self.head.x,
                                                                                self.head.y) or self.life_left <= 0:
                self.dead = True

    def eat(self):  # eat food
        self.score += 1
        if self.life_left > 400:
            self.life_left = 500
        else:
            self.life_left += 100
        self.body.append(self.prev_pos)
        self.food = Food()
        while self.body_collide(self.food.pos.x, self.food.pos.y) or (
                self.food.pos.x == self.head.x and self.food.pos.y == self.head.y):
            self.food = Food()

    def shift_body(self):  # shift the body to follow the head
        self.prev_pos = self.body[-1]
        self.body = [self.head.clone()] + self.body[:-1]
        vel = Vector(self.x_vel, self.y_vel)
        self.head.add(vel)

    def clone(self):  # clone the snake
        clone = Snake()
        clone.brain = self.brain.clone()
        return clone

    def crossover(self, partner):  # crossover the snake with another snake
        child = Snake()
        child.brain = self.brain.crossover(partner.brain)
        return child

    def calculate_fitness(self):  # calculate the fitness of the snake
        fitness = np.floor(self.life_time ** 2)
        fitness *= 2 ** self.score
        if self.score >= 10:
            fitness *= self.score - 9
        self.fitness = fitness

    def mutate(self, mutation_rate):  # mutate the snakes brain
        self.brain.mutate(mutation_rate)

    def look(self):  # look in all 8 directions and check for food, body and wall
        self.vision = []
        temp = self.look_in_direction(Vector(-size, 0))
        self.vision.extend(temp)
        temp = self.look_in_direction(Vector(-size, -size))
        self.vision.extend(temp)
        temp = self.look_in_direction(Vector(0, -size))
        self.vision.extend(temp)
        temp = self.look_in_direction(Vector(size, -size))
        self.vision.extend(temp)
        temp = self.look_in_direction(Vector(size, 0))
        self.vision.extend(temp)
        temp = self.look_in_direction(Vector(size, size))
        self.vision.extend(temp)
        temp = self.look_in_direction(Vector(0, size))
        self.vision.extend(temp)
        temp = self.look_in_direction(Vector(-size, size))
        self.vision.extend(temp)

    def look_in_direction(self, direction: Vector):
        look = [0.0] * 3
        pos = Vector(self.head.x, self.head.y)
        distance = 0
        food_found = False
        body_found = False
        pos.add(direction)
        distance += 1
        while not self.wall_collide(pos.x, pos.y):
            if not food_found and self.food_collide(pos.x, pos.y):
                look[0] = 1
                food_found = True
            if not body_found and self.body_collide(pos.x, pos.y):
                look[1] = 1
                body_found = True
            pos.add(direction)
            distance += 1
        look[2] = 1 / distance
        return look

    def think(self):
        self.decision = self.brain.output(self.vision)
        _max = 0
        max_index = 0
        for i in range(4):
            if self.decision[i] > _max:
                _max = self.decision[i]
                max_index = i

        if max_index == 0:
            self.move_up()
        elif max_index == 1:
            self.move_down()
        elif max_index == 2:
            self.move_left()
        else:
            self.move_right()

    def move_up(self):
        if self.y_vel != -size:
            self.y_vel = size
            self.x_vel = 0
        else:
            self.dead = True

    def move_down(self):
        if self.y_vel != size:
            self.y_vel = -size
            self.x_vel = 0
        else:
            self.dead = True

    def move_left(self):
        if self.x_vel != size:
            self.x_vel = - size
            self.y_vel = 0
        else:
            self.dead = True

    def move_right(self):
        if self.x_vel != -size:
            self.x_vel = size
            self.y_vel = 0
        else:
            self.dead = True
