from enum import Enum, IntEnum
from typing import Tuple, List, Optional

from days import AOCDay, day


class Cart:
    class Direction(Enum):
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4

        @staticmethod
        def from_char(char):
            return {
                ">": Cart.Direction.RIGHT,
                "v": Cart.Direction.DOWN,
                "^": Cart.Direction.UP,
                "<": Cart.Direction.LEFT
            }[char]

    class TurnDirection(IntEnum):
        LEFT = 1
        STRAIGHT = 2
        RIGHT = 3

    direction: Direction
    current_position: Tuple[int, int]
    next_corner: TurnDirection

    def __init__(self, direction: Direction, position: Tuple[int, int]):
        self.direction = direction
        self.current_position = position
        self.next_corner = Cart.TurnDirection.LEFT

    def __str__(self):
        return "Cart on ({},{}) going {}, turning {}".format(self.current_position[0], self.current_position[1],
                                                             self.direction, self.next_corner)

    def __repr__(self):
        return {
            Cart.Direction.LEFT: "<",
            Cart.Direction.RIGHT: ">",
            Cart.Direction.UP: "^",
            Cart.Direction.DOWN: "v",
        }[self.direction]

    turn_results = {
        Direction.LEFT: {
            TurnDirection.LEFT: (Direction.DOWN, TurnDirection.STRAIGHT),
            TurnDirection.STRAIGHT: (Direction.LEFT, TurnDirection.RIGHT),
            TurnDirection.RIGHT: (Direction.UP, TurnDirection.LEFT),
        },
        Direction.UP: {
            TurnDirection.LEFT: (Direction.LEFT, TurnDirection.STRAIGHT),
            TurnDirection.STRAIGHT: (Direction.UP, TurnDirection.RIGHT),
            TurnDirection.RIGHT: (Direction.RIGHT, TurnDirection.LEFT),
        },
        Direction.DOWN: {
            TurnDirection.LEFT: (Direction.RIGHT, TurnDirection.STRAIGHT),
            TurnDirection.STRAIGHT: (Direction.DOWN, TurnDirection.RIGHT),
            TurnDirection.RIGHT: (Direction.LEFT, TurnDirection.LEFT),
        },
        Direction.RIGHT: {
            TurnDirection.LEFT: (Direction.UP, TurnDirection.STRAIGHT),
            TurnDirection.STRAIGHT: (Direction.RIGHT, TurnDirection.RIGHT),
            TurnDirection.RIGHT: (Direction.DOWN, TurnDirection.LEFT),
        },
    }

    def turn(self):
        self.direction, self.next_corner = self.turn_results[self.direction][self.next_corner]

    def turn_corner(self, corner):
        self.direction = {
            "\\": {
                Cart.Direction.RIGHT: Cart.Direction.DOWN,
                Cart.Direction.UP: Cart.Direction.LEFT,
                Cart.Direction.LEFT: Cart.Direction.UP,
                Cart.Direction.DOWN: Cart.Direction.RIGHT,
            },
            "/": {
                Cart.Direction.LEFT: Cart.Direction.DOWN,
                Cart.Direction.UP: Cart.Direction.RIGHT,
                Cart.Direction.DOWN: Cart.Direction.LEFT,
                Cart.Direction.RIGHT: Cart.Direction.UP,
            }
        }[corner][self.direction]

    def get_velocity(self):
        return {
            Cart.Direction.LEFT: (-1, 0),
            Cart.Direction.RIGHT: (1, 0),
            Cart.Direction.UP: (0, -1),
            Cart.Direction.DOWN: (0, 1)
        }[self.direction]

    def tick(self, track: List[List[str]], carts: List['Cart']) -> bool:
        delta_x, delta_y = self.get_velocity()
        new_x, new_y = (self.current_position[0] + delta_x), (self.current_position[1] + delta_y)
        collision = False

        # If new piece of track is a +, turn.
        if track[new_y][new_x] == "+":
            self.turn()

        # If new piece of track is a corner, turn.
        if track[new_y][new_x] in "/\\":
            self.turn_corner(track[new_y][new_x])

        # If new piece of track is a cart, collision.
        if get_cart(carts, new_x, new_y) is not None:
            collision = True

        self.current_position = new_x, new_y
        return collision


def get_cart(carts, x, y) -> Optional[List[Cart]]:
    carts = filter(lambda c: c.current_position == (x, y), carts)
    res = list(carts)
    return res if res else None


@day(13)
class DayThirteen(AOCDay):
    test_input = """/->-\        
|   |  /----\\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """
    track: List[List[str]] = []
    carts: List[Cart] = []

    cart_to_line = {
        ">": "-",
        "v": "|",
        "^": "|",
        "<": "-",
    }

    def print_track(self):
        result = ""
        for y in range(len(self.track)):
            for x in range(len(self.track[y])):
                cart = get_cart(self.carts, x, y)
                if cart is not None and len(cart) == 1:
                    result += repr(cart[0])
                elif cart is not None and len(cart) > 1:
                    result += "X"
                else:
                    result += self.track[y][x]
            result += "\n"
        return result

    def sort_carts(self):
        coord_carts = [(cart.current_position, cart) for cart in self.carts]
        sorted_carts = sorted(coord_carts, key=lambda x: x[0])
        return [x[1] for x in sorted_carts]

    def common(self, input_data):
        # input_data = self.test_input.split("\n")
        self.track = []
        self.carts = []
        for y in range(len(input_data)):
            self.track.append([])
            for x in range(len(input_data[y])):
                self.track[-1].append(input_data[y][x])
                if input_data[y][x] in [">", "v", "^", "<"]:
                    self.carts.append(Cart(Cart.Direction.from_char(input_data[y][x]), (x, y)))
                    self.track[-1][-1] = self.cart_to_line[input_data[y][x]]

        yield self.carts

    def part1(self, input_data):
        yield self.print_track()
        while True:
            sorted_carts = self.sort_carts()
            for c in sorted_carts:
                collision = c.tick(self.track, self.carts)
                if collision:
                    yield self.print_track()
                    yield "Collision on ({},{})!".format(c.current_position[0], c.current_position[1])
                    return
            # yield self.print_track()

    def part2(self, input_data):
        yield self.print_track()
        while True:
            sorted_carts = self.sort_carts()
            for c in sorted_carts:
                collision = c.tick(self.track, self.carts)
                if collision:
                    yield "Collision on ({},{})!".format(c.current_position[0], c.current_position[1])
                    # Remove the two carts
                    carts = get_cart(self.carts, c.current_position[0], c.current_position[1])
                    for cart in carts:
                        self.carts.remove(cart)

                    if len(self.carts) <= 1:
                        c = self.carts[0]
                        c.tick(self.track, self.carts)
                        yield self.print_track()
                        yield "One cart left on position ({},{})!".format(c.current_position[0], c.current_position[1])
                        return
            # yield self.print_track()
