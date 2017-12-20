import itertools

from aoc_10 import Loop


TEST_INPUT = 'flqrgnkx'
INPUT_DATA = 'stpzcrnm'


def knot_hash_inputs(input_data):
    return [
        '-'.join((input_data, str(i)))
        for i in range(128)
    ]


def knot_hash(input_data):
    return Loop().dense_hash(input_data)


def hash_to_binary(hex_knot_hash):
    return ''.join(char_to_binary(char) for char in hex_knot_hash)


def char_to_binary(hex_char):
    assert len(hex_char) == 1
    bin_str = bin(int(hex_char, base=16))
    return '{:04}'.format(int(bin_str[2:]))


def create_grid(hashes):
    return [
        [
            int(char)
            for char in hash_to_binary(hash_)
        ]
        for hash_ in hashes
    ]


def filled_squares(grid):
    return sum(
        sum(
            int(char) for char in row
        )
        for row in grid
    )


def num_regions(grid):
    regions = 0
    seen_coords = set()

    # cheeky way to move around a region recursively marking as seen
    def mark_coords_in_region_as_seen(x, y):
        list(_mark_coords_in_region_as_seen(x, y))

    def _mark_coords_in_region_as_seen(x, y):
        seen_coords.add((x, y))
        for a, b in adjacent_coords(x, y):
            if (a, b) not in seen_coords and grid[a][b]:
                yield from _mark_coords_in_region_as_seen(a, b)

    for i, j in all_coords():

        if (i, j) not in seen_coords and grid[i][j]:
            regions += 1
            mark_coords_in_region_as_seen(i, j)

    return regions


def all_coords():
    yield from itertools.product(range(128), range(128))


def adjacent_coords(i, j):
    for step in (-1, 1):

        if 0 <= (i + step) < 128:
            yield i + step, j

        if 0 <= (j + step) < 128:
            yield i, j + step


def main():
    test()

    hash_inputs = knot_hash_inputs(INPUT_DATA)
    hashes = map(knot_hash, hash_inputs)
    grid = create_grid(hashes)
    print(f'part a: {filled_squares(grid)}')
    print(f'part b: {num_regions(grid)}')


def test():
    assert char_to_binary('0') == '0000'
    assert char_to_binary('e') == '1110'

    binary_hash = hash_to_binary('a0c2017')
    assert binary_hash == '1010000011000010000000010111', binary_hash

    hash_inputs = knot_hash_inputs(TEST_INPUT)
    assert hash_inputs[:3] == [
        'flqrgnkx-0',
        'flqrgnkx-1',
        'flqrgnkx-2'
    ]

    hashes = map(knot_hash, hash_inputs)
    grid = create_grid(hashes)
    total_filled_squares = filled_squares(grid)

    assert total_filled_squares == 8108, total_filled_squares

    assert set(adjacent_coords(0, 0)) == {(1, 0), (0, 1)}
    assert set(adjacent_coords(5, 5)) == {(4, 5), (5, 4), (5, 6), (6, 5)}
    assert set(adjacent_coords(127, 9)) == {(126, 9), (127, 8), (127, 10)}

    regions = num_regions(grid)
    assert regions == 1242, regions


if __name__ == '__main__':
    main()
