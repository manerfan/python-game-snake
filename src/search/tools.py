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

from graph import canvas


def cell_equal(cell1: (int, int), cell2: (int, int)):
    """
    比较两个cell是否相同
    :param cell1:   cell1
    :param cell2:   cell2
    :return: True | False
    """
    if cell1 and not cell2:
        return False

    if not cell1 and cell2:
        return False

    if not cell1 and not cell2:
        return True

    (x1, y1) = cell1
    (x2, y2) = cell2

    return x1 == x2 and y1 == y2


def cal_cell_id(cell):
    (x, y) = cell
    return f"({x},{y})"


def is_adjacent(cell1, cell2):
    (x1, y1) = cell1
    (x2, y2) = cell2
    if x1 == x2 and abs(y1 - y2) == 1:
        return True
    if y1 == y2 and abs(x1 - x2) == 1:
        return True
    return False


def adj(cell, mark={}, obstacles=[]):
    """
    计算可用邻点
    :param cell:        坐标
    :param mark:        已遍历的点
    :param obstacles:   障碍点
    :return:            可用邻点
    """
    (x, y) = cell
    cells = [
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y)
    ]
    return filter(valid_cell(mark, obstacles), cells)


def cal_path(mark, cell_id):
    """
    通过mark计算路径
    :param mark:        路径树
    :param cell_id:     终点坐标
    :return:            路径
    """
    path = []
    cell = mark[cell_id]

    while cell:
        path.append(cell)
        parent_id = cal_cell_id(cell)
        if parent_id in mark.keys():
            cell = mark[parent_id]
        else:
            break

    path.reverse()
    return path


def valid_cell(mark={}, obstacles=[]):
    def valid(cell):
        (x, y) = cell
        if x < 0 or x >= canvas.WIDTH:
            return False
        if y < 0 or y >= canvas.HEIGHT:
            return False
        if cal_cell_id(cell) in mark.keys():
            return False
        for obstacle in obstacles:
            if cell_equal(cell, obstacle):
                return False
        return True

    return valid


if __name__ == "__main__":
    assert cell_equal(None, None)
    assert not cell_equal(None, (1, 2))
    assert not cell_equal((1, 2), None)
    assert not cell_equal((1, 2), (3, 4))
    assert cell_equal((1, 2), (1, 2))

    print(cal_cell_id((1, 2)))
