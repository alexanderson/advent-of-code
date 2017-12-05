import utils


TEST_INPUTS_A = {
    '1122': 3,
    '1111': 4,
    '1234': 0,
    '91212129': 9
}
TEST_INPUTS_B = {
    '1212': 6,
    '1221': 0,
    '123425': 4,
    '123123': 12,
    '12131415': 4
}


def calc_sum(data, next_idx_fn):
    sum = 0

    for idx, val in enumerate(data):
        val = int(val)

        next_idx = next_idx_fn(idx, len(data))
        next_val = int(data[next_idx])

        if val == next_val:
            sum += val

    return sum


def next_idx_a(idx, data_len):
    next_idx = idx + 1
    if next_idx == data_len:
        return 0
    return next_idx


def next_idx_b(idx, data_len):
    next_idx = idx + data_len/2
    if next_idx >= data_len:
        return next_idx - data_len
    return next_idx


def aoc_01(next_idx_fn, test_inputs, input_data):
    for data, value in test_inputs.items():
        assert calc_sum(data, next_idx_fn) == value

    return calc_sum(input_data, next_idx_fn)


if __name__ == '__main__':
    input_data = utils.get_input_data(1)

    part_a_answer = aoc_01(next_idx_a, TEST_INPUTS_A, input_data)
    print('part a: {}'.format(part_a_answer))

    part_b_answer = aoc_01(next_idx_b, TEST_INPUTS_B, input_data)
    print('part b: {}'.format(part_b_answer))
