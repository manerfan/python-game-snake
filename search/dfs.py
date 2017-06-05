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

from queue import LifoQueue
from graph import canvas
from search import tools


def cal(start, end, obstacles=[], show_details=False):
    """
    使用DFS算法搜索路径
    :param start:        起点
    :param end:          终点
    :param obstacles:    障碍
    :param show_details: 是否显示细节
    :return:             返回路径
    """
    if tools.cell_equal(start, end):
        return [start]

    queue = LifoQueue()
    mark = {}

    queue.put(Node(start))

    while not queue.empty():
        node = queue.get()
        cell = node.cell
        parent = node.parent

        if tools.cal_cell_id(cell) in mark.keys():
            # 已经遍历过了
            continue

        mark[tools.cal_cell_id(cell)] = parent

        if show_details:
            canvas.draw_cell(cell, canvas.COLOR.DARK_GREEN.value)
            canvas.update()

        if tools.cell_equal(cell, end):
            path = tools.cal_path(mark, tools.cal_cell_id(end))
            return path[1:]

        adjs = tools.adj(cell, mark, obstacles)
        for adj in adjs:
            queue.put(Node(adj, cell))

    return []


class Node:
    def __init__(self, cell, parent=None):
        self._cell = cell
        self._parent = parent

    @property
    def cell(self):
        return self._cell

    @property
    def parent(self):
        return self._parent
