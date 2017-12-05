import itertools

import utils


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
    """Check a passphrase is valid.

    :param passphrase: phrase to check validity.
    :param check_fns: list of functions which determine validity.
    """
    assert passphrase
    parts = passphrase.split(' ')
    for word_a, word_b in itertools.combinations(parts, 2):
        for func in check_fns:
            if not func(word_a, word_b):
                return False
    return True


def words_unique(word_a, word_b):
    """Two words are unique."""
    return word_a != word_b


def words_not_anagrams(word_a, word_b):
    """Two words are not anagrams."""
    if sorted(word_a) != sorted(word_b):
        return True


def num_valid_passphrases(data, check_fns):
    return sum(
        passphrase_valid(phrase, check_fns)
        for phrase in data
    )


def main():
    test()

    input_data = utils.get_input_data(4).split('\n')

    part_a = num_valid_passphrases(
        input_data, [words_unique]
    )
    print('part a: {}'.format(part_a))

    part_b = num_valid_passphrases(
        input_data, [words_unique, words_not_anagrams]
    )
    print('part b: {}'.format(part_b))


def test():
    for phrase, valid in TEST_INPUT_A.items():
        assert passphrase_valid(phrase, [words_unique]) == valid

    for phrase, valid in TEST_INPUT_B.items():
        assert passphrase_valid(
            phrase, [words_unique, words_not_anagrams]
        ) == valid


if __name__ == '__main__':
    main()
