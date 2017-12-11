import collections

import utils

TEST_INPUT = {
    'ne,ne,ne': 3,
    'ne,ne,sw,sw': 0,
    'ne,ne,s,s': 2,
    'se,sw,se,sw,sw': 3
}

DIRECTIONS = ('n', 'ne', 'se', 's', 'sw', 'nw')


def min_steps(directions):
    direction_counts = collections.Counter(directions)
    direction_counts = _reduce(direction_counts)
    return sum(direction_counts.values())


def max_steps(full_directions):
    directions = []
    furthest = 0
    for direction in full_directions:
        directions.append(direction)
        steps = min_steps(directions)
        if steps > furthest:
            furthest = steps
    return furthest


def _reduce(counts):
    counts = _distill_net_counts(counts)
    counts = _reduce_triangle(counts)
    return counts


def _reduce_triangle(counts):
    counts = counts.copy()
    for idx, direction in enumerate(DIRECTIONS):
        dir_a = DIRECTIONS[idx - 2]
        dir_b = DIRECTIONS[idx - 4]
        net_dir = DIRECTIONS[idx - 3]
        common_step = min(counts[dir_a], counts[dir_b])
        if common_step:
            counts[net_dir] += common_step
            counts[dir_a] -= common_step
            counts[dir_b] -= common_step

    return counts


def _distill_net_counts(counts):
    counts = counts.copy()
    pairs = (
        ('n', 's'),
        ('ne', 'sw'),
        ('nw', 'se')
    )
    for forward, backwards in pairs:
        net_forward = counts[forward] - counts[backwards]
        if net_forward > 0:
            counts[forward] = net_forward
            counts[backwards] = 0
        elif net_forward < 0:
            counts[backwards] = abs(net_forward)
            counts[forward] = 0
        else:
            counts[forward] = counts[backwards] = 0
    return counts


def main():
    test()

    input_directions = utils.get_input_data(11).split(',')
    steps = min_steps(input_directions)
    print(f'part a: {steps}')
    furthest = max_steps(input_directions)
    print(f'part b: {furthest}')


def test():
    for directions, expected_min_steps in TEST_INPUT.items():
        directions = directions.split(',')
        assert min_steps(directions) == expected_min_steps


if __name__ == '__main__':
    main()
