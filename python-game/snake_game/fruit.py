import random

from pygame.math import Vector2

from config import CELL_NUMBER, CELL_SIZE


class Fruit:
    def __init__(self):
        self.randomize()
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self, pygame, screen, apple):
        # Рисуем фрукт
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        # Рандомное положение
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)
