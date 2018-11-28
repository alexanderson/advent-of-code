GEN_A_FACTOR = 16807
GEN_B_FACTOR = 48271

DIVISOR = 2147483647

GEN_A_CRITERIA_MULTIPLE = 4
GEN_B_CRITERIA_MULTIPLE = 8

PART_A_PAIRS = int(4E7)
PART_B_PAIRS = int(5E6)

TEST_START_A = 65
TEST_START_B = 8921

GEN_A_START = 722
GEN_B_START = 354


def generator(multiplier, divisor=DIVISOR):

    def _generator(value):
        while True:
            value = (value * multiplier) % divisor
            yield value

    return _generator


def only_if_multiple(iterator, num):
    for value in iterator:
        if not value % num:
            yield value


generator_a = generator(GEN_A_FACTOR)
generator_b = generator(GEN_B_FACTOR)


def lowest_16_bits(gen_a, gen_b):
    for value_a, value_b in zip(gen_a, gen_b):
        yield (
            lowest_x_bits(value_a, 16),
            lowest_x_bits(value_b, 16)
        )


def lowest_x_bits(value, num_bits):
    return value & 2 ** num_bits - 1


def judges_count(gen_a, gen_b, num_pairs):
    count = 0

    pairs_of_16_bits = lowest_16_bits(gen_a, gen_b)

    for _ in range(num_pairs):
        a, b = next(pairs_of_16_bits)

        if a == b:
            count += 1

    return count


def aoc_15a(start_a, start_b):
    gen_a = generator_a(start_a)
    gen_b = generator_b(start_b)
    return judges_count(gen_a, gen_b, num_pairs=PART_A_PAIRS)


def aoc_15b(start_a, start_b):
    gen_a = generator_a(start_a)
    gen_b = generator_b(start_b)

    gen_a = only_if_multiple(gen_a, GEN_A_CRITERIA_MULTIPLE)
    gen_b = only_if_multiple(gen_b, GEN_B_CRITERIA_MULTIPLE)

    return judges_count(gen_a, gen_b, num_pairs=PART_B_PAIRS)


def main():
    test_misc()
    test_part_a()
    test_part_b()

    count_a = aoc_15a(GEN_A_START, GEN_B_START)
    print(f'part a: {count_a}')

    count_b = aoc_15b(GEN_A_START, GEN_B_START)
    print(f'part b: {count_b}')


def test_misc():
    gen_a = generator_a(TEST_START_A)
    assert [next(gen_a) for _ in range(5)] == [
        1092455,
        1181022009,
        245556042,
        1744312007,
        1352636452
    ]

    gen_b = generator_b(TEST_START_B)
    assert [next(gen_b) for _ in range(5)] == [
        430625591,
        1233683848,
        1431495498,
        137874439,
        285222916
    ]
    lowest_16_bit_pairs = lowest_16_bits(
        generator_a(TEST_START_A),
        generator_b(TEST_START_B)
    )
    first_5_lowest_16_pairs = [next(lowest_16_bit_pairs) for _ in range(5)]
    assert first_5_lowest_16_pairs == [
        (int('1010101101100111', base=2), int('1101001100110111', base=2)),
        (int('1111011100111001', base=2), int('1000010110001000', base=2)),
        (int('1110001101001010', base=2), int('1110001101001010', base=2)),
        (int('0001011011000111', base=2), int('1100110000000111', base=2)),
        (int('1001100000100100', base=2), int('0010100000000100', base=2))
    ], first_5_lowest_16_pairs


def test_part_a():
    count = aoc_15a(TEST_START_A, TEST_START_B)
    assert count == 588, count


def test_part_b():
    count = aoc_15b(TEST_START_A, TEST_START_B)
    assert count == 309, count


if __name__ == '__main__':
    main()
