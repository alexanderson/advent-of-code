import collections


TEST_COORDS = (
    '1, 1',
    '1, 6',
    '8, 3',
    '3, 4',
    '5, 5',
    '8, 9'
)
TEST_MIN_TOTAL_DISTANCE = 32
TEST_REGION_A_SIZE = 17
TEST_REGION_B_SIZE = 16
MIN_TOTAL_DISTANCE = 10000


Point = collections.namedtuple('Point', 'x y')
Location = collections.namedtuple('Location', 'id x y')


def get_locations(raw_coords):
    locations = []
    for id_, coord in enumerate(raw_coords):
        x, y = coord.split(', ')
        location = Location(id_, int(x), int(y))
        locations.append(location)
    return locations


def biggest_finite_area(grid):
    ignore_locations = set()
    areas = collections.defaultdict(int)

    for j, row in enumerate(grid):
        for i, closest_location in enumerate(row):
            areas[closest_location] += 1
            if on_edge(i, j, grid):
                ignore_locations.add(closest_location)

    for edge_location in ignore_locations:
        del areas[edge_location]

    return max(areas.values())


def on_edge(i, j, grid):
    height = len(grid) - 1
    width = len(grid[0]) - 1
    return (
        i in (0, width) or
        j in (0, height)
    )


def size_of_closest_region(locations, min_total_distance):
    region_size = 0
    min_x, min_y, max_x, max_y = grid_limits(locations)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            point = Point(x, y)
            if total_location_distance(point, locations) < min_total_distance:
                region_size += 1
    return region_size


def total_location_distance(point, locations):
    return sum(manhattan_distance(point, location) for location in locations)


def build_grid(locations):
    min_x, min_y, max_x, max_y = grid_limits(locations)
    return [
        [
            find_closest_location(Point(x, y), locations)
            for x in range(min_x, max_x + 1)
        ]
        for y in range(min_y, max_y + 1)
    ]


def grid_limits(locations):
    min_x = min(locations, key=lambda l: l.x).x
    min_y = min(locations, key=lambda l: l.y).y
    max_x = max(locations, key=lambda l: l.x).x
    max_y = max(locations, key=lambda l: l.y).y
    return (
        min_x - 2,
        min_y - 2,
        max_x + 2,
        max_y + 2
    )


def find_closest_location(point, locations):
    closest_distance = None
    closest_locations = set()
    for location in locations:
        distance = manhattan_distance(point, location)
        if closest_distance is None:
            closest_distance = distance
            closest_locations.add(location)
        elif distance < closest_distance:
            closest_distance = distance
            closest_locations = {location}
        elif distance == closest_distance:
            closest_locations.add(location)

    if len(closest_locations) > 1:
        return None
    assert len(closest_locations) == 1
    closest_location = closest_locations.pop()
    return closest_location


def manhattan_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def test_biggest_area():
    locations = get_locations(TEST_COORDS)
    grid = build_grid(locations)
    area = biggest_finite_area(grid)
    assert area == TEST_REGION_A_SIZE, area


def test_size_of_closest_region():
    locations = get_locations(TEST_COORDS)
    size = size_of_closest_region(locations, TEST_MIN_TOTAL_DISTANCE)
    assert size == TEST_REGION_B_SIZE, size


def get_coords():
    with open('input.txt') as input_file:
        coords = input_file.readlines()
    return [coord.strip() for coord in coords]


def main():
    coords = get_coords()
    locations = get_locations(coords)
    grid = build_grid(locations)
    area = biggest_finite_area(grid)
    print(area)

    closest_region_size = size_of_closest_region(locations, MIN_TOTAL_DISTANCE)
    print(closest_region_size)


if __name__ == '__main__':
    test_biggest_area()
    test_size_of_closest_region()

    main()
