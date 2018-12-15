import collections
import enum
import time
from typing import Tuple, List, Optional, Set

from days import AOCDay, day


class Field:
    position: Tuple[int, int]

    def __init__(self, position: Tuple[int, int]):
        self.position = position

    def __str__(self):
        return " "

    def get_surrounding(self):
        x, y = self.position
        return [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]


class Wall(Field):
    def __str__(self):
        return "#"


class Empty(Field):
    def __str__(self):
        return "."


class Nothing(Field):
    def __str__(self):
        return " "


class Unit(Field):
    class Type(enum.Enum):
        ELF = enum.auto()
        GOBLIN = enum.auto()

        def __str__(self):
            return {
                Unit.Type.ELF: "E",
                Unit.Type.GOBLIN: "G",
            }[self]

    unit_type: 'Unit.Type'
    life: int = 100
    atk: int = 3

    def __init__(self, unit_type: 'Unit.Type', position: Tuple[int, int], life: int, atk: int):
        super(Unit, self).__init__(position)
        self.unit_type = unit_type
        self.life = life
        self.atk = atk

    def __str__(self):
        return str(self.unit_type)


class Board:
    board: List[List[Field]]
    units: List[Unit]
    is_part_two: bool = False
    elf_has_died: bool = False

    def __init__(self, size_x: int, size_y: int):
        self.board = [[None for _ in range(size_x)] for _ in range(size_y)]
        self.units = []
        self.is_part_two = False
        self.elf_has_died = False

    def __str__(self):
        res = ""
        occupied = {u.position: u for u in self.units if u.life > 0}
        for y, line in enumerate(self.board):
            res += "{:3} ".format(y)
            for field in line:
                res += str(occupied[field.position]) if field.position in occupied else str(field)
            res += "  "
            for u in [x for x in self.units if x.position[1] == y and x.life > 0]:
                res += " {}({:3}),".format(str(u), u.life)
            res += "\n"
        return res

    def get(self, position: Tuple[int, int]) -> Field:
        return self.board[position[1]][position[0]]

    def start_combat(self) -> int:
        go_on = True
        rounds: int = 0

        # Until we need to stop, do a round
        while go_on:
            go_on = self.tick()
            rounds += 1
            # print(self)
            # time.sleep(1)
            # input("Continue?")

        # Return the amount of rounds times the sum of life points of all units that are still alive.
        return (rounds - 1) * sum(u.life for u in self.units if u.life > 0)

    def tick(self) -> bool:
        # In reading order, go through the units
        for unit in sorted(self.units, key=lambda x: (x.position[1], x.position[0])):
            # Only alive units count
            if unit.life > 0:
                # Let the unit move
                go_on = self.move(unit)

                # Stop if unit says to end combat (all enemies dead), or part 2 and an elf has died
                if not go_on or (self.is_part_two and self.elf_has_died):
                    return False
        return True

    def move(self, unit: Unit) -> bool:
        # Find enemies
        enemies = [e for e in self.units if e.unit_type != unit.unit_type and e.life > 0]

        # If no enemies, end combat.
        if not enemies:
            return False

        # Identify places that we can go that are in range
        occupied_coords = set(u.position for u in self.units if u.life > 0 and u != unit)
        in_range_coords = set(coords for enemy in enemies for coords in enemy.get_surrounding()
                              if not isinstance(self.get(coords), Wall) and coords not in occupied_coords)

        # If we are not already in one of these positions, try to move to one of them.
        if unit.position not in in_range_coords:
            self.move_to_closest(unit, in_range_coords)

        # See if we are next to an enemy so we can attack
        attack_opportunities = [e for e in enemies if e.position in unit.get_surrounding()]
        if attack_opportunities:
            # Find the one with the lowest HP in reading order
            attack = min(attack_opportunities, key=lambda x: (x.life, (x.position[1], x.position[0])))
            attack.life -= unit.atk
            if attack.life <= 0 and attack.unit_type == Unit.Type.ELF:
                self.elf_has_died = True

        return True

    def move_to_closest(self, unit: Unit, coords: Set[Tuple[int, int]]):
        # Dijkstra's algorithm
        to_visit = collections.deque([(unit.position, 0)])  # Queue of coordinate, distance pairs
        distances = {unit.position: (0, None)}
        seen = set()
        occupied = set(u.position for u in self.units if u.life > 0)  # All occupied coordinates

        # While we still have some spots left to visit
        while to_visit:
            position, distance = to_visit.popleft()

            # For all of the neighbors of this position
            for neighbor in self.get(position).get_surrounding():
                # If this is a wall, or this is occupied, skip it.
                if isinstance(self.get(neighbor), Wall) or neighbor in occupied:
                    continue

                # If we have not seen this position before, or the distance to this is smaller than the distance that we
                # already found, update the distance and 'via' values
                if neighbor not in distances.keys() or (distances[neighbor][0], (distances[neighbor][1][1], distances[neighbor][1][0])) > (distance + 1, (position[1], position[0])):
                    distances[neighbor] = (distance + 1, position)

                # If we have not visited this neighbor yet, add it to the to_visit list if it is not in there yet.
                if neighbor not in seen:
                    if not any(neighbor == field[0] for field in to_visit):
                        to_visit.append((neighbor, distance + 1))

            # Mark the original position as seen
            seen.add(position)

        # See if we found a shortest path to one of our target coordinates,
        # and return the first one in reading order if we did, else return None
        results = [(distance, position) for position, (distance, via) in distances.items() if position in coords]
        if results:
            d, closest = min(results, key=lambda x: (x[0], (x[1][1], x[1][0])))
            while distances[closest][0] > 1:
                d, closest = distances[closest]
            unit.position = closest


@day(15)
class DayTemplate(AOCDay):
    test_input = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######"""
    test_input_2 = """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######"""
    test_input_3 = """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######"""
    test_input_4 = """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######"""
    test_input_5 = """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######"""
    test_input_6 = """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########"""
    test_input_7 = """################################
#######.G...####################
#########...####################
#########.G.####################
#########.######################
#########.######################
#########G######################
#########.#...##################
#########.....#..###############
########...G....###.....########
#######............G....########
#######G....G.....G....#########
######..G.....#####..G...#######
######...G...#######......######
#####.......#########....G..E###
#####.####..#########G...#....##
####..####..#########..G....E..#
#####.####G.#########...E...E.##
#########.E.#########.........##
#####........#######.E........##
######........#####...##...#..##
###...................####.##.##
###.............#########..#####
#G#.#.....E.....#########..#####
#...#...#......##########.######
#.G............#########.E#E####
#..............##########...####
##..#..........##########.E#####
#..#G..G......###########.######
#.G.#..........#################
#...#..#.......#################
################################"""
    test_input_8 = """###########
#G..#....G#
###..E#####
###########"""  # 10804

    board: Board = None
    gob_atk: int = 3
    elf_atk: int = 3
    life: int = 200

    def common(self, input_data):
        # input_data = self.test_input.split("\n")
        input_data = [list(x) for x in input_data]
        self.board = Board(len(input_data[0]), len(input_data))
        for y in range(len(input_data)):
            for x in range(len(input_data[y])):
                c = input_data[y][x]
                if c == "#":
                    thing = Wall((x, y))
                elif c == ".":
                    thing = Empty((x, y))
                elif c == "G":
                    self.board.units.append(Unit(Unit.Type.GOBLIN, (x, y), self.life, self.gob_atk))
                    thing = Empty((x, y))
                elif c == "E":
                    self.board.units.append(Unit(Unit.Type.ELF, (x, y), self.life, self.elf_atk))
                    thing = Empty((x, y))
                else:
                    print("I don't know what a '{}' is".format(c))
                    thing = Nothing((x, y))
                self.board.board[y][x] = thing

    def part1(self, input_data):
        yield "Combat ended with score {}".format(self.board.start_combat())

    def part2(self, input_data):
        i = 1
        done = False
        old_score = 0
        while not done:
            # initialize board
            self.elf_atk = i
            self.common(input_data)
            # Set part 2 flag
            self.board.is_part_two = True
            self.board.elf_has_died = False
            end_score = self.board.start_combat()
            if not self.board.elf_has_died:
                old_score = end_score
                break
            i += 1

        yield "No elves died with attack power {}. Round had score {}".format(i, old_score)
