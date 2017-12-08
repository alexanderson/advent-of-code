import collections
import re

import utils

TEST_INPUT = (
    'pbga (66)',
    'xhth (57)',
    'ebii (61)',
    'havc (66)',
    'ktlj (57)',
    'fwft (72) -> ktlj, cntj, xhth',
    'qoyq (66)',
    'padx (45) -> pbga, havc, qoyq',
    'tknk (41) -> ugml, padx, fwft',
    'jptl (61)',
    'ugml (68) -> gyxo, ebii, jptl',
    'gyxo (61)',
    'cntj (57)'
)

LINE_RE = re.compile('^(\w+) \((\d+)\)(?: -> ([\w\s,]+))?$')


def _parse_line(line):
    name, weight, children = LINE_RE.match(line).groups()
    children = children.split(', ') if children else []
    return name, int(weight), children


class Stack:

    @classmethod
    def parse(cls, input):
        return cls(
            _parse_line(line)
            for line in input
        )

    def __init__(self, programs):
        self.all_programs = set()
        self.weights = {}
        self.children = {}
        self._recursive_weights = {}

        self._load_programs(programs)

        self.parents = self._build_parents()

    def _load_programs(self, programs):
        for name, weight, children in programs:
            self.weights[name] = weight
            self.children[name] = children

    def _build_parents(self):
        parents = {}
        for parent, children in self.children.items():
            # ensure all programs have a key in parents
            parents.setdefault(parent, None)

            for child in children:
                parents[child] = parent
        return parents

    def bottom_program(self):
        return next(
            program
            for program, parent in self.parents.items()
            if parent is None
        )

    def recursive_get_unbalanced_child(self):
        program = self.bottom_program()
        while True:
            unbalanced_child = self.get_unbalanced_child(program)
            if not unbalanced_child:
                return program
            program = unbalanced_child

    def get_unbalanced_child(self, program):
        recursive_child_weights = [
            self.get_recursive_weight(child)
            for child in self.children[program]
        ]
        counts = collections.Counter(recursive_child_weights)
        if len(counts) == 1:
            return None
        odd_child_weight, _ = counts.most_common()[-1]
        odd_child_idx = recursive_child_weights.index(odd_child_weight)
        odd_child = self.children[program][odd_child_idx]
        return odd_child

    def get_recursive_weight(self, program):
        if program not in self._recursive_weights:
            recursive_weight = self._calc_recursive_weight(program)
            self._recursive_weights[program] = recursive_weight
        return self._recursive_weights[program]

    def _calc_recursive_weight(self, program):
        weight = self.weights[program]
        for child in self.children[program]:
            weight += self.get_recursive_weight(child)
        return weight


def aoc_07b(stack):
    erroneous_program = stack.recursive_get_unbalanced_child()
    parent = stack.parents[erroneous_program]
    recursive_child_weights = [
        stack.get_recursive_weight(child)
        for child in stack.children[parent]
    ]
    counts = collections.Counter(recursive_child_weights)
    desired, erroneous = counts.most_common()
    desired_recursive_weight, _ = desired
    erroneous_recursive_weight, _ = erroneous
    weight_correction = desired_recursive_weight - erroneous_recursive_weight
    return stack.weights[erroneous_program] + weight_correction


def main():
    test()
    
    input_data = utils.get_input_data(7).split('\n')

    stack = Stack.parse(input_data)
    
    part_a = stack.bottom_program()
    print(f'part a: {part_a}')

    part_b = aoc_07b(stack)
    print(f'part b: {part_b}')


def test():
    stack = Stack.parse(TEST_INPUT)
    part_a_test = stack.bottom_program()
    assert part_a_test == 'tknk', part_a_test

    assert stack.get_recursive_weight('ugml') == 251
    assert stack.get_recursive_weight('padx') == 243
    assert stack.get_recursive_weight('fwft') == 243

    corrected_weight = aoc_07b(stack)
    assert corrected_weight == 60


if __name__ == '__main__':
    main()
