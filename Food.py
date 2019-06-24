from config import size
import random
from Vector import Vector
from kivy.graphics import Color, Rectangle


class Food:
    def __init__(self):
        y = size + random.randint(0, 36) * size
        x = size + random.randint(0, 36) * size + 400
        self.pos = Vector(x, y)

    def show(self, canvas):
        canvas.clear()
        with canvas:
            Color(1, 0, 0, 1)
            Rectangle(pos=(self.pos.x, self.pos.y), size=(size, size))

    def clone(self):
        clone = Food()
        clone.pos.x = self.pos.x
        clone.pos.y = self.pos.y
        return clone
