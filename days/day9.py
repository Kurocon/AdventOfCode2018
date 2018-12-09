import re
from collections import defaultdict
from typing import Optional, Dict

from days import AOCDay, day


class Entry:
    next: Optional['Entry'] = None
    prev: Optional['Entry'] = None
    value: int = 0

    def __init__(self, value: int, previous_entry: Optional['Entry'] = None, next_entry: Optional['Entry'] = None):
        self.value = value
        self.prev = previous_entry
        self.next = next_entry


@day(9)
class DayNine(AOCDay):
    test_input = "9 players; last marble is worth 25 points"
    input_regex = r'([0-9]+) players; last marble is worth ([0-9]+) points'

    num_players: int = None
    num_marbles: int = None
    current_marble: Entry = None
    scores: Dict[int, int] = None

    def common(self, input_data):
        # input_data = self.test_input
        m = re.match(self.input_regex, input_data)
        self.num_players = int(m.group(1))
        self.num_marbles = int(m.group(2))
        entry_zero = Entry(0)
        entry_zero.next = entry_zero
        entry_zero.prev = entry_zero
        self.current_marble = entry_zero
        self.scores = defaultdict(int)

    def part1(self, input_data):
        return self.process()

    def part2(self, input_data):
        self.num_marbles = self.num_marbles * 100
        return self.process()

    def process(self):
        # Reduce class attribute accesses
        current_marble = self.current_marble
        scores = self.scores
        num_players = self.num_players

        for new_marble in range(1, self.num_marbles + 1):
            # if new_marble % 10000 == 0:
            #     yield(new_marble)

            if new_marble % 23 == 0:
                current_player = (new_marble % num_players) + 1
                current_marble = current_marble.prev.prev.prev.prev.prev.prev.prev
                scores[current_player] += new_marble + current_marble.value
                current_marble.prev.next = current_marble.next
                current_marble.next.prev = current_marble.prev
                current_marble = current_marble.next

            else:
                new_marble = Entry(new_marble, current_marble.next, current_marble.next.next)
                current_marble.next.next.prev = new_marble
                current_marble.next.next = new_marble
                current_marble = new_marble

        yield max(scores.values())
