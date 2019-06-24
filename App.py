from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from evolution_graph import show

from Population import Population

from kivy.graphics import Color, Line
from threading import Thread

from config import x, y, w, h, size

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 1200)
Config.set('graphics', 'height', 800)


class PainterWidget(Widget):
    pass


class SnakeAIApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mutation_text = Label(text='Mutation rate: 5%', pos=(155, 640), color=(.5, .5, .5, 1), font_size=20,
                                   font_family='tahoma')
        self.gen_text = Label(text='Generation: 1', pos=(135, 670), color=(.5, .5, .5, 1), font_size=20,
                              font_family='tahoma')
        self.score_text = Label(text='Score: 0', pos=(120, 30), color=(.5, .5, .5, 1), font_size=20,
                                font_family='tahoma')
        self.high_score_text = Label(text='High score: 0', pos=(140, 0), color=(.5, .5, .5, 1), font_size=20,
                                     font_family='tahoma')
        self.nodes_widget = Widget()
        self.weights_widget = Widget()
        self.snake_widget = Widget()
        self.food_widget = Widget()
        self.nodes_widget.size = (1200, 800)
        self.weights_widget.size = (1200, 800)
        self.snake_widget.size = (1200, 800)
        self.food_widget.size = (1200, 800)

        self.pop = Population(200)

    def build(self):
        parent = Widget()
        parent.add_widget(Button(text='Graph', on_press=show, size=(100, 35), pos=(299, 765)))
        parent.add_widget(Button(text='Load', on_press=self.load, size=(100, 35), pos=(199, 765)))
        parent.add_widget(Button(text='Save', on_press=self.save, size=(100, 35), pos=(99, 765)))
        parent.add_widget(Button(text='+', on_press=self.i_mut, size=(20, 20), pos=(340, 700)))
        parent.add_widget(Button(text='-', on_press=self.d_mut, size=(20, 20), pos=(365, 700)))
        parent.add_widget(Label(text='RED < 0', pos=(105, 70), color=(1, 0, 0, 1), font_size=18, font_family='tahoma'))
        parent.add_widget(
            Label(text='BLUE > 0', pos=(210, 70), color=(0, 0, 1, 1), font_size=18, font_family='tahoma'))
        parent.add_widget(self.gen_text)
        parent.add_widget(self.mutation_text)
        parent.add_widget(self.score_text)
        parent.add_widget(self.high_score_text)
        parent.add_widget(self.nodes_widget)
        parent.add_widget(self.weights_widget)
        parent.add_widget(self.snake_widget)
        parent.add_widget(self.food_widget)
        with parent.canvas:
            Color(1, 1, 1, 1)
            Line(points=(400, 0, 400, 800))
            Line(points=(420, 20, 420, 780))
            Line(points=(420, 20, 1180, 20))
            Line(points=(1180, 20, 1180, 780))
            Line(points=(420, 780, 1180, 780))

        space = size / 5
        n_size = (h - (space * (self.pop.best_snake.brain.i_nodes - 2))) / self.pop.best_snake.brain.i_nodes
        n_space = (w - (len(self.pop.best_snake.brain.weights) * n_size)) / len(self.pop.best_snake.brain.weights)
        o_buff = (h - (space * (self.pop.best_snake.brain.o_nodes - 1)) - (
                n_size * self.pop.best_snake.brain.o_nodes)) / 2

        lc = 1

        for a in range(self.pop.best_snake.brain.h_layers):
            lc += 1
        x0 = x + (lc * (n_size + n_space)) + (n_size / 2) - 49
        y0 = y + o_buff + (n_size / 2) - 51
        parent.add_widget(
            Label(text='U', pos=(x0, y0 + 3 * (space + n_size)), color=(0, 0, 0, 1), font_size=18, font_family='tahoma',
                  bold=True))
        parent.add_widget(
            Label(text='D', pos=(x0, y0 + 2 * (space + n_size)), color=(0, 0, 0, 1), font_size=18, font_family='tahoma',
                  bold=True))
        parent.add_widget(
            Label(text='L', pos=(x0, y0 + 1 * (space + n_size)), color=(0, 0, 0, 1), font_size=18, font_family='tahoma',
                  bold=True))
        parent.add_widget(
            Label(text='R', pos=(x0, y0), color=(0, 0, 0, 1), font_size=18, font_family='tahoma', bold=True))

        thread = Thread(target=self.pop.evolution, args=(
            self.weights_widget.canvas, self.nodes_widget.canvas, self.snake_widget.canvas, self.food_widget.canvas,
            self.gen_text, self.score_text, self.high_score_text))

        thread.start()

        return parent

    def load(self, instance):
        pass

    def save(self, instance):
        pass

    def i_mut(self, instance):
        self.pop.mutation_rate *= 2
        if self.pop.mutation_rate > 1:
            self.pop.mutation_rate = 1
        self.mutation_text.text = 'Mutation rate: {:.0%}'.format(self.pop.mutation_rate)

    def d_mut(self, instance):
        self.pop.mutation_rate /= 2
        if self.pop.mutation_rate < 0.01:
            self.pop.mutation_rate = 0.01
        self.mutation_text.text = 'Mutation rate: {:.0%}'.format(self.pop.mutation_rate)


if __name__ == '__main__':
    SnakeAIApp().run()
