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

from queue import Queue

from graph import canvas

from search import tools


def cal(start, end, obstacles=[], show_details=False):
    """
    使用BFS算法搜索路径
    :param start:        起点
    :param end:          终点
    :param obstacles:    障碍
    :param show_details: 是否显示细节
    :return:             返回路径
    """
    if tools.cell_equal(start, end):
        return []

    if tools.is_adjacent(start, end):
        return [end]

    queue = Queue()
    queue.put(start)
    mark = {tools.cal_cell_id(start): None}

    while not queue.empty():
        cell = queue.get()

        adjs = tools.adj(cell, mark, obstacles)
        for adj in adjs:
            if tools.cal_cell_id(adj) in mark.keys():
                continue

            mark[tools.cal_cell_id(adj)] = cell
            queue.put(adj)

            if tools.cell_equal(adj, end):
                path = tools.cal_path(mark, tools.cal_cell_id(adj))
                return path[1:] + [end]

            if show_details:
                canvas.draw_cell(adj, canvas.COLOR.DARK_GREEN.value)
                canvas.update()

    return None
