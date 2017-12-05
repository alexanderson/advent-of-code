TEST_INPUT = (0, 3, 0, 1, -3)


def increment_jumps(jump):
    return jump + 1


def decrement_large_jumps(jump):
    if jump >= 3:
        return jump - 1
    return jump + 1


def aoc_05(data, jump_modifier=increment_jumps):
    data = list(data)
    size = len(data)
    position = 0
    total_jumps = 0

    while True:
        if position < 0 or position >= size:
            return total_jumps

        jump = data[position]
        data[position] = jump_modifier(jump)
        position += jump
        total_jumps += 1


def read_input(path):
    with open(path) as f:
        return [
            int(line.strip())
            for line in f.readlines()
            if line
        ]


def main():
    assert aoc_05(TEST_INPUT) == 5
    assert aoc_05(TEST_INPUT, decrement_large_jumps) == 10

    input_data = read_input('aoc_05.txt')

    part_a = aoc_05(input_data)
    print('part a: {}'.format(part_a))

    part_b = aoc_05(input_data, decrement_large_jumps)
    print('part b: {}'.format(part_b))


if __name__ == '__main__':
    main()
