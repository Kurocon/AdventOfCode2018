import heapq
import re
from functools import lru_cache
from typing import List

from days import AOCDay, day


@day(22)
class DayTemplate(AOCDay):
    test_input = """depth: 510
target: 10,10""".split("\n")

    depth: int = 0
    coordinates: List[int] = []

    @lru_cache(maxsize=None)
    def geological_index(self, x, y):
        if x == 0 and y == 0:
            return 0
        if [x, y] == self.coordinates:
            return 0
        if y == 0:
            return x * 16807
        if x == 0:
            return y * 48271
        return self.erosion_level(x-1, y) * self.erosion_level(x, y-1)

    @lru_cache(maxsize=None)
    def erosion_level(self, x, y):
        geo_index = self.geological_index(x, y)
        return (geo_index + self.depth) % 20183

    TYPE_ROCKY = 0
    TYPE_WET = 1
    TYPE_NARROW = 2

    @lru_cache(maxsize=None)
    def region_type(self, x, y):
        return self.erosion_level(x, y) % 3

    def common(self, input_data):
        # input_data = self.test_input
        self.depth = int(re.findall("\d+", input_data[0])[0])
        self.coordinates = list(map(int, re.findall("\d+", input_data[1])))[:2]
        yield "Depth: {}\nTarget: {}, {}".format(self.depth, self.coordinates[0], self.coordinates[1])

    def part1(self, input_data):
        res = 0
        for y in range(self.coordinates[1]+1):
            for x in range(self.coordinates[0]+1):
                res += self.region_type(x, y)
        yield "Region risk level: {}".format(res)

    TOOL_NEITHER = 0
    TOOL_TORCH = 1
    TOOL_CLIMBING_GEAR = 2

    ALLOWED_TOOLS = {
        TYPE_ROCKY: [TOOL_CLIMBING_GEAR, TOOL_TORCH],
        TYPE_WET: [TOOL_CLIMBING_GEAR, TOOL_NEITHER],
        TYPE_NARROW: [TOOL_TORCH, TOOL_NEITHER],
    }

    def adjacent(self, x, y):
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    def search(self):
        tool = self.TOOL_TORCH

        # Queue = (minutes, x, y, tool)
        queue = [(0, 0, 0, tool)]
        best_paths = {}

        target = (self.coordinates[0], self.coordinates[1], self.TOOL_TORCH)

        while len(queue) > 0:
            mins, x, y, tool = heapq.heappop(queue)

            if (x, y, tool) in best_paths and best_paths[(x, y, tool)] <= mins:
                continue
            best_paths[(x, y, tool)] = mins

            if (x, y, tool) == target:
                return mins

            for i in range(3):
                if i != tool and i != self.region_type(x, y):
                    heapq.heappush(queue, (mins + 7, x, y, i))

            for adj in self.adjacent(x, y):
                # Don't look to far from the target
                if 0 <= adj[0] <= self.coordinates[0] + 1000 and 0 <= adj[1] <= self.coordinates[1] + 1000:
                    if tool != self.region_type(adj[0], adj[1]):  # If Tool ID equals region type, the tool cant be used there.
                        heapq.heappush(queue, (mins + 1, adj[0], adj[1], tool))

    def part2(self, input_data):
        yield self.search()
