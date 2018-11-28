import utils


TEST_INPUT = (0, 3, 0, 1, -3)


def increment_jumps(jump):
    return jump + 1


def decrement_large_jumps(jump):
    if jump >= 3:
        return jump - 1
    return jump + 1


def steps_til_exit(data, jump_modifier=increment_jumps):
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


def main():
    test()

    input_data = utils.get_input_data(5)
    input_data = [int(line) for line in input_data.split('\n')]

    part_a = steps_til_exit(input_data)
    print('part a: {}'.format(part_a))

    part_b = steps_til_exit(input_data, decrement_large_jumps)
    print('part b: {}'.format(part_b))


def test():
    assert steps_til_exit(TEST_INPUT) == 5
    assert steps_til_exit(TEST_INPUT, decrement_large_jumps) == 10


if __name__ == '__main__':
    main()
