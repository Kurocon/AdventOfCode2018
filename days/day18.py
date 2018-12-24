from collections import defaultdict
from enum import IntEnum

from days import AOCDay, day


class Field(IntEnum):
    OPEN = 0
    TREES = 1
    LUMBER = 2

    def to_str(self):
        return {
            Field.OPEN: ".",
            Field.TREES: "|",
            Field.LUMBER: "#"
        }[self]

    @staticmethod
    def from_str(c):
        return {
            ".": Field.OPEN,
            "|": Field.TREES,
            "#": Field.LUMBER
        }[c]


@day(18)
class DayTemplate(AOCDay):
    test_input = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.""".split("\n")

    data = []

    histories = []

    def print(self):
        res = []
        for line in self.data:
            res.append("".join(x.to_str() for x in line))
        return "\n".join(res)

    def common(self, input_data):
        # input_data = self.test_input
        self.data = []
        for line in input_data:
            self.data.append([])
            for c in line:
                self.data[-1].append(Field.from_str(c))

    def part1(self, input_data):
        yield self.print()

        for i in range(10):
            self.data = self.do_generation()

        counts = self.get_counts()
        yield "{} trees, {} lumberyards, {}x{}={}".format(
            counts[Field.TREES], counts[Field.LUMBER],
            counts[Field.TREES], counts[Field.LUMBER],
            counts[Field.TREES] * counts[Field.LUMBER]
        )

    def part2(self, input_data):
        i, index = 0, 0
        yield "Searching for pattern..."
        for i in range(1000000000):
            self.data = self.do_generation()

            if self.data not in self.histories:
                self.histories.append(self.data)
            else:
                index = self.histories.index(self.data)
                yield "Found collision with {} on {} ({} cycles)".format(index, i, i-index)
                break

        offset = (1000000000 - index) % (i-index)
        self.data = self.histories[index + offset - 1]

        counts = self.get_counts()
        yield "{} trees, {} lumberyards, {}x{}={}".format(
            counts[Field.TREES], counts[Field.LUMBER],
            counts[Field.TREES], counts[Field.LUMBER],
            counts[Field.TREES] * counts[Field.LUMBER]
        )

    def do_generation(self):
        output = [x[:] for x in self.data]  # Copy to create new generation

        for y in range(len(output)):
            for x in range(len(output[y])):
                adj = self.adjacents(self.data, x, y)

                # Open becomes trees if 3+ are trees
                if output[y][x] == Field.OPEN and adj[Field.TREES] >= 3:
                    output[y][x] = Field.TREES
                # Trees becomes lumberyard if 3+ are lumberyard
                elif output[y][x] == Field.TREES and adj[Field.LUMBER] >= 3:
                    output[y][x] = Field.LUMBER
                # Lumberyard changes to open if not adjacent to at least one lumberyard and one trees
                elif output[y][x] == Field.LUMBER and (adj[Field.LUMBER] == 0 or adj[Field.TREES] == 0):
                    output[y][x] = Field.OPEN

        return output

    def get_counts(self):
        counts = defaultdict(int)
        for y in range(len(self.data)):
            for x in range(len(self.data[y])):
                counts[self.data[y][x]] += 1
        return counts

    @staticmethod
    def adjacents(field, x, y):
        res = defaultdict(int)
        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:
                if i != 0 or j != 0:
                    if (0 <= y+j < len(field)) and (0 <= x+i < len(field[0])):
                        res[field[y+j][x+i]] += 1
        return res
