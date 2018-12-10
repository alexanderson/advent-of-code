import re

TEST_PARTICLES = (
    'position=< 9,  1> velocity=< 0,  2>',
    'position=< 7,  0> velocity=<-1,  0>',
    'position=< 3, -2> velocity=<-1,  1>',
    'position=< 6, 10> velocity=<-2, -1>',
    'position=< 2, -4> velocity=< 2,  2>',
    'position=<-6, 10> velocity=< 2, -2>',
    'position=< 1,  8> velocity=< 1, -1>',
    'position=< 1,  7> velocity=< 1,  0>',
    'position=<-3, 11> velocity=< 1, -2>',
    'position=< 7,  6> velocity=<-1, -1>',
    'position=<-2,  3> velocity=< 1,  0>',
    'position=<-4,  3> velocity=< 2,  0>',
    'position=<10, -3> velocity=<-1,  1>',
    'position=< 5, 11> velocity=< 1, -2>',
    'position=< 4,  7> velocity=< 0, -1>',
    'position=< 8, -2> velocity=< 0,  1>',
    'position=<15,  0> velocity=<-2,  0>',
    'position=< 1,  6> velocity=< 1,  0>',
    'position=< 8,  9> velocity=< 0, -1>',
    'position=< 3,  3> velocity=<-1,  1>',
    'position=< 0,  5> velocity=< 0, -1>',
    'position=<-2,  2> velocity=< 2,  0>',
    'position=< 5, -2> velocity=< 1,  2>',
    'position=< 1,  4> velocity=< 2,  1>',
    'position=<-2,  7> velocity=< 2, -2>',
    'position=< 3,  6> velocity=<-1, -1>',
    'position=< 5,  0> velocity=< 1,  0>',
    'position=<-6,  0> velocity=< 2,  0>',
    'position=< 5,  9> velocity=< 1, -2>',
    'position=<14,  7> velocity=<-2,  0>',
    'position=<-3,  6> velocity=< 2, -1>',
)

PARTICLE_RE = re.compile(
    r'position=<(?P<x>(-|\s)?\d+),\s+(?P<y>(-|\s)?\d+)>\s'
    r'velocity=<(?P<vx>(-|\s)?\d+),\s+(?P<vy>(-|\s)?\d+)>'
)


class Grid:

    def __init__(self, particles):
        self.particles = particles

    def tick(self, seconds=1):
        for particle in self.particles:
            particle.tick(seconds)

    def find_message(self):
        area = self.get_area()
        time = 0
        while True:
            self.tick()
            new_area = self.get_area()
            if new_area > area:
                self.tick(-1)
                return str(self), time
            time += 1
            area = new_area

    def get_area(self):
        min_x, min_y, max_x, max_y = self.get_min_and_max_coords()
        dx = max_x - min_x
        dy = max_y - min_y
        return dx * dy

    def get_min_and_max_coords(self):
        min_x = None
        min_y = None
        max_x = None
        max_y = None
        for particle in self.particles:
            min_x = min(particle.x, min_x if min_x is not None else particle.x)
            min_y = min(particle.y, min_y if min_y is not None else particle.y)
            max_x = max(particle.x, max_x if max_x is not None else particle.x)
            max_y = max(particle.y, max_y if max_y is not None else particle.y)
        return min_x, min_y, max_x, max_y

    def __str__(self):
        min_x, min_y, max_x, max_y = self.get_min_and_max_coords()
        grid = [
            ['.' for _ in range(min_x, max_x + 1)]
            for __ in range(min_y, max_y + 1)
        ]
        for particle in self.particles:
            grid[particle.y - min_y][particle.x - min_x] = '#'

        return '\n'.join(''.join(row) for row in grid)


class Particle:

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def tick(self, seconds=1):
        self.x += self.vx * seconds
        self.y += self.vy * seconds


def parse_particle(line):
    match = PARTICLE_RE.match(line)
    groups = match.groupdict()
    return Particle(
        int(groups['x']),
        int(groups['y']),
        int(groups['vx']),
        int(groups['vy'])
    )


def get_input():
    with open('input.txt') as input_file:
        return [
            line.rstrip('\n')
            for line in input_file.readlines()
        ]


def test_message():
    particles = [parse_particle(line) for line in TEST_PARTICLES]
    grid = Grid(particles)
    message, time = grid.find_message()
    assert time == 3, time
    assert message == '\n'.join((
        '#...#..###',
        '#...#...#.',
        '#...#...#.',
        '#####...#.',
        '#...#...#.',
        '#...#...#.',
        '#...#...#.',
        '#...#..###'
    )), message


def main():
    test_message()

    particles = [parse_particle(line) for line in get_input()]
    grid = Grid(particles)
    message, time = grid.find_message()
    print(message)
    print(time)



if __name__ == '__main__':
    main()
