TEST_INPUT = '''initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #'''
TEST_TOTAL = 325


def parse_input(input_data):
    input_data = input_data.split('\n')
    inital_state = input_data[0].split(': ')[1]
    inital_state = parse_state(inital_state)

    notes = input_data[2:]
    notes = parse_notes(notes)
    return inital_state, notes


def parse_state(state):
    if len(state) == 1:
        return state == '#'
    return [parse_state(pot) for pot in state]


def parse_notes(notes):
    return dict(
        parse_note(note)
        for note in notes
    )


def parse_note(note):
    rule, outcome = note.split(' => ')
    rule = tuple(
        pot == '#'
        for pot in rule
    )
    outcome = outcome == '#'
    return rule, outcome


class Pots:

    def __init__(self, initial_state, notes):
        self.initial_state = initial_state
        self.notes = notes
        self._pots = dict(enumerate(initial_state))

    def __getitem__(self, item):
        return self._pots.get(item, False)

    def evolve(self):
        next_generation = {}

        leftmost = min(k for k in self._pots.keys() if self[k]) - 2
        rightmost = max(k for k in self._pots.keys() if self[k]) + 2

        for i in range(leftmost, rightmost + 1):
            surrouding = tuple(self[x] for x in range(i - 2, i + 3))
            outcome = self.notes.get(surrouding, False)
            next_generation[i] = outcome

        self._pots = next_generation

    def total(self):
        return sum(
            pot_number
            for pot_number, is_alive in self._pots.items()
            if is_alive
        )


def test_evolution():
    initial_state, notes = parse_input(TEST_INPUT)
    pots = Pots(initial_state, notes)
    for _ in range(20):
        pots.evolve()
    total = pots.total()
    assert total == TEST_TOTAL, f'{total} != {TEST_TOTAL}'


def main():
    test_evolution()

    with open('input.txt') as input_file:
        input_data = input_file.read().strip()

    initial_state, notes = parse_input(input_data)
    pots = Pots(initial_state, notes)
    for _ in range(20):
        pots.evolve()
    total = pots.total()
    print(total)

    state = [val for key, val in sorted(pots._pots.items())]
    total = pots.total()
    for cycle in range(20, int(5E10)):
        if not cycle % int(5E3):
            print(cycle)
        pots.evolve()

        new_state = [val for key, val in sorted(pots._pots.items())]
        new_total = pots.total()

        # hack - state converges on a pattern which moved along the pots
        # at a constant rate.
        # Determine the constant total rate and extrapolate.
        if new_state == state:
            rate = new_total - total
            print(new_total + rate * (int(5E10) - cycle -1))
            return

        state = new_state
        total = new_total


if __name__ == '__main__':
    main()
