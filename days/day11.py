from days import AOCDay, day


@day(11)
class DayTemplate(AOCDay):
    test_input = "42"
    serial_number: int = None

    def get_power_level(self, x, y):
        rack_id = x + 10
        power_level = ((rack_id * y) + self.serial_number) * rack_id
        hundreds = int(str(power_level)[-3]) if len(str(power_level)) >= 3 else 0
        return hundreds - 5

    def common(self, input_data):
        self.serial_number = 8
        assert self.get_power_level(3, 5) == 4
        self.serial_number = 57
        assert self.get_power_level(122, 79) == -5
        self.serial_number = 39
        assert self.get_power_level(217, 196) == 0
        self.serial_number = 71
        assert self.get_power_level(101, 153) == 4

        # input_data = self.test_input
        self.serial_number = int(input_data)

    def part1(self, input_data):
        max_power_level = (0, 0, 0)
        for x in range(300 - 3):
            for y in range(300 - 3):
                power_level_sum = 0
                for i in range(3):
                    for j in range(3):
                        power_level_sum += self.get_power_level(x+i, y+j)
                if power_level_sum > max_power_level[0]:
                    max_power_level = (power_level_sum, x, y)

        yield max_power_level[0], max_power_level[1], max_power_level[2]

    def part2(self, input_data):
        max_power_level = (0, 0, 0, 0)
        size = 0
        for size in range(1, 301):
            yield "Checking {}x{}".format(size, size)
            for x in range(300 - 3):
                for y in range(300 - 3):
                    power_level_sum = 0
                    for i in range(size):
                        for j in range(size):
                            power_level_sum += self.get_power_level(x+i, y+j)
                    if power_level_sum > max_power_level[0]:
                        max_power_level = (power_level_sum, x, y, size)
                        yield "New max power: {}".format(max_power_level)

        yield max_power_level[0], max_power_level[1], max_power_level[2], max_power_level[3]
