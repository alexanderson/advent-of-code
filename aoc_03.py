import math

import itertools

TEST_INPUTS_A = {
    1: 0,
    12: 3,
    23: 2,
    1024: 31
}

INPUT = 265149

"""
37  36  35  34  33  32  31
38  17  16  15  14  13  30
39  18   5   4   3  12  29
40  19   6   1   2  11  28
41  20   7   8   9  10  27
42  21  22  23  24  25  26
43  44  45  46  47  48  49
"""


def manhattan_dist(location):
    if location == 1:
        return 0

    layer = _layer(location)
    layer_max = ((2 * layer) + 1) ** 2
    diff = layer_max - location  # steps from bottom left corner
    steps_from_corner = diff % (2 * layer)  # any corner, clockwise

    if steps_from_corner < layer:
        return 2 * layer - steps_from_corner
    else:
        return steps_from_corner


def _layer(location):
    return int(
        math.floor(
            (math.sqrt(location - 1) + 1) / 2
        )
    )


def aoc_03b(target):
    position = 1
    value = 1
    coords = (0, 0)
    all_values = {
        coords: value
    }
    while value < target:
        position += 1
        coords = _next(coords)
        value = _value(coords, all_values)
        all_values[coords] = value
    return value


def _next(curr_coords):
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
    for location, distance in TEST_INPUTS_A.items():
        assert manhattan_dist(location) == distance, location

    part_a = manhattan_dist(INPUT)
    print('part a: {}'.format(part_a))

    part_b = aoc_03b(INPUT)
    print('part b: {}'.format(part_b))


if __name__ == '__main__':
    main()
