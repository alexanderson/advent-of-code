TEST_POLYMER = 'dabAcCaCBAcCcaDA'
TEST_RESULT = 'dabCBAcaDA'
TEST_SHORTEST_LENGTH = 4


def react(polymer):
    while True:
        pair_index = find_pair(polymer)
        if pair_index is None:
            return polymer
        polymer = polymer[:pair_index] + polymer[pair_index + 2:]


def find_pair(polymer):
    for i in range(len(polymer) - 1):
        if polymer[i].swapcase() == polymer[i + 1]:
            return i


def get_shortest_polymer(polymer):
    shortest_length = len(polymer)
    for unit in 'abcdefghijklmnopqrstuvwxyz':
        reduced_polymer = remove_unit(unit, polymer)
        reacted_polymer = react(reduced_polymer)
        length = len(reacted_polymer)
        if length < shortest_length:
            shortest_length = length
    return shortest_length


def remove_unit(unit, polymer):
    return polymer.replace(unit, '').replace(unit.upper(), '')


def test_reaction():
    result = react(TEST_POLYMER)
    assert result == TEST_RESULT, result


def test_shortest_polymer():
    length = get_shortest_polymer(TEST_POLYMER)
    assert length == TEST_SHORTEST_LENGTH, length


def get_input():
    with open('input.txt') as input_file:
        return input_file.read().strip()


if __name__ == '__main__':
    test_reaction()
    test_shortest_polymer()

    polymer = get_input()
    result = react(polymer)
    print(len(result))

    length = get_shortest_polymer(polymer)
    print(length)
