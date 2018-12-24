import re
from collections import defaultdict
from enum import IntEnum
from typing import Dict

from days import AOCDay, day


PARSE_REGEX_1 = r'(?:x=(?P<x>[0-9]+), y=(?P<y1>[0-9]+)(?:..(?P<y2>[0-9]+))?)'
PARSE_REGEX_2 = r'(?:y=(?P<y>[0-9]+), x=(?P<x1>[0-9]+)(?:..(?P<x2>[0-9]+))?)'


class Items(IntEnum):
    SAND = 0
    CLAY = 1
    SOURCE = 2
    WATER = 3
    STATICWATER = 4

    def is_water(self):
        return self in [Items.WATER, Items.STATICWATER]

    @staticmethod
    def from_int(n):
        return {
            Items.SAND: ".",
            Items.CLAY: "#",
            Items.SOURCE: "+",
            Items.WATER: "|",
            Items.STATICWATER: '~'
        }[n]


@day(17)
class DayTemplate(AOCDay):
    test_input = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504""".split("\n")

    data: Dict[int, Dict[int, Items]] = defaultdict(lambda: defaultdict(lambda: Items.SAND))
    min_y = 0
    max_y = 0
    min_x = 0
    max_x = 0

    def print(self):
        result = ""
        for y in range(self.min_y, self.max_y+1):
            for x in range(self.min_x, self.max_x+1):
                result += Items.from_int(self.data[y][x])
            result += "\n"
        return result

    def common(self, input_data):
        # input_data = self.test_input
        data = defaultdict(lambda: defaultdict(int))
        for line in input_data:
            m1 = re.match(PARSE_REGEX_1, line)
            m2 = re.match(PARSE_REGEX_2, line)
            if m1:
                grp = m1.groupdict()
                x = int(grp['x'])
                y1 = int(grp['y1'])
                y2 = int(grp['y2'])
                for y in range(y1, y2+1):
                    self.data[y][x] = Items.CLAY
            elif m2:
                grp = m2.groupdict()
                y = int(grp['y'])
                x1 = int(grp['x1'])
                x2 = int(grp['x2'])
                for x in range(x1, x2+1):
                    self.data[y][x] = Items.CLAY
            else:
                yield "Error parsing line {}".format(line)

        # Water source
        self.data[0][500] = Items.SOURCE

        self.min_y = min(self.data.keys())
        self.max_y = max(self.data.keys())
        self.min_x = min([i for x in self.data.values() for i in x.keys()])
        self.max_x = max([i for x in self.data.values() for i in x.keys()])

    def in_range(self, x, y):
        # return (self.min_x-1 < x < self.max_x+1) and (self.min_y-1 < y < self.max_y+1)
        return self.min_y-1 < y < self.max_y+1

    def onlywater(self, x, y):
        # If the line below has either .~. #~. or .~#, return True
        return (self.data[y+1][x-1] == Items.SAND or self.data[y+1][x+1] == Items.SAND) and self.data[y+1][x].is_water()
        #
        #
        # # If below this is only a line of water to the bottom, return True.
        # if all(self.data[j][x] == Items.WATER for j in range(y+1, self.max_y+1)):
        #     return True
        # return False

    def onlywater_x(self, x, y):
        # If the line below x,y has only water until it reaches sand on either side, return True.
        min_x = x
        max_x = x
        sand_min, sand_max = False, False
        # Find sand to left
        for i in range(x, self.min_x-1, -1):
            if not self.data[y+1][i].is_water():
                min_x = i
                sand_min = self.data[y+1][i] == Items.SAND
                break
        min_x += 1  # Off-by-one to let the range below start at the correct x value for checking
        # Find sand to right
        for i in range(x, self.max_x+1):
            if not self.data[y+1][i].is_water():
                max_x = i
                sand_max = self.data[y+1][i] == Items.SAND
                break
        # Check if all water
        if (sand_min or sand_max) and all(self.data[y+1][i].is_water() for i in range(min_x, max_x)):
            return True
        return False

    def convert_static_to_flowing(self, line):
        if Items.WATER not in line.values() or Items.STATICWATER not in line.values():
            return

        start = 0
        has_flowing = False
        for i in range(max(line.keys())+1):
            if line[i] == Items.WATER:
                has_flowing = True
                for j in range(start, i):
                    if line[j] == Items.STATICWATER:
                        line[j] = Items.WATER
            elif line[i] == Items.STATICWATER:
                if has_flowing:
                    line[i] = Items.WATER
            else:
                start = i
                has_flowing = False

    def simulate_water(self):
        x, y = 500, 0
        if self.data[y+1][x] != Items.SAND:
            raise ValueError("Water full")

        static = False

        while self.in_range(x, y):
            # Water moves down until it finds clay or water
            if self.data[y+1][x] == Items.SAND:
                while self.data[y+1][x] == Items.SAND and self.in_range(x, y+1):
                    y += 1

                # If we reached the end of the map, stop
                if not self.in_range(x, y+1):
                    static = False
                    break

                continue

            # If below this is only a horizontal line of water between wand, stop here.
            if self.onlywater_x(x, y):
                static = False
                break

            # If free space to the left and something below, move left
            if self.data[y][x-1] == Items.SAND and self.data[y+1][x] != Items.SAND:
                while self.data[y][x-1] == Items.SAND and self.data[y+1][x] != Items.SAND and self.in_range(x-1, y) and not self.onlywater(x, y):
                    x -= 1

                # If we stopped because of a wall to the left, stop
                if self.data[y][x-1] != Items.SAND:
                    if self.data[y][x-1] == Items.WATER:
                        static = False
                    else:
                        static = True
                    break
                # If we reached the end of the map, stop
                if not self.in_range(x-1, y):
                    static = False
                    break
                # If below this is only a line of water to the bottom, stop
                if self.onlywater(x, y):
                    static = False
                    break
                continue

            # Else, if free space to the right and something below, move right
            elif self.data[y][x+1] == Items.SAND and self.data[y+1][x] != Items.SAND:
                while self.data[y][x+1] == Items.SAND and self.data[y+1][x] != Items.SAND and self.in_range(x+1, y) and not self.onlywater(x, y):
                    x += 1

                # If we stopped because of a wall to the right, stop
                if self.data[y][x+1] != Items.SAND:
                    if self.data[y][x+1] == Items.WATER:
                        static = False
                    else:
                        static = True
                    break
                # If we reached the end of the map, stop
                if not self.in_range(x+1, y):
                    static = False
                    break
                # If below this is only a line of water to the bottom, stop
                if self.onlywater(x, y):
                    static = False
                    break
                continue

            # Else, stay here.
            static = True
            break

        self.data[y][x] = Items.STATICWATER if static else Items.WATER
        print("x={},y={}".format(x, y))

    def part1(self, input_data):
        try:
            while True:
                self.simulate_water()
                # yield self.print()
                # input("?")
        except ValueError:
            # Water connected to only other water and at least one flowing water should be flowing
            for line in self.data.values():
                self.convert_static_to_flowing(line)

            self.min_y = min(self.data.keys())
            self.max_y = max(self.data.keys())
            self.min_x = min([i for x in self.data.values() for i in x.keys()])
            self.max_x = max([i for x in self.data.values() for i in x.keys()])

            yield self.print()
            s = sum([1 if x == Items.STATICWATER else 0 for row in self.data.values() for x in row.values()])
            s -= sum([1 if x == Items.STATICWATER else 0 for x in self.data[max(self.data.keys())].values()])
            f = sum([1 if x == Items.WATER else 0 for row in self.data.values() for x in row.values()])
            f -= sum([1 if x == Items.WATER else 0 for x in self.data[max(self.data.keys())].values()])
            yield "Water: {}".format(s)
            yield "Flowing: {}".format(f - 2)
            yield "Total: {}".format(s + f - 2)

    def part2(self, input_data):
        pass  # Part 1 does both.
