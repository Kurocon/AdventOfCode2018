from days import AOCDay, day


@day(5)
class DayFive(AOCDay):

    test_input = "dabAcCaCBAcCcaDA"

    @staticmethod
    def check_one_step(inp):
        orig_input = list(inp)
        output = list(inp)

        indices_to_remove = []
        for i in range(len(output)-1):
            c1, c2 = output[i], output[i+1]
            if c1 != c2 and c1.lower() == c2.lower():
                indices_to_remove.append(i)
                indices_to_remove.append(i+1)
                break
        indices_to_remove = reversed(sorted(indices_to_remove))
        for i in indices_to_remove:
            del output[i]

        return orig_input, output

    @staticmethod
    def remove_all(inp, char):
        return filter(lambda x: x != char.lower() and x != char.upper(), inp)

    def common(self, input_data):
        pass

    def part1(self, input_data):
        # input_data = [self.test_input]
        old = None
        new = input_data[0]
        while old != new:
            old, new = DayFive.check_one_step(new)

        yield "Input has {} characters, output has {} characters. {} characters reacted.".format(len(input_data[0]),
                                                                                                 len(new),
                                                                                                 len(input_data[0]) - len(new))

    def part2(self, input_data):
        results = {}
        for c in "abcdefghijklmnopqrstuvwxyz":
            yield "Processing {}...".format(c)
            current_input = list(DayFive.remove_all(input_data[0], c))

            old = None
            new = current_input
            while old != new:
                old, new = DayFive.check_one_step(new)
            results[c] = len(new)
            yield "{} results in {} characters.".format(c, len(new))

        shortest = min(results.items(), key=lambda x: x[1])
        yield "Removing {} leads to the shortest reactant, at {} long.".format(shortest[0], shortest[1])
