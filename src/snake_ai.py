#!/usr/bin/env python3

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

import random
import copy

from graph import canvas
from search import a_star as a_path_search, dfs as dfs_path_search, tools
from search.queue import PriorityQueue

TOTAL = canvas.WIDTH * canvas.HEIGHT
HALF = int(TOTAL / 2)


def valid_coord(coord, coords):
    """
    验证坐标是否可用
    :param coord:   待验证的坐标
    :param coords:  坐标不能出现在此组内
    :return:        True | False
    """
    (x, y) = coord
    if x < 0 or x >= canvas.WIDTH:
        return False
    if y < 0 or y >= canvas.HEIGHT:
        return False

    for _coord in coords:
        (_x, _y) = _coord
        if x == _x and y == _y:
            return False
    return True


def get_apple_coord(snake_coords):
    """
    生成apple
    :param snake_coords:    snake坐标
    :return:                apple坐标
    """
    apple = (random.randint(0, canvas.WIDTH - 1), random.randint(0, canvas.HEIGHT - 1))
    while not valid_coord(apple, snake_coords):
        apple = (random.randint(0, canvas.WIDTH - 1), random.randint(0, canvas.HEIGHT - 1))
    return apple


def move(snake_coords, n_coord, apple, draw=False):
    """
    移动一个格子
    :param snake_coords:    snake_coords
    :param n_coord:         移动到此格子
    :param apple:           apple
    :param draw:            是否更新canvas
    """

    snake_coords.insert(0, n_coord)
    tail = None
    if not tools.cell_equal(n_coord, apple):
        score = 0
        tail = snake_coords.pop()
    else:
        score = 1

    if draw:
        if tail:
            canvas.draw_cells([tail, apple], canvas.COLOR.BG_COLOR.value)
        canvas.draw_cell_line(snake_coords, canvas.COLOR.DARK_GRAY.value, canvas.COLOR.DARK_GREEN.value)

    return score


def virtual_run(snake_coords, apple, path):
    """
    尝试去吃apple，判断吃完apple后是否还能找到tail
    :param snake_coords:    snake
    :param apple:           apple
    :param path:            path
    :return:                True | False
    """
    _snake_coords = copy.deepcopy(snake_coords)
    _apple = copy.deepcopy(apple)
    _path = copy.deepcopy(path)

    # 去吃apple
    for _n_coord in _path:
        move(_snake_coords, _n_coord, _apple)

    if len(_snake_coords) == TOTAL:
        # 吃完苹果就win了
        return True

    # 寻找head到tail的路径
    __path = a_path_search.cal(_snake_coords[0], _snake_coords[-1], _snake_coords[:-1])  # 移动时tail会腾出空间

    # 吃完apple后还能找到tail，则为True
    return __path is not None


def wander(snake_coords, apple):
    (a_x, a_y) = apple

    adjs = tools.adj(snake_coords[0], obstacles=snake_coords[:-1])  # 移动时tail会腾出空间
    queue = PriorityQueue()

    for adj in adjs:
        (x, y) = adj
        g = abs(a_x - x) + abs(a_y - y)  # adj到apple的距离

        path = dfs_path_search.cal(adj, snake_coords[-2], [adj] + snake_coords[:-2])  # 移动时tail会腾出空间
        if path:  # 移动到adj后还能找到蛇尾
            h = len(path)
        else:  # 移动到adj后就找不到蛇尾了
            h = 0

        queue.put(adj, (-h, -g))  # 如果能找到tail则找tail，否则随便走走

    return queue.get()


def next_coord(snake_coords, apple):
    """
    计算下一个坐标
    :param snake_coords:    snake_coords
    :param apple:           apple
    :return:                下一个坐标
    """
    # 搜索head到apple的路径
    if len(snake_coords) < HALF:
        path = a_path_search.cal(snake_coords[0], apple, snake_coords[:-1])  # 移动时tail会腾出空间
    else:
        path = dfs_path_search.cal(snake_coords[0], apple, snake_coords[:-1])

    if path:
        # 可以吃到apple
        if virtual_run(snake_coords, apple, path):
            # 吃完apple后还可以找到tail
            return path[0]  # 走起
        else:
            # 吃完apple后就进了死胡同
            return wander(snake_coords, apple)
    else:
        # 吃不到apple
        return wander(snake_coords, apple)


def run_game():
    snake_coords = [(1, 2), (1, 1)]
    apple = get_apple_coord(snake_coords)
    score = 0

    canvas.draw_bg()
    canvas.draw_grid()
    canvas.draw_cell_line(snake_coords, canvas.COLOR.DARK_GRAY.value, canvas.COLOR.DARK_GREEN.value)
    canvas.draw_cell(apple, canvas.COLOR.RED.value)
    canvas.update()

    while True:
        n_coord = next_coord(snake_coords, apple)
        if not n_coord:
            print("Game Over! STUCK")
            return

        score += move(snake_coords, n_coord, apple, draw=True)

        if not valid_coord(snake_coords[0], snake_coords[1:]):
            print("Game Over!")
            valid_coord(snake_coords[0], snake_coords[1:])
            return
        if len(snake_coords) == TOTAL:
            print("Game KO!")
            canvas.draw_grid()
            return
        if tools.cell_equal(n_coord, apple):
            apple = get_apple_coord(snake_coords)

        canvas.draw_cell(apple, canvas.COLOR.RED.value)
        canvas.draw_grid()


def main():
    global TOTAL, HALF

    canvas.init("Game_Snake_AI", 15, 13)
    canvas.draw_grid()
    canvas.update()

    TOTAL = canvas.WIDTH * canvas.HEIGHT
    HALF = int(TOTAL / 2)

    input("Press <Enter> to start!")
    run_game()
    input("Press <Enter> to close!")


if __name__ == "__main__":
    main()
