import utils


TEST_PROGRAMS = 'abcde'
PROGRAMS = 'abcdefghijklmnop'

TEST_INSTRUCTIONS = ('s1', 'x3/4', 'pe/b')


class Dance:

    def __init__(self, instructions, programs=PROGRAMS):
        self.programs = list(programs)

        self._action_map = {
            's': self.spin,
            'x': self.exchange,
            'p': self.partner
        }
        self.instructions = [
            self._compile(instruction)
            for instruction in instructions
        ]

    def _compile(self, instruction):
        action = self._action_map[instruction[0]]
        args = instruction[1:].split('/')
        if action != self.partner:
            args = tuple(int(arg) for arg in args)
        return action, args

    def perform(self):
        for action, args in self.instructions:
            action(*args)

    def spin(self, x):
        self.programs = self.programs[-x:] + self.programs[:-x]

    def exchange(self, a, b):
        self.programs[a], self.programs[b] = self.programs[b], self.programs[a]

    def partner(self, a, b):
        index_a = self.programs.index(a)
        index_b = self.programs.index(b)
        self.exchange(index_a, index_b)

    def __str__(self):
        return ''.join(self.programs)


def period(dance):
    """Number of dance iterations until programs return to starting positions.
    """
    seen_positions = {str(dance)}
    cycles = 0

    while True:
        dance.perform()
        cycles += 1
        positions = str(dance)

        if positions in seen_positions:
            break

        seen_positions.add(positions)

    return cycles


def main():
    test()

    instructions = utils.get_input_data(16).split(',')
    dance = Dance(instructions)

    dance.perform()
    print(f'part a: {dance}')

    dance = Dance(instructions)

    dance_period = period(dance)

    for _ in range(int(1E9) % dance_period):
        dance.perform()

    print(f'part b: {dance}')


def test():
    dance = Dance(TEST_INSTRUCTIONS, TEST_PROGRAMS)
    dance.perform()
    assert ''.join(dance.programs) == 'baedc'
    dance.perform()
    assert ''.join(dance.programs) == 'ceadb'


if __name__ == '__main__':
    main()
