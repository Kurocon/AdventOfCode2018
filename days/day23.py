import re
from queue import PriorityQueue

from days import AOCDay, day


@day(23)
class DayTemplate(AOCDay):
    test_input = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1"""
    test_input2 = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""

    bots = {}
    BOTS_RE = re.compile('pos=<(?P<x>[-0-9]+),(?P<y>[-0-9]+),(?P<z>[-0-9]+)>, r=(?P<r>[-0-9]+)')

    def manhattan_distance(self, source, target):
        return abs(source[0] - target[0]) + abs(source[1] - target[1]) + abs(source[2] - target[2])

    def in_range(self, bot):
        bots_in_range = []
        for x in self.bots:
            if self.manhattan_distance(bot, x) <= self.bots[bot]:
                bots_in_range.append(x)
        return bots_in_range

    def pos_in_range(self, bot, pos):
        return self.manhattan_distance(bot, pos) <= self.bots[bot]

    def common(self, input_data):
        # input_data = self.test_input2.split("\n")
        for line in input_data:
            rx = self.BOTS_RE.match(line)
            x, y, z, r = int(rx.group('x')), int(rx.group('y')), int(rx.group('z')), int(rx.group('r'))
            self.bots[(x,y,z)] = r

    def part1(self, input_data):
        max_bot = max(self.bots, key=lambda x: self.bots[x])
        print("Best bot is {} with r={}".format(max_bot, self.bots[max_bot]))
        bots_in_range = self.in_range(max_bot)
        print("{} bots in range.".format(len(bots_in_range)))

    def part2(self, input_data):
        queue = PriorityQueue()
        for bot in self.bots:
            distance = self.manhattan_distance((0, 0, 0), bot)
            queue.put((max(0, distance - self.bots[bot]), 1))
            queue.put((distance + self.bots[bot] + 1, -1))

        count, max_count, result = 0, 0, 0
        while not queue.empty():
            distance, n = queue.get()
            count += n
            if count > max_count:
                max_count, result = count, distance

        yield result
