import enum
import string

import utils

TEST_INPUT = '\n'.join((
    '     |          ',
    '     |  +--+    ',
    '     A  |  C    ',
    ' F---|----E|--+ ',
    '     |  |  |  D ',
    '     +B-+  +--+ ',
    '                '
))


def direction_valid(direction, tile):
    if tile == '|':
        return direction in Direction.UP, Direction.DOWN
    elif tile == '-':
        return direction in Direction.LEFT, Direction.RIGHT


class Finished(Exception):
    pass


class Diagram:

    def __init__(self, input_data):
        self._grid = [
            list(row)
            for row in input_data.split('\n')
        ]
        self.pointer = Pointer(*self.start())
        self.path = ''
        self.steps = 0

    def start(self):
        return self._grid[0].index('|'), 0

    def get(self, pointer):
        x, y = pointer.coords()
        return self._grid[y][x]

    def run(self):
        try:
            while True:
                self.move()
        except Finished:
            return

    def move(self):

        tile = self.get(self.pointer)

        if tile in '|-':
            self.steps += 1
            self.pointer.move()

        elif tile == '+':
            self.change_direction()
            self.steps += 1
            self.pointer.move()

        elif tile in string.ascii_uppercase:
            self.path += tile
            self.steps += 1
            self.pointer.move()

        else:
            raise Finished

    def change_direction(self):
        current_direction = self.pointer.direction
        if current_direction in (Direction.UP, Direction.DOWN):
            options = Direction.LEFT, Direction.RIGHT
        elif current_direction in (Direction.LEFT, Direction.RIGHT):
            options = Direction.UP, Direction.DOWN
        else:
            raise Exception('Invalid direction')

        for direction in options:
            try:
                temp_pointer = Pointer(
                    self.pointer.x,
                    self.pointer.y,
                    direction
                )
                temp_pointer.move()
                tile = self.get(temp_pointer)
                valid_direction = (
                    tile in string.ascii_uppercase or
                    (
                        direction in (Direction.LEFT, Direction.RIGHT) and
                        tile == '-'
                    ) or
                    (
                        direction in (Direction.UP, Direction.DOWN) and
                        tile == '|'
                    )
                )
                if valid_direction:
                    self.pointer.direction = direction
                    return
            except IndexError:
                continue

        raise Exception(f'No direction to turn:\n{self.local()}')

    def local(self):
        x_values = [self.pointer.x + step for step in (-1, 0, 1)]
        y_values = [self.pointer.y + step for step in (-1, 0, 1)]
        return '\n'.join(
            ''.join(
                self.get(Pointer(x, y))
                for x in x_values
                if x >= 0
            )
            for y in y_values
            if y >= 0
        )


class Direction(enum.Enum):
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class Pointer:

    def __init__(self, x, y, direction=Direction.DOWN):
        self.x = x
        self.y = y
        self.direction = direction

    def coords(self):
        return self.x, self.y

    def move(self):
        if self.direction == Direction.DOWN:
            self.y += 1
        elif self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.LEFT:
            self.x -= 1
        elif self.direction == Direction.RIGHT:
            self.x += 1


def main():
    test()

    input_data = utils.get_input_data(19, strip=False)
    diagram = Diagram(input_data)
    diagram.run()
    print(f'part a: {diagram.path}')
    print(f'part b: {diagram.steps}')


def test():
    diagram = Diagram(TEST_INPUT)
    diagram.run()
    assert diagram.path == 'ABCDEF', diagram.path
    assert diagram.steps == 38, diagram.steps


if __name__ == '__main__':
    main()
