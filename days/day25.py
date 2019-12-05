from collections import defaultdict

from days import AOCDay, day


@day(25)
class DayTemplate(AOCDay):
    test_input = """0,0,0,0
3,0,0,0
0,3,0,0
0,0,3,0
0,0,0,3
0,0,0,6
9,0,0,0
12,0,0,0"""
    test_input2 = """-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0"""
    test_input3 = """1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2"""

    test_input4 = """1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2"""

    points = []
    graph = defaultdict(list)
    points_by_x_coord = defaultdict(list)

    def manhattan_distance(self, x, y):
        return sum(abs(xi - yi) for xi, yi in zip(x, y))

    def common(self, input_data):
        self.points = [tuple(int(x) for x in line.split(",")) for line in input_data]

    def part1(self, input_data):
        # Build a graph of neighbours (close enough according to manhattan distance) of points
        self.graph = defaultdict(list)
        self.points_by_x_coord = defaultdict(list)

        for point in self.points:
            for x in range(point[0] - 3, point[0] + 4):
                for candidate in self.points_by_x_coord[x]:
                    if self.manhattan_distance(point, candidate) <= 3:
                        self.graph[point].append(candidate)
                        self.graph[candidate].append(point)

            self.points_by_x_coord[point[0]].append(point)
            if point not in self.graph.keys():
                self.graph[point] = []

        # Connect the neighbours into constellations
        unused = set(self.graph.keys())
        num_constellations = 0

        while unused:
            num_constellations += 1
            # node = unused.pop()
            node = next(iter(unused))
            unused.remove(node)
            stack = [node]

            while stack:
                node = stack.pop()
                for neighbor in self.graph[node]:
                    if neighbor in unused:
                        stack.append(neighbor)
                        unused.remove(neighbor)

        yield num_constellations



    def part2(self, input_data):
        pass
