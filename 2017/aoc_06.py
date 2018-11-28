TEST_INPUT_A = (0, 2, 7, 0)

INPUT_DATA = (11, 11, 13, 7, 0, 15, 5, 5, 4, 4, 1, 1, 7, 1, 15, 11)


def required_redistribution_cycles(redistribution_history):
    return len(redistribution_history) - 1


def redistribution_loop_size(redistribution_history):
    loop_end_value = redistribution_history[-1]
    loop_start_cycle = redistribution_history.index(loop_end_value)
    total_cycles = required_redistribution_cycles(redistribution_history)
    return total_cycles - loop_start_cycle


def redistribute_until_loop(data):
    history = list()
    data = list(data)

    while tuple(data) not in history:
        history.append(tuple(data))

        largest_bucket = data.index(max(data))
        data = redistribute(data, largest_bucket)

    history.append(tuple(data))

    return history


def redistribute(data, idx):
    size = len(data)
    blocks = _empty_bucket(data, idx)

    for block in range(blocks):
        idx = _next_idx(idx, size)
        data[idx] += 1

    return data


def _empty_bucket(data, idx):
    blocks = data[idx]
    data[idx] = 0
    return blocks


def _next_idx(idx, size):
    idx += 1
    return 0 if idx == size else idx


def main():
    test()

    redistribution_history = redistribute_until_loop(INPUT_DATA)

    part_a = required_redistribution_cycles(redistribution_history)
    print('part a: {}'.format(part_a))

    part_b = redistribution_loop_size(redistribution_history)
    print('part b: {}'.format(part_b))


def test():
    test_history = redistribute_until_loop(TEST_INPUT_A)
    cycles = required_redistribution_cycles(test_history)
    loop_size = redistribution_loop_size(test_history)
    assert cycles == 5, cycles
    assert loop_size == 4, loop_size


if __name__ == '__main__':
    main()
