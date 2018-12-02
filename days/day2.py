from collections import defaultdict

from days import AOCDay, day


@day(2)
class DayTemplate(AOCDay):
    def common(self, input_data):
        pass

    def part1(self, input_data):
        res = {2: 0, 3: 0}
        for i in input_data:
            d = defaultdict(int)
            for c in i:
                d[c] += 1
            has_two = False
            has_three = False
            for c, v in d.items():
                if v == 2:
                    has_two = True
                if v == 3:
                    has_three = True
            if has_two:
                res[2] += 1
            if has_three:
                res[3] += 1
        yield "{} items with 2 common letters, and {} items with 3 common letters".format(res[2], res[3])
        yield "Checksum: {}".format(res[2] * res[3])

    @staticmethod
    def get_character_equal_values(word1, word2):
        for i in range(len(word1)):
            yield word1[i] == word2[i]

    @staticmethod
    def get_resulting_word(word, equality):
        return "".join([word[i] for i in range(len(word)) if equality[i]])

    def part2(self, input_data):
        for i in range(len(input_data)):
            for j in range(i, len(input_data)):
                word1, word2 = input_data[i], input_data[j]
                if word1 == word2:
                    continue
                equality = list(self.get_character_equal_values(word1, word2))
                if len([x for x in equality if not x]) == 1:
                    yield "Found words with only one differing character! {} and {}.".format(word1, word2)
                    yield "Without the differing letter, this is {}".format(self.get_resulting_word(word1, equality))
