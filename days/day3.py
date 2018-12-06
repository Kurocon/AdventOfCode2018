import re
from collections import defaultdict

from days import AOCDay, day


@day(3)
class DayThree(AOCDay):

    PARSE_REGEX = r'#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)'
    parsed_input = []

    def common(self, input_data):
        self.parsed_input = []
        for line in input_data:
            match = re.match(self.PARSE_REGEX, line)
            if match:
                self.parsed_input.append({
                    'claim_id': int(match.group(1)),
                    'x_offset': int(match.group(2)),
                    'y_offset': int(match.group(3)),
                    'width': int(match.group(4)),
                    'height': int(match.group(5))
                })
            else:
                yield "Error: No match for line {}".format(line)

    def part1(self, input_data):
        squares = defaultdict(list)
        for line in self.parsed_input:
            x_squares = [(x+line['x_offset'], line['y_offset']) for x in range(line['width'])]
            claim_squares = [(x, y+i) for x, y in x_squares for i in range(line['height'])]
            for square in claim_squares:
                squares[square].append(line['claim_id'])

        overlapping_squares = sum([1 for key, value in squares.items() if len(value) > 1])
        yield "There are {} overlapping squares".format(overlapping_squares)

    def part2(self, input_data):
        squares = defaultdict(list)
        for line in self.parsed_input:
            x_squares = [(x+line['x_offset'], line['y_offset']) for x in range(line['width'])]
            claim_squares = [(x, y+i) for x, y in x_squares for i in range(line['height'])]
            for square in claim_squares:
                squares[square].append(line['claim_id'])

        unique_claims = set(x['claim_id'] for x in self.parsed_input)
        overlapping_claims = set()
        for key, value in squares.items():
            if len(value) > 1:
                for v in value:
                    overlapping_claims.add(v)

        result = unique_claims - overlapping_claims
        yield "The unique claim is {}".format(result)

