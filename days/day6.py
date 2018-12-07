from collections import defaultdict

from days import AOCDay, day


@day(6)
class DaySix(AOCDay):
    coords = {}
    grid = []
    test_input = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    # max = 32
    max = 10000

    def common(self, input_data):
        # input_data = self.test_input.split("\n")

        character = 0
        for line in input_data:
            coords = line.split(", ")
            self.coords[character] = (int(coords[0]), int(coords[1]))
            character += 1

        max_x = max(self.coords.values(), key=lambda i: i[0])[0] + 2
        max_y = max(self.coords.values(), key=lambda i: i[1])[1] + 2
        yield "Grid is of size {} x {}".format(max_x, max_y)
        self.grid = []

        for x in range(max_y):
            self.grid.append([])
            for y in range(max_x):
                self.grid[-1].append("_")

        for character, coords in self.coords.items():
            self.grid[coords[1]][coords[0]] = character

        # yield "\n".join(["".join([self.chars[x] for x in row]) for row in self.grid])

    @staticmethod
    def manhattan_distance(current, center):
        dx = abs(current[0] - center[0])
        dy = abs(current[1] - center[1])
        return dx + dy

    def part1(self, input_data):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                distances = defaultdict(list)
                for character, coord in self.coords.items():
                    distances[DaySix.manhattan_distance((x, y), coord)].append(character)
                min_dist = min(distances.items(), key=lambda d: d[0])
                # yield "{} has minimum distance to {} ({})".format((x, y), min_dist[1], min_dist[0])
                if len(min_dist[1]) == 1:
                    if self.grid[y][x] != min_dist[1][0]:
                        self.grid[y][x] = min_dist[1][0]
                else:
                    self.grid[y][x] = "."

        # yield "\n".join(["".join([self.chars[x] if x != "." else "." for x in row]) for row in self.grid])

        # Filter out letters that are on the sides of the grid, as those are infinite
        letter_candidates = []
        for i in list(range(len(self.coords))):
            valid = True
            # First row
            for grid in self.grid[0]:
                if grid == i:
                    valid = False
                    break
            if valid:
                # First column
                for grid in [x[0] for x in self.grid]:
                    if grid == i:
                        valid = False
                        break
            if valid:
                # Last row
                for grid in self.grid[-1]:
                    if grid == i:
                        valid = False
                        break
            if valid:
                # Last column
                for grid in [x[-1] for x in self.grid]:
                    if grid == i:
                        valid = False
                        break

            if valid:
                letter_candidates.append(i)

        yield "Letter candidates: {}".format([self.chars[i] for i in letter_candidates])

        sizes = defaultdict(int)
        for y in self.grid:
            for x in y:
                if x in letter_candidates:
                    sizes[x] += 1

        max_size = max(sizes.items(), key=lambda x: x[1])
        yield "The largest field is {} with {} tiles".format(self.chars[max_size[0]], max_size[1])

    def part2(self, input_data):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.grid[y][x] = "#" if sum([DaySix.manhattan_distance((x, y), c) for _, c in self.coords.items()]) < self.max else "."

        # yield "\n".join(["".join(row) for row in self.grid])

        size = 0
        for y in self.grid:
            for x in y:
                if x == "#":
                    size += 1

        yield "The safe field is {} tiles large".format(size)
