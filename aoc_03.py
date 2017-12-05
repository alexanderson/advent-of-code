import itertools
import math


TEST_INPUTS_A = {
    1: 0,
    12: 3,
    23: 2,
    1024: 31
}

INPUT = 265149


def manhattan_dist(location):
    """The manhattan distance.

    Calculates which layer the location is on, and where in that layer it is,
    then knowing that the corners are `2 * layer` steps from the centre and the
    midpoints are `layer` steps from the centre, calculates the minimum steps
    to the centre from `location`.

    2 2 2 2 2    layer = 2
    * 1 1 1 2    steps from layer_max = 7
    ^ 1 0 1 2    steps from corner = 3
    | 1 1 1 2    therefore steps from center = 3
    | 2 2 2 2

    """
    if location == 1:
        return 0

    layer = get_layer(location)

    # largest number on that layer
    layer_max = ((2 * layer) + 1) ** 2

    # number of steps, backwards/clockwise, from bottom left corner of layer
    diff = layer_max - location

    # number of clockwise steps from nearest corner
    steps_from_corner = diff % (2 * layer)

    if steps_from_corner < layer:
        return 2 * layer - steps_from_corner
    else:
        return steps_from_corner


def get_layer(location):
    """layer from centre, i.e.

    2 2 2 2 2
    2 1 1 1 2
    2 1 0 1 2
    2 1 1 1 2
    2 2 2 2 2
    """
    return int(
        math.floor(
            (math.sqrt(location - 1) + 1) / 2
        )
    )


def aoc_03b(target):
    """Iterate around the spiral, recoding sum of adjacent, known squares
    until target is reached.

    :returns: first value larger than target to be written.
    """
    position = 1
    value = 1
    coordinates = (0, 0)

    all_values = {
        coordinates: value
    }

    while value < target:
        position += 1
        coordinates = next_coordinates(coordinates)
        value = _value(coordinates, all_values)

        all_values[coordinates] = value

    return value


def next_coordinates(curr_coords):
    """Get coordinates of next square in spiral."""
    x, y = curr_coords
    layer = max(abs(x), abs(y))
    if y == -layer:
        return x + 1, y
    if x == -layer:
        return x, y - 1
    if y == layer:
        return x - 1, y
    if x == layer:
        return x, y + 1
    else:
        raise ValueError('Incorrect coords {}'.format(curr_coords))


def _value(coords, all_values):
    x, y = coords
    all_local_coords = itertools.product(
        [-1, 0, 1],
        [-1, 0, 1]
    )
    surrounding_coords = (
        (x + x_diff, y + y_diff)
        for x_diff, y_diff in
        all_local_coords
        if (x_diff, y_diff) != (0, 0)
    )
    return sum(
        all_values.get(adjacent_coord, 0)
        for adjacent_coord in surrounding_coords
    )


def main():
    test()

    part_a = manhattan_dist(INPUT)
    print('part a: {}'.format(part_a))

    part_b = aoc_03b(INPUT)
    print('part b: {}'.format(part_b))


def test():
    for location, distance in TEST_INPUTS_A.items():
        assert manhattan_dist(location) == distance, location


if __name__ == '__main__':
    main()
