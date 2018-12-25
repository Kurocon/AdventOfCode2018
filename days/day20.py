from typing import Dict, Tuple

from days import AOCDay, day


@day(20)
class DayTemplate(AOCDay):
    test_input_1 = "^WNE$"
    test_input_2 = "^ENWWW(NEEE|SSE(EE|N))$"
    test_input_3 = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
    test_input_4 = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"
    test_input_5 = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"

    grid: Dict[Tuple[int, int], int] = {(0, 0): 0}

    def parse(self, iterator, position=(0, 0), distance=0):
        saved_position = position
        saved_distance = distance

        for c in iterator:
            if c in "NESW":
                if c == "N":
                    position = (position[0], position[1]-1)
                elif c == "E":
                    position = (position[0]+1, position[1])
                elif c == "S":
                    position = (position[0], position[1]+1)
                elif c == "W":
                    position = (position[0]-1, position[1])
                distance += 1
                if position not in self.grid.keys() or distance < self.grid[position]:
                    self.grid[position] = distance
            elif c == "(":
                self.parse(iterator, position, distance)
            elif c == ")":
                return
            elif c == "|":
                position = saved_position
                distance = saved_distance
            elif c == "$":
                return
            elif c == "^":
                pass
            else:
                print("Dunno char {}".format(c))

    def common(self, input_data):
        # input_data = self.test_input_5
        self.grid = {(0, 0): 0}
        self.parse(iter(input_data))

    def part1(self, input_data):
        yield "Longest path is at distance {}".format(max(self.grid.values()))

    def part2(self, input_data):
        yield "{} rooms pass through at least 1000 doors".format(sum(1 for n in self.grid.values() if n >= 1000))
