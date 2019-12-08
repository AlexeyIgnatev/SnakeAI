from math import exp
from random import triangular


# Функция активации сигмоида
def activation(x):
    return 1 / (1 + exp(-x))


# Функция генерации рандомных значений между 1 и -1
def random_clamped():
    return triangular(-1, 1)


# Структура сети Перцептрон (1 скрытый слой)
network = [1, [1], 1]

# Популяция в поколении
population = 50

# Доля сохранения лучших сетей без изменения для следующего поколения
elitism = 0.2

# Доля создания новых случайных сетей
random_behaviour = 0.2

# Скорость мутации на весах синапсов
mutation_rate = 0.1

# Интервал мутационных изменений на весе синапса
mutation_range = 0.5

# Сохранение последних поколений
historic = 0

# Только сохранить счет (не сеть)
low_historic = False

# Количество детей
nb_child = 1
