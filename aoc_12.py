import utils

TEST_INPUT = (
    '0 <-> 2',
    '1 <-> 1',
    '2 <-> 0, 3, 4',
    '3 <-> 2, 4',
    '4 <-> 2, 3, 6',
    '5 <-> 6',
    '6 <-> 4, 5'
)


def connected_programs(input_data, program):
    all_connections = parse_input(input_data)
    connections = collect_group(all_connections, program)
    return len(connections)


def connected_groups(input_data):
    all_connections = parse_input(input_data)
    groups = 0

    while all_connections:
        seed_program = next(iter(all_connections.keys()))
        collect_group(all_connections, seed_program)
        groups += 1

    return groups


def collect_group(all_connections, seed_program):
    connections = {seed_program}
    while True:
        new_connections = set()

        for p in connections:
            new_connections |= get_connections(all_connections, p)

        if new_connections:
            connections |= new_connections
        else:
            break
    return connections


def get_connections(data, program):
    return set(data.pop(program, []))


def parse_input(data):
    all_connections = {}
    for line in data:
        program, connections = line.split(' <-> ')
        connections = [
            int(connection)
            for connection in connections.split(', ')
        ]
        all_connections[int(program)] = connections
    return all_connections


def main():
    test()

    input_data = utils.get_input_data(12).split('\n')

    connections = connected_programs(input_data, 0)
    print(f'part a: {connections}')
    num_groups = connected_groups(input_data)
    print(f'part b: {num_groups}')


def test():
    connections = connected_programs(TEST_INPUT, 0)
    assert connections == 6, connections
    groups = connected_groups(TEST_INPUT)
    assert groups == 2, groups


if __name__ == '__main__':
    main()
