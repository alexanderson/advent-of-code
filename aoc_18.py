import operator as op

import utils

TEST_INSTRUCTIONS = (
    'set a 1',
    'add a 2',
    'mul a a',
    'mod a 5',
    'snd a',
    'set a 0',
    'rcv a',
    'jgz a -1',
    'set a 1',
    'jgz a -2'
)


class RecoveredSound(Exception):

    def __init__(self, frequency):
        self.frequency = frequency


class JumpError(Exception):
    pass


class Program:

    def __init__(self, instructions):
        self._data = {}
        self._action_map = {
            'set': self.set,
            'add': self.add,
            'mul': self.mul,
            'mod': self.mod,
            'snd': self.snd,
            'rcv': self.rcv,
            'jgz': self.jgz
        }
        self._instructions = [
            self._parse_instruction(instruction)
            for instruction in instructions
        ]
        self.position = 0
        self._last_sound_played = None

    def _parse_instruction(self, instruction):
        action, *args = instruction.split(' ')

        if action in ('snd', 'rcv'):
            return self._action_map[action], args[0]

        register, value = args
        try:
            value = int(value)
        except ValueError:
            pass

        return self._action_map[action], register, value

    def run(self):
        while True:
            action, *args = self._instructions[self.position]

            try:
                jumped = action(*args)
            except RecoveredSound as sound:
                return sound.frequency

            if not jumped:
                self.position += 1

    def get(self, register):
        return self._data.get(register, 0)

    def set(self, register, value):
        value = self._process_value(value)
        self._data[register] = value

    def add(self, register, value):
        value = self._process_value(value)
        self._act(register, op.add, value)

    def mul(self, register, value):
        value = self._process_value(value)
        self._act(register, op.mul, value)

    def mod(self, register, value):
        value = self._process_value(value)
        self._act(register, op.mod, value)

    def snd(self, register):
        self._last_sound_played = self.get(register)

    def rcv(self, register):
        if self.get(register):
            raise RecoveredSound(self._last_sound_played)

    def jgz(self, register, value):
        if self.get(register):
            value = self._process_value(value)
            self.position += value
            return True

    def _process_value(self, value):
        return value if isinstance(value, int) else self.get(value)

    def _act(self, register, operator, value):
        curr_value = self.get(register)
        self._data[register] = operator(curr_value, value)


def main():
    test()

    instructions = utils.get_input_data(18).split('\n')
    program = Program(instructions)
    freq = program.run()
    print(f'part a: {freq}')


def test():
    program = Program(TEST_INSTRUCTIONS)
    freq = program.run()
    assert freq == 4


if __name__ == '__main__':
    main()
