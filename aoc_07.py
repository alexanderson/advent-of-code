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

Program = collections.namedtuple('Program', 'name weight children')


def bottom_program(data):
    programs_by_name = _parse_input(data)
    all_programs = set(programs_by_name.values())
    programs_with_parent = {
        programs_by_name[child]
        for parent in all_programs
        for child in parent.children
    }
    parentless_programs = all_programs - programs_with_parent
    assert len(parentless_programs) == 1, parentless_programs
    return parentless_programs.pop()


def _parse_input(data):
    programs = (_parse_line(line) for line in data)
    return {
        program.name: program
        for program in programs
    }


def _parse_line(line):
    name, weight, children = LINE_RE.match(line).groups()
    children = tuple(children.split(', ')) if children else ()
    return Program(name, weight, children)


def main():
    test()
    
    input_data = utils.get_input_data(7).split('\n')
    
    part_a = bottom_program(input_data).name
    print(f'part a: {part_a}')


def test():
    part_a_test = bottom_program(TEST_INPUT).name
    assert part_a_test == 'tknk', part_a_test


if __name__ == '__main__':
    main()
