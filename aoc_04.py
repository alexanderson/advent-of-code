import itertools


TEST_INPUT_A = {
    'aa bb cc dd ee': True,
    'aa bb cc dd aa': False,
    'aa bb cc dd aaa': True
}
TEST_INPUT_B = {
    'abcde fghij': True,
    'abcde xyz ecdab': False,
    'a ab abc abd abf abj': True,
    'iiii oiii ooii oooi oooo': True,
    'oiii ioii iioi iiio': False
}


def passphrase_valid(passphrase, check_fns):
    assert passphrase
    parts = passphrase.split(' ')
    for word_a, word_b in itertools.combinations(parts, 2):
        for func in check_fns:
            if not func(word_a, word_b):
                return False
    return True


def words_unique(word_a, word_b):
    return word_a != word_b


def words_not_anagrams(word_a, word_b):
    if sorted(word_a) != sorted(word_b):
        return True


def aoc_04(data, check_fns):
    return sum(
        passphrase_valid(phrase, check_fns)
        for phrase in data
    )


def read_input(path):
    with open(path) as f:
        return [
            line.strip()
            for line in f.readlines()
            if line
        ]


def main():
    part_a_fns = [words_unique]
    part_b_fns = [words_unique, words_not_anagrams]

    for phrase, valid in TEST_INPUT_A.items():
        assert passphrase_valid(phrase, part_a_fns) == valid

    for phrase, valid in TEST_INPUT_B.items():
        assert passphrase_valid(phrase, part_b_fns) == valid

    input_data = read_input('aoc_04.txt')

    part_a = aoc_04(input_data, part_a_fns)
    print('part a: {}'.format(part_a))

    part_b = aoc_04(input_data, part_b_fns)
    print('part b: {}'.format(part_b))


if __name__ == '__main__':
    main()
