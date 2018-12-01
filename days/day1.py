from days import AOCDay, day


@day(1)
class DayOne(AOCDay):
    def part1(self, input_data):
        yield sum(i for i in map(int, input_data))

    def part2(self, input_data):
        frequency = 0
        unique_frequencies = set()
        data = list(map(int, input_data))

        while True:
            for i in data:
                if frequency in unique_frequencies:
                    yield frequency
                    return

                unique_frequencies.add(frequency)
                frequency += i
