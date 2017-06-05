"""
Copyright 2017 ManerFan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import pygame
from enum import Enum

WIDTH = 24
HEIGHT = 18
CELL_SIZE = 40
WINDOW_WIDTH = WIDTH * CELL_SIZE
WINDOW_HEIGHT = HEIGHT * CELL_SIZE

screen = None


class COLOR(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARK_GREEN = (0, 155, 0)
    DARK_GRAY = (40, 40, 40)
    BG_COLOR = (0, 0, 0)


def init(title):
    """
    初始化画布
    """
    global screen
    pygame.init()
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def update():
    pygame.display.update()


def draw_grid():
    """
    在画布上绘制grid方格
    """
    screen.fill(COLOR.BG_COLOR.value)

    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, COLOR.DARK_GRAY.value, (x, 0), (x, WINDOW_HEIGHT))

    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, COLOR.DARK_GRAY.value, (0, y), (WINDOW_WIDTH, y))

    update()


def draw_cell_line(cells, cell_color=COLOR.GREEN.value, line_color=COLOR.DARK_GREEN.value):
    """
    绘制像素点，并使用直线将像素点连接
    :param cells:           像素点
    :param cell_color:      像素点颜色
    :param line_color:      线条颜色
    :return: 
    """
    draw_cells(cells, cell_color)

    for i in range(1, len(cells)):
        (x1, y1) = cells[i - 1]
        (x2, y2) = cells[i]
        pygame.draw.line(screen, line_color,
                         ((x1 + .5) * CELL_SIZE, (y1 + .5) * CELL_SIZE),
                         ((x2 + .5) * CELL_SIZE, (y2 + .5) * CELL_SIZE),
                         4)


def draw_cells(cells, color=COLOR.GREEN.value):
    """
    绘制像素点
    :param cells:   像素点 
    :param color:   颜色
    """
    for cell in cells:
        draw_cell(cell, color)


def draw_cell(cell, color=COLOR.GREEN.value):
    """
    绘制一个像素点
    :param cell:    像素点位置 
    :param color:   像素点颜色
    """
    (x, y) = cell
    x = x * CELL_SIZE
    y = y * CELL_SIZE

    outer_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    padding_rect = pygame.Rect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
    inner_rect = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)

    pygame.draw.rect(screen, color, outer_rect)
    pygame.draw.rect(screen, COLOR.BG_COLOR.value, padding_rect)
    pygame.draw.rect(screen, color, inner_rect)
