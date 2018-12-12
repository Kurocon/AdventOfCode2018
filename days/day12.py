from typing import Dict, List, Optional

from days import AOCDay, day


class Pot:
    prv: 'Pot' = None
    nxt: 'Pot' = None
    plant: bool = False
    index: int = 0

    def __init__(self, prv: Optional['Pot'], nxt: Optional['Pot'], plant: bool, index: int):
        self.prv = prv
        self.nxt = nxt
        self.plant = plant
        self.index = index

    def __str__(self):
        return "#" if self.plant else "."

    def __repr__(self):
        return self.__str__()

    def get_prevs(self):
        if self.prv is not None:
            return "{}{}".format(self.prv.get_prevs(), self.prv)
        else:
            return ".."

    def get_nexts(self):
        if self.nxt is not None:
            return "{}{}".format(self.nxt, self.nxt.get_nexts())
        else:
            return ".."

    def get_two_prevs(self):
        if self.prv is not None and self.prv.prv is not None:
            return "{}{}".format(self.prv.prv, self.prv)
        else:
            if self.prv is None:
                return ".."
            elif self.prv.prv is None:
                return ".{}".format(self.prv)

    def get_two_nexts(self):
        if self.nxt is not None and self.nxt.nxt is not None:
            return "{}{}".format(self.nxt, self.nxt.nxt)
        else:
            if self.nxt is None:
                return ".."
            elif self.nxt.nxt is None:
                return "{}.".format(self.nxt)

    def get_match(self):
        return "{}{}{}".format(self.get_two_prevs(), self, self.get_two_nexts())


@day(12)
class DayTwelve(AOCDay):
    initial_state: Pot = None
    first_pot: Pot = None
    last_pot: Pot = None
    transitions: Dict[str, bool] = {}
    current_state = List[bool]

    number_of_iterations = 20

    test_input = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
....# => .
...#. => .
.#..# => .
#..#. => .
..#.# => .
#.#.. => .
.#..# => .
#..## => .
..##. => .
##... => .
#.... => .
..... => .
..... => .
....# => .
..### => .
.###. => .
##... => .
#...# => .
..### => .
.###. => .
##..# => .
.##.# => .
#.##. => .
##### => ."""

    def get_state_repr(self) -> str:
        return "{}{}{}".format(self.initial_state.get_prevs(), self.initial_state, self.initial_state.get_nexts())

    def get_final_sum(self) -> int:
        current_pot = self.first_pot
        result = 0
        while current_pot is not None:
            if current_pot.plant:
                result += current_pot.index
            current_pot = current_pot.nxt
        return result

    def common(self, input_data):
        # input_data = self.test_input.split("\n")
        initial_state = input_data[0].split(" ")[2]

        # Add two pots to the front
        self.first_pot = Pot(None, None, False, -2)
        last_pot = Pot(self.first_pot, None, False, -1)
        self.first_pot.nxt = last_pot
        index = 0
        self.initial_state = None

        for c in initial_state:
            pot = Pot(None, None, c == "#", index)
            index += 1
            if last_pot is not None:
                last_pot.nxt = pot
                pot.prv = last_pot
            last_pot = pot
            if self.initial_state is None:
                self.initial_state = pot

        # Add two pots to the end
        penultimate_pot = Pot(last_pot, None, False, index)
        self.last_pot = Pot(penultimate_pot, None, False, index+1)
        penultimate_pot.nxt = self.last_pot
        last_pot.nxt = penultimate_pot

        self.transitions: Dict[str, bool] = {}
        for line in input_data[2:]:
            match, nxt = line.split(" => ")
            self.transitions[match] = nxt == "#"

        yield self.get_state_repr()

    def part1(self, input_data):
        yield "{:>2}: {}".format(0, self.get_state_repr())
        for iteration in range(1, self.number_of_iterations + 1):
            last_repr = self.get_state_repr()

            indices_to_flip = []

            start_index = self.first_pot.index - 2

            for i in range(2, len(last_repr)-2):
                match = last_repr[(i-2):(i+3)]
                try:
                    if last_repr[i] != ("#" if self.transitions[match] else "."):
                        indices_to_flip.append(start_index + i)
                except KeyError:
                    yield "{} not in trans".format(match)

            # yield indices_to_flip

            p = self.first_pot
            while p is not None:
                if p.index in indices_to_flip:
                    p.plant = not p.plant
                    indices_to_flip.remove(p.index)
                p = p.nxt

            # Check if we need to add new first pots
            if self.first_pot.plant or self.first_pot.nxt.plant:
                if self.first_pot.plant:
                    # Two new pots
                    new_first_pot = Pot(None, None, False, self.first_pot.index-2)
                    new_second_pot = Pot(new_first_pot, self.first_pot, False, self.first_pot.index-1)
                    new_first_pot.nxt = new_second_pot
                    self.first_pot.prv = new_second_pot
                    self.first_pot = new_first_pot
                elif self.first_pot.nxt.plant:
                    # One new pot
                    new_first_pot = Pot(None, self.first_pot, False, self.first_pot.index-1)
                    self.first_pot.prv = new_first_pot
                    self.first_pot = new_first_pot

            # Check if we need to add new last pots
            if self.last_pot.plant or self.last_pot.prv.plant:
                if self.last_pot.plant:
                    # Two new pots
                    new_penultimate_pot = Pot(self.last_pot, None, False, self.last_pot.index+1)
                    new_last_pot = Pot(new_penultimate_pot, None, False, self.last_pot.index+2)
                    new_penultimate_pot.prv = new_last_pot
                    self.last_pot.nxt = new_penultimate_pot
                    self.last_pot = new_last_pot
                elif self.last_pot.prv.plant:
                    # One new pot
                    new_last_pot = Pot(self.last_pot, None, False, self.last_pot.index+1)
                    self.last_pot.nxt = new_last_pot
                    self.last_pot = new_last_pot

            yield "{:>2}: {}".format(iteration, self.get_state_repr())

        yield "So the resulting sum is {}".format(self.get_final_sum())

    def part2(self, input_data):
        self.number_of_iterations = 50000000000
        # yield "{:>2}: {}".format(0, self.get_state_repr())

        difference = 0
        prevsum = 0
        history = []

        for iteration in range(1, self.number_of_iterations + 1):
            last_repr = self.get_state_repr()

            indices_to_flip = []

            start_index = self.first_pot.index - 2

            for i in range(2, len(last_repr)-2):
                match = last_repr[(i-2):(i+3)]
                try:
                    if last_repr[i] != ("#" if self.transitions[match] else "."):
                        indices_to_flip.append(start_index + i)
                except KeyError:
                    yield "{} not in trans".format(match)

            # yield indices_to_flip

            p = self.first_pot
            while p is not None:
                if p.index in indices_to_flip:
                    p.plant = not p.plant
                    indices_to_flip.remove(p.index)
                p = p.nxt

            # Check if we need to add new first pots
            if self.first_pot.plant or self.first_pot.nxt.plant:
                if self.first_pot.plant:
                    # Two new pots
                    new_first_pot = Pot(None, None, False, self.first_pot.index-2)
                    new_second_pot = Pot(new_first_pot, self.first_pot, False, self.first_pot.index-1)
                    new_first_pot.nxt = new_second_pot
                    self.first_pot.prv = new_second_pot
                    self.first_pot = new_first_pot
                elif self.first_pot.nxt.plant:
                    # One new pot
                    new_first_pot = Pot(None, self.first_pot, False, self.first_pot.index-1)
                    self.first_pot.prv = new_first_pot
                    self.first_pot = new_first_pot

            # Check if we need to add new last pots
            if self.last_pot.plant or self.last_pot.prv.plant:
                if self.last_pot.plant:
                    # Two new pots
                    new_penultimate_pot = Pot(self.last_pot, None, False, self.last_pot.index+1)
                    new_last_pot = Pot(new_penultimate_pot, None, False, self.last_pot.index+2)
                    new_penultimate_pot.prv = new_last_pot
                    self.last_pot.nxt = new_penultimate_pot
                    self.last_pot = new_last_pot
                elif self.last_pot.prv.plant:
                    # One new pot
                    new_last_pot = Pot(self.last_pot, None, False, self.last_pot.index+1)
                    self.last_pot.nxt = new_last_pot
                    self.last_pot = new_last_pot

            final_sum = self.get_final_sum()
            difference = final_sum - prevsum
            prevsum = final_sum
            history.append(difference)

            # yield iteration, final_sum, difference

            if len(history) > 20:
                history = history[-20:]

            if len(history) == 20 and len(list(set(history))) == 1:
                yield "Pattern found after loop {}: Adds {} every time".format(iteration, history[0])

                total_sum = final_sum + (self.number_of_iterations - iteration) * history[0]
                yield "Total sum: {}".format(total_sum)

                break

        yield "So the resulting sum is {}".format(self.get_final_sum())
