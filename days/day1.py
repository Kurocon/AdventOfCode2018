from days import AOCDay, day


@day(1)
class DayOne(AOCDay):
    frequency = 0

    def common(self):
        self.frequency = 0

    def part1(self):
        for i in self.input_data:
            self.frequency += i
        yield str(self.frequency)

    def part2(self):
        unique_frequencies = set()

        while True:
            for i in self.input_data:
                if self.frequency in unique_frequencies:
                    yield "DUP FREQ: {}".format(self.frequency)
                    return
                else:
                    unique_frequencies.add(self.frequency)
                self.frequency += i
