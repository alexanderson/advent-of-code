import collections


TEST_IDS = (
    'abcdef',
    'bababc',
    'abbcde',
    'abcccd',
    'aabcdd',
    'abcdee',
    'ababab',
), 12
TEST_IDS_2 = (
    'abcde',
    'fghij',
    'klmno',
    'pqrst',
    'fguij',
    'axcye',
    'wvxyz',
), 'fgij'


def calc_checksum(ids):
    contains_two = 0
    contains_three = 0
    for id in ids:
        counter = collections.Counter(id)
        counts = {count for _, count in counter.most_common()}
        if 3 in counts:
            contains_three += 1
        if 2 in counts:
            contains_two += 1
    return contains_two * contains_three


def correct_common_letters(ids):
    for pair in pairs(ids):
        letters = list(zip(*pair))
        if letter_difference(letters) == 1:
            return common_letters(letters)


def pairs(items):
    for i, item in enumerate(items):
        others = items[:i] + items[i + 1:]
        for other in others:
            yield item, other


def letter_difference(letters):
    return sum(1 for x, y in letters if x != y)


def common_letters(letters):
    return ''.join(x for x, y in letters if x == y)


def test_checksum(input_data):
    ids, expected_checksum = input_data
    checksum = calc_checksum(ids)
    assert checksum == expected_checksum, '{} != {}'.format(
        checksum, expected_checksum
    )


def test_common_letters(input_data):
    ids, expected_common = input_data
    common = correct_common_letters(ids)
    assert common == expected_common, '{} != {}'.format(
        common, expected_common
    )


def get_input():
    with open('input.txt') as input_file:
        data = input_file.read()
    lines = data.split('\n')
    return list(filter(None, lines))


if __name__ == '__main__':
    test_checksum(TEST_IDS)

    ids = get_input()
    checksum = calc_checksum(ids)
    print(checksum)

    test_common_letters(TEST_IDS_2)
    common = correct_common_letters(ids)
    print(common)
