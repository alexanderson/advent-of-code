import itertools

TEST_POWERS = (
    # x, y, serial, power
    (3, 5, 8, 4),
    (122, 79, 57, -5),
    (217, 196, 39, 0),
    (101, 153, 71, 4)
)
TEST_GRID_POWER_FIXED = (
    # serial, power, coords
    (18, 29, (33, 45)),
    (42, 30, (21, 61))
)
TEST_GRID_POWER_ANY_SIZE = (
    # serial, power, (x, y, size)
    (18, 113, (90, 269, 16)),
    (42, 119, (232, 251, 12))
)
GRID_SIZE = 300
SERIAL = 9445


def get_power(x, y, serial):
    rack_id = x + 10
    power = rack_id * y
    power += serial
    power *= rack_id
    power = int(str(power)[-3])
    power -= 5
    return power


def get_max_power_any_size(grid):
    largest_power = 0
    coords = None
    for size in range(1, GRID_SIZE + 1):
        print(size)
        power, (x, y) = get_max_power_fixed_section(grid, size)
        if not coords:
            largest_power = power
            coords = (x, y, size)
        if power > largest_power:
            largest_power = power
            coords = (x, y, size)
    return coords


def get_max_power_fixed_section(grid, size):
    largest_power = 0
    coords = None
    for section in get_sections(size):
        power = sum(grid[y][x] for x, y in section)
        if not coords:
            largest_power = power
            coords = section[0]
            coords = (coords[0] + 1, coords[1] + 1)
        if power > largest_power:
            largest_power = power
            coords = section[0]
            coords = (coords[0] + 1, coords[1] + 1)

    return largest_power, coords


def build_grid_of_powers(serial):
    return [
        [
            get_power(x + 1, y + 1, serial)
            for x in range(GRID_SIZE)
        ]
        for y in range(GRID_SIZE)
    ]


def get_sections(size):
    for top_left_y in range(GRID_SIZE - size + 1):
        for top_left_x in range(GRID_SIZE - size + 1):
            yield tuple(
                (top_left_x + i, top_left_y + j)
                for i, j in
                itertools.product(range(size), range(size))
            )


def test_cell_power():
    for x, y, serial, expected_power in TEST_POWERS:
        power = get_power(x, y, serial)
        assert power == expected_power, f'{power} != {expected_power}'


def test_grid_power_fixed_section():
    for serial, expected_power, expected_coords in TEST_GRID_POWER_FIXED:
        grid = build_grid_of_powers(serial)
        power, coords = get_max_power_fixed_section(grid, size=3)
        assert power == expected_power, f'{power} != {expected_power}'
        assert coords == expected_coords, f'{coords} != {expected_coords}'


def test_grid_power_any_size():
    for serial, expected_power, expected_coords in TEST_GRID_POWER_ANY_SIZE:
        grid = build_grid_of_powers(serial)
        power, coords = get_max_power_any_size(grid)
        assert power == expected_power, f'{power} != {expected_power}'
        assert coords == expected_coords, f'{coords} != {expected_coords}'


def main():
    test_cell_power()
    test_grid_power_fixed_section()
    test_grid_power_any_size()

    grid = build_grid_of_powers(SERIAL)
    print(grid)
    exit()
    power, coords = get_max_power_fixed_section(grid, 3)
    print(power, coords)

    power, coords = get_max_power_any_size(grid)
    print(power, coords)


if __name__ == '__main__':
    main()
