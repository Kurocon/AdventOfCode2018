import re
from collections import defaultdict

from days import AOCDay, day


@day(4)
class DayTemplate(AOCDay):
    sleep_data = defaultdict(int)
    minute_data = {x: [] for x in range(60)}
    regex_begin = r'\[([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})\] Guard #([0-9]+) begins shift'
    regex_sleep = r'\[([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})\] falls asleep'
    regex_awake = r'\[([0-9]{4})-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})\] wakes up'

    test_data = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-01 00:55] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""

    def common(self, input_data):
        # input_data = self.test_data.split("\n")
        input_data = sorted(input_data)
        # yield "\n".join(input_data)
        self.sleep_data = defaultdict(int)
        self.minute_data = {x: [] for x in range(60)}
        current_guard = None
        start_minute = None
        for l in input_data:
            m = re.match(self.regex_begin, l)
            if m:
                current_guard = m.group(6)
            m = re.match(self.regex_sleep, l)
            if m:
                start_minute = int(m.group(5))
            m = re.match(self.regex_awake, l)
            if m:
                end_minute = int(m.group(5))
                for i in range(start_minute, end_minute):
                    self.minute_data[i].append(current_guard)
                    self.sleep_data[current_guard] += 1

    def part1(self, input_data):
        max_minutes = max(self.sleep_data.values())
        most_sleep = [x for x, y in self.sleep_data.items() if max_minutes == y][0]
        yield "Guard {} sleeps the most {} minutes".format(most_sleep, self.sleep_data[most_sleep])

        new_data = {x: [y for y in ys if y == most_sleep] for x, ys in self.minute_data.items()}
        lengths = {x: len(y) for x, y in new_data.items()}
        max_length = max(lengths.values())
        minute = [x for x, y in lengths.items() if y == max_length][0]
        yield "He sleeps the most on minute {} ({} times)".format(minute, max_length)

        yield "So the answer is {} * {} = {}".format(most_sleep, minute, int(most_sleep) * int(minute))

    def part2(self, input_data):
        guards = self.sleep_data.keys()

        def max_minute(guard):
            minutes = {x: len([y for y in ys if y == guard]) for x, ys in self.minute_data.items()}
            max_item = max(minutes.items(), key=lambda x: x[1])
            return max_item

        mins_per_guard = {guard: max_minute(guard) for guard in guards}
        gd, mdata = max(mins_per_guard.items(), key=lambda x: x[1][1])
        yield "Guard {} spent most time asleep in minute {} ({} times), so the answer is {}".format(gd, mdata[0], mdata[1],
                                                                                                    int(gd) * int(mdata[0]))
