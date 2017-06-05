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

from search.queue import PriorityQueue
from graph import canvas
from search import tools


def cal(start, end, obstacles=[], show_details=False):
    """
    使用A*算法搜索路径
    :param start:        起点
    :param end:          终点
    :param obstacles:    障碍
    :param show_details: 是否显示细节
    :return:             返回路径
    """
    if tools.cell_equal(start, end):
        return []

    queue = PriorityQueue()
    start_node = Node(start, 0, Node.cal_h(start, end))
    queue.put(start_node, start_node.f)
    mark = {tools.cal_cell_id(start): None}

    while not queue.empty():
        node = queue.get()

        adjs = tools.adj(node.cell, mark, obstacles)
        for adj in adjs:
            if tools.cal_cell_id(adj) in mark.keys():
                continue

            mark[tools.cal_cell_id(adj)] = node.cell

            adj_node = Node(adj, node.g + 1, Node.cal_h(adj, end))
            queue.put(adj_node, adj_node.f)

            if tools.cell_equal(adj, end):
                path = tools.cal_path(mark, tools.cal_cell_id(adj))
                return path[1:]

            if show_details:
                canvas.draw_cell(adj, canvas.COLOR.DARK_GREEN.value)
                canvas.update()

    return []


class Node:
    def __init__(self, cell, g, h):
        self._cell = cell
        self._g = g  # start走到cell的距离
        self._h = h  # cell到end的距离
        self._f = g + h

    @property
    def cell(self):
        return self._cell

    @property
    def f(self):
        return self._f

    @property
    def g(self):
        return self._g

    @staticmethod
    def cal_h(cell1, cell2):
        (x1, y1) = cell1
        (x2, y2) = cell2
        return abs(x1 - x2) + abs(y1 - y2)
