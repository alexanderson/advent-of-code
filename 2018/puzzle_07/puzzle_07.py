TEST_INPUT = (
    'Step C must be finished before step A can begin.',
    'Step C must be finished before step F can begin.',
    'Step A must be finished before step B can begin.',
    'Step A must be finished before step D can begin.',
    'Step B must be finished before step E can begin.',
    'Step D must be finished before step E can begin.',
    'Step F must be finished before step E can begin.',
)
TEST_ORDER = 'CABDFE'
TEST_COMPLETION_TIME = 15


class Node:

    def __init__(self, step):
        self.step = step
        self.dependencies = set()
        self.following = set()

    def time_to_complete(self, time_offset):
        return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(self.step) + time_offset + 1

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return 'Node({step})'.format(step=self.step)


class Graph:

    def __init__(self, dependencies):
        self.dependencies = dependencies
        self.nodes = {}
        for step, depends_on in dependencies:
            if step not in self.nodes:
                self.nodes[step] = Node(step)
            if depends_on not in self.nodes:
                self.nodes[depends_on] = Node(depends_on)

            self.nodes[step].dependencies.add(self.nodes[depends_on])
            self.nodes[depends_on].following.add(self.nodes[step])

        self.root_nodes = frozenset(
            node for node in self.nodes.values()
            if not node.dependencies
        )
        self.completed_nodes = set()
        self.queue = set(self.root_nodes)

    def traverse(self):
        while self.queue:
            current_node = self.get_next_node()
            yield current_node
            self.finish_node(current_node)

    def get_next_node(self):
        if not self.queue:
            return None
        node = min(self.queue, key=lambda node: node.step)
        self.queue.remove(node)
        return node

    def finish_node(self, node):
        self.completed_nodes.add(node)
        self.add_next_steps_to_queue(node)

    def add_next_steps_to_queue(self, node):
        next_nodes = {
            n for n in
            # all uncompleted nodes
            node.following - self.completed_nodes
            # only if all deps have been completed
            if n.dependencies <= self.completed_nodes
        }
        self.queue |= next_nodes

    def is_complete(self):
        return self.completed_nodes == set(self.nodes.values())


class InstructionProcessor:
    
    def __init__(self, graph, num_workers, time_offset):
        self.graph = graph
        self.workers = [Worker(time_offset) for _ in range(num_workers)]
        
    def process(self):
        t = 0
        while True:
            self.tick()
            if self.graph.is_complete():
                return t
            t += 1
    
    def tick(self):
        for worker in self.workers:
            if worker.is_finished():
                self.graph.finish_node(worker.job)
                worker.reset()
            if not worker.job:
                node = self.graph.get_next_node()
                if node:
                    worker.give(node)
        for worker in self.workers:
            if worker.job:
                assert worker.remaining_time
                worker.remaining_time -= 1


class Worker:

    def __init__(self, time_offset):
        self.job = None
        self.remaining_time = None
        self.time_offset = time_offset

    def give(self, node):
        self.job = node
        self.remaining_time = node.time_to_complete(self.time_offset)

    def is_finished(self):
        return self.job and self.remaining_time == 0

    def reset(self):
        self.job = None
        self.remaining_time = None


def get_order(dependencies):
    graph = Graph(dependencies)
    return ''.join(node.step for node in graph.traverse())


def get_time_to_complete(dependencies, num_workers, time_offset):
    graph = Graph(dependencies)
    processor = InstructionProcessor(graph, num_workers, time_offset)
    total_time = processor.process()
    return total_time


def parse_dependencies(input_data):
    return [parse_line(line) for line in input_data]


def parse_line(line):
    parts = line.split(' ')
    return parts[7], parts[1]


def get_input():
    with open('input.txt') as input_file:
        return input_file.readlines()


def test_order():
    dependencies = parse_dependencies(TEST_INPUT)
    order = get_order(dependencies)
    assert order == TEST_ORDER, order


def test_time_to_complete():
    dependencies = parse_dependencies(TEST_INPUT)
    total_time = get_time_to_complete(
        dependencies, num_workers=2, time_offset=0
    )
    assert total_time == TEST_COMPLETION_TIME, total_time


def main():
    test_order()
    test_time_to_complete()

    input_data = get_input()
    dependencies = parse_dependencies(input_data)
    order = get_order(dependencies)
    print(order)

    total_time = get_time_to_complete(
        dependencies, num_workers=5, time_offset=60
    )
    print(total_time)


if __name__ == '__main__':
    main()
