import pygame
import random
import copy
from pygame.locals import *


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.clist = self.cell_list()

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.clist)
            self.update_cell_list()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=False):
        clist = [[0 for i in range(self.cell_width)] for j in range(self.cell_height)]
        if randomize:
            clist = [[random.randint(0, 1) for i in range(self.cell_width)]
                    for j in range(self.cell_height)]
        self.clist = clist
        return self.clist

    def draw_cell_list(self, rects):
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                x = j * self.cell_size + 1
                y = i * self.cell_size + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if rects[i][j]:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, a, b))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, a, b))

    def get_neighbours(self, cell):
        x, y = cell
        n = self.cell_height - 1
        m = self.cell_width - 1
        neighbours = [self.clist[i][j] for i in range(x - 1, x + 2) for j in range(y - 1, y + 2) if
                      (0 <= i <= n) and (0 <= j <= m) and (i != x or j != y)]
        return neighbours

    def update_cell_list(self, cell_list):
        deepcopy = copy.deepcopy(self.clist)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neighbours = sum(self.get_neighbours((i, j)))
                if self.clist[i][j]:
                    if not 1 < neighbours < 4:
                        deepcopy[i][j] = 0
                else:
                    if neighbours == 3:
                        deepcopy[i][j] = 1
        self.clist = deepcopy
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
