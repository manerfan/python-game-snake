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

import heapq


class PriorityQueue:
    """
    优先级队列
    """
    def __init__(self):
        self._queue = []
        self._index = 0

    def put(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def get(self):
        if len(self._queue) < 1:
            return None
        return heapq.heappop(self._queue)[-1]

    def empty(self):
        return len(self._queue) < 1


if __name__ == "__main__":
    queue = PriorityQueue()
    queue.put((1, 2), 1)
    queue.put((3, 4), 3)
    queue.put((2, 3), 2)
    print(queue.get())
    print(queue.get())
    print(queue.empty())
    print(queue.get())
    print(queue.empty())
