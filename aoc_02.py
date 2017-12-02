TEST_INPUT_A = (
    (5, 1, 9, 5),
    (7, 5, 3),
    (2, 4, 6, 8)
)
TEST_INPUT_B = (
    (5, 9, 2, 8),
    (9, 4, 7, 3),
    (3, 8, 6, 5)
)


def checksum_a(data):
    return sum(
        max(row) - min(row)
        for row in data
    )


def checksum_b(data):
    return sum(
        _divide(*_get_two_divisible(row))
        for row in data
    )


def _get_two_divisible(row):
    for a in row:
        for b in row:
            if a == b:
                continue
            if not a % b:
                return a, b


def _divide(a, b):
    return a / b


def read_input(path):
    with open(path) as f:
        return [
            _parse_row(row)
            for row in f.readlines()
            if row
        ]


def _parse_row(row):
    return [
        int(item)
        for item in row.split('\t')
    ]


def main():
    assert checksum_a(TEST_INPUT_A) == 18
    assert checksum_b(TEST_INPUT_B) == 9

    input_data = read_input('aoc_02.tsv')

    part_a = checksum_a(input_data)
    print('part a: {}'.format(part_a))

    part_b = checksum_b(input_data)
    print('part b: {}'.format(part_b))


if __name__ == '__main__':
    main()
