TEST_LICENCE = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
TEST_META_SUM = 138
TEST_VALUE = 66


class Node:
    def __init__(self):
        self.children = []
        self.meta = []


def parse_node(licence):
    if isinstance(licence, str):
        licence = iter(int(part) for part in licence.split(' '))

    node = Node()
    num_children = next(licence)
    num_meta = next(licence)
    for _ in range(num_children):
        node.children.append(parse_node(licence))
    for _ in range(num_meta):
        node.meta.append(next(licence))
    return node


def sum_meta(node):
    return sum(node.meta + [sum_meta(child) for child in node.children])


def get_value(node):
    if node.children:
        value = 0
        for child_index in node.meta:
            try:
                child = node.children[child_index - 1]
            except IndexError:
                pass
            else:
                value += get_value(child)

        return value
    else:
        return sum(node.meta)


def test_sum_meta():
    root = parse_node(TEST_LICENCE)
    meta_sum = sum_meta(root)
    assert meta_sum == TEST_META_SUM, meta_sum


def test_get_value():
    root = parse_node(TEST_LICENCE)
    value = get_value(root)
    assert value == TEST_VALUE, value


def get_input():
    with open('input.txt') as input_file:
        return input_file.read().strip()


def main():
    test_sum_meta()
    test_get_value()

    licence = get_input()
    root = parse_node(licence)
    meta_sum = sum_meta(root)
    print(meta_sum)

    value = get_value(root)
    print(value)


if __name__ == '__main__':
    main()
