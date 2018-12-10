import itertools
import re
from functools import reduce
from typing import List, Optional

from days import AOCDay, day


class Point:
    x: int = 0
    y: int = 0
    velocity_x: int = 0
    velocity_y: int = 0

    def __init__(self, x: int, y: int, velocity_x: int, velocity_y: int):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def tick(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def copy(self):
        return Point(self.x, self.y, self.velocity_x, self.velocity_y)

@day(10)
class DayTen(AOCDay):
    test_input = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""
    input_regex = r'position=<(?:\s+)?(?P<pos_x>-?[0-9]+), (?:\s+)?(?P<pos_y>-?[0-9]+)> velocity=<(?:\s+)?(?P<vel_x>-?[0-9]+), (?:\s+)?(?P<vel_y>-?[0-9]+)>'

    points = []
    result: List[List[Optional[Point]]] = [[]]

    def common(self, input_data):
        # input_data = self.test_input.split("\n")
        self.points = []
        for line in input_data:
            m = re.match(self.input_regex, line)
            if m:
                self.points.append(Point(int(m.group('pos_x')), int(m.group('pos_y')), int(m.group('vel_x')), int(m.group('vel_y'))))
            else:
                yield "Cannot parse line {}".format(line)

    def get_bounding_box(self, points):
        l, t = reduce(lambda a, b: map(min, zip(a, b)), [(p.x, p.y) for p in points])
        r, b = reduce(lambda a, b: map(max, zip(a, b)), [(p.x, p.y) for p in points])
        return l, t, r, b

    def get_grid(self, points: List[Point]):
        l, t, r, b = self.get_bounding_box(points)
        result: List[List[Optional[Point]]] = []
        for y in range(abs(t) + b + 1):
            result.append([])
            for x in range(abs(l) + r + 1):
                result[-1].append(None)
        for p in points:
            result[abs(t) + p.y][abs(l) + p.x] = p

        return ["".join(["#" if x is not None else "." for x in row]) for row in result]

    def detect(self, old_surface):
        new_l, new_t, new_r, new_b = self.get_bounding_box(self.points)
        new_surface = new_r - new_l * new_b - new_t
        return new_surface, new_surface > old_surface

    def part1(self, input_data):
        i = 0

        old_surface = 99999999999999999999999999999999999
        old_result = self.points

        while True:
            old_surface, larger = self.detect(old_surface)

            if larger:
                yield "\n---- TEXT FOUND!! -----\n"
                yield "\n".join(self.get_grid(old_result))
                return

            old_result = [x.copy() for x in self.points]

            for p in self.points:
                p.tick()
            i += 1

    def part2(self, input_data):
        i = 0

        old_surface = 99999999999999999999999999999999999

        while True:
            old_surface, larger = self.detect(old_surface)

            if larger:
                yield "Have to wait {} seconds.".format(i - 1)
                return

            for p in self.points:
                p.tick()
            i += 1
