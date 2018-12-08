from typing import List, Tuple

from days import AOCDay, day


class Node:
    def __init__(self, identifier: str, num_leaves: int, num_metadata: int):
        self.identifier = identifier
        self.num_leaves = num_leaves
        self.num_metadata = num_metadata
        self.leaves = []
        self.metadata = []

    def add_leaf(self, leaf: 'Node'):
        self.leaves.append(leaf)

    def add_metadata(self, metadata: int):
        self.metadata.append(metadata)

    def sum_metadata(self) -> int:
        node = sum(self.metadata)
        leaves = sum(x.sum_metadata() for x in self.leaves)
        return node + leaves

    def get_value(self) -> int:
        if len(self.leaves) == 0:
            value = sum(self.metadata)
        else:
            value = 0
            for i in self.metadata:
                if i > 0:
                    try:
                        node: 'Node' = self.leaves[i-1]
                        value += node.get_value()
                    except IndexError:
                        pass
        return value

    def __str__(self):
        return "{} ({}) ({}) \nchildren:\n{}\nmetadata:\n{}".format(
            self.identifier, self.num_leaves, self.num_metadata,
            "\n".join([str(x) for x in self.leaves]),
            ",".join([str(x) for x in self.metadata])
        )


@day(8)
class DayEight(AOCDay):
    test_input = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    current_identifier = "A"
    root_node = None

    def parse_node(self, input_data: List[int]) -> Tuple[Node, int]:
        i = 0
        node = None
        while i < len(input_data):
            # Parse a header (2 numbers)
            num_leaves = input_data[i]
            i += 1
            num_metadata = input_data[i]
            i += 1
            node = Node(self.current_identifier, num_leaves, num_metadata)
            self.current_identifier = chr(ord(self.current_identifier) + 1)
            for j in range(num_leaves):
                leaf, end_index = self.parse_node(input_data[i:])
                i += end_index
                node.add_leaf(leaf)
            for k in range(num_metadata):
                metadata = input_data[i]
                i += 1
                node.add_metadata(metadata)
            break
        return node, i

    def common(self, input_data):
        # input_data = self.test_input
        self.current_identifier = "A"
        input_data = [int(x) for x in input_data.split()]
        self.root_node, leftover = self.parse_node(input_data)
        assert leftover == len(input_data)

    def part1(self, input_data):
        yield "Sum of metadata is {}".format(self.root_node.sum_metadata())

    def part2(self, input_data):
        yield "Value of root node is {}".format(self.root_node.get_value())
