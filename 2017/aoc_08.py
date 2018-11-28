import operator

import utils


TEST_INPUT = (
    'b inc 5 if a > 1',
    'a inc 1 if b < 5',
    'c dec -10 if a >= 1',
    'c inc -20 if c == 10'
)


ACTION_OPERATORS = {
    'inc': operator.add,
    'dec': operator.sub
}

CONDITION_OPERATORS = {
    '==': operator.eq,
    '!=': operator.ne,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}


class Instruction:
    """An instruction to perform on a memory object.

    Evaluates its condition on the memory then performs the action if the
    condition holds.

    Able to parse instruction strings using `Instruction.parse().`
    """

    def __init__(self, action, condition):
        self.action = action
        self.condition = condition

    @classmethod
    def parse(cls, line):
        action, condition = line.split(' if ')
        action = action.split(' ')
        condition = condition.split(' ')
        return cls(Action(*action), Condition(*condition))

    def evaluate(self, memory):
        if self.condition.evaluate(memory):
            self.action.evaluate(memory)


class Action:
    """An instruction action.

    Performs an inc/dec on a memory address by a certain value.
    """

    def __init__(self, address, operator_, value):
        self.address = address
        self.operator = ACTION_OPERATORS[operator_]
        self.value = int(value)

    def evaluate(self, memory):
        memory.set(
            self.address,
            self.operator(memory.get(self.address), self.value)
        )


class Condition:
    """An instruction condition.

    Evaluates its value using its operator with a value at a memory address.
    """

    def __init__(self, address, operator_, value):
        self.address = address
        self.operator = CONDITION_OPERATORS[operator_]
        self.value = int(value)

    def evaluate(self, memory):
        return self.operator(memory.get(self.address), self.value)


class Memory:
    """Memory register data structure.

    Has getter and setter methods, unassigned registers default to 0.
    Has current max and global historic max properties."""

    def __init__(self):
        self._data = {}
        self.global_max = 0

    def get(self, key):
        return self._data.setdefault(key, 0)

    def set(self, key, value):
        if value > self.global_max:
            self.global_max = value

        self._data[key] = value

    @property
    def max(self):
        return max(self._data.values())


def run(input_data):
    """Run an instruction set on a freshly initialized memory object.
    Returns the resulting memory state."""
    memory = Memory()

    for line in input_data:
        instruction = Instruction.parse(line)
        instruction.evaluate(memory)

    return memory


def main():
    test()

    input_data = utils.get_input_data(8).split('\n')
    memory = run(input_data)
    print(f'part a: {memory.max}')
    print(f'part b: {memory.global_max}')


def test():
    memory = run(TEST_INPUT)
    assert memory.max == 1
    assert memory.global_max == 10


if __name__ == '__main__':
    main()
