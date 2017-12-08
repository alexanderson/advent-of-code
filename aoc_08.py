import collections
import operator

import utils


TEST_INPUT = (
    'b inc 5 if a > 1',
    'a inc 1 if b < 5',
    'c dec -10 if a >= 1',
    'c inc -20 if c == 10'
)
ACTIONS =
OPERATORS = {
    '==': operator.eq,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le
}

Instruction = collections.namedtuple('Instruction', (
    'address',
    'operator',
    'value',
    'condition'
))
Condition = collections.namedtuple('Condition', 'address operator value')


def _parse_line(line):
    tokens = line.split(' ')
    addr, op, val, _, cond_addr, cond_op, cond_value = tokens
    return Instruction(
        addr, op, val, Condition(cond_addr, OPERATORS[cond_op], cond_value)
    )

class Memory:

    def __init__(self):
        self._data = {}

    def get(self, key):
        return self._data.setdefault(key, 0)

    def set(self, key, value):
        self._data[key] = value

    def run(self, instruction):
        if instruction.condition.

    def eval_condition(self, condition):
        value = self.get(condition.address)



def run(instructions, memory):
    for instruction in instructions:
        if


def r


def main():
    test()


def test():


if __name__ == '__main__':
    main()
