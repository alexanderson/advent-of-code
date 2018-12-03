import collections
import re


CUTOUT_RE = re.compile(
    r'#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<width>\d+)x(?P<height>\d+)'
)

Cutout = collections.namedtuple('Cutout', 'id x y width height')


class Fabric:

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._grid = [
            [set() for _ in range(self._width)]
            for _ in range(self._height)
        ]

    def add_cutout(self, cutout):
        for y, x in coords(cutout):
            self._grid[y][x].add(cutout.id)

    def overlaps(self):
        overlaps = 0
        for row in self._grid:
            for cell in row:
                if len(cell) > 1:
                    overlaps += 1
        return overlaps

    def isolated_cutouts(self):
        all_ids = set()
        overlapping_ids = set()
        for row in self._grid:
            for cell in row:
                all_ids |= cell
                if len(cell) > 1:
                    overlapping_ids |= cell
        return all_ids - overlapping_ids


def get_cutouts():
    with open('input.txt') as input_file:
        instructions = input_file.readlines()
    lines = (line.rstrip('\n') for line in instructions)
    return [
        parse(line)
        for line in lines
        if line
    ]


def parse(cutout):
    match = CUTOUT_RE.match(cutout)
    assert match, cutout
    groups = match.groupdict()
    return Cutout(
        id=int(groups['id']),
        x=int(groups['x']),
        y=int(groups['y']),
        width=int(groups['width']),
        height=int(groups['height']),
    )


def grid_size(cutouts):
    width = 0
    height = 0
    for cutout in cutouts:
        width = max(width, cutout.x + cutout.width)
        height = max(height, cutout.y + cutout.height)
    return (
        width + 1,
        height + 1
    )


def coords(cutout):
    for y in range(cutout.y, cutout.y + cutout.height):
        for x in range(cutout.x, cutout.x + cutout.width):
            yield y, x


def test_overlap():
    fabric = Fabric(8, 8)
    instructions = (
        '#1 @ 1,3: 4x4',
        '#2 @ 3,1: 4x4',
        '#3 @ 5,5: 2x2',
    )
    for instruction in instructions:
        cutout = parse(instruction)
        fabric.add_cutout(cutout)
    overlaps = fabric.overlaps()
    assert overlaps == 4, '{} != 4'.format(overlaps)

    isolated_cutouts = fabric.isolated_cutouts()
    assert isolated_cutouts == {3}, isolated_cutouts


if __name__ == '__main__':
    test_overlap()

    cutouts = get_cutouts()
    width, height = grid_size(cutouts)
    fabric = Fabric(width, height)
    for cutout in cutouts:
        fabric.add_cutout(cutout)

    overlaps = fabric.overlaps()
    print(overlaps)

    isolated_cutouts = fabric.isolated_cutouts()
    print(isolated_cutouts)
