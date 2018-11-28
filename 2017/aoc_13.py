import utils

TEST_INPUT = (
    '0: 3',
    '1: 2',
    '4: 4',
    '6: 4'
)


class Firewall:

    def __init__(self, config):
        config = dict(config)

        self.num_layers = max(config.keys()) + 1
        self._layers = [
            Layer(config.get(layer, 0))
            for layer in range(self.num_layers)
        ]
        self.packet_position = -1

        self.score = 0

    def wait_for(self, picoseconds):
        for _ in range(picoseconds):
            self.scan_move()

    def packed_in_motion(self):
        return self.packet_position < self.num_layers

    def tick(self):
        assert self.packed_in_motion()
        self.packet_position += 1
        self.amend_score()
        self.scan_move()

    def amend_score(self):
        if self.packed_in_motion():
            layer = self._layers[self.packet_position]
            if layer.scan_active():
                self.score += (self.packet_position * layer.size)

    def scan_move(self):
        for layer in self._layers:
            layer.scan_move()


class Layer:

    def __init__(self, size):
        self.size = size
        self._scan_direction = 1
        self.scan_position = 0

    def scan_move(self):
        if self.size < 2:
            return

        self.scan_position += self._scan_direction

        if self.scan_position in (0, self.size - 1):
            self._scan_direction *= -1

    def scan_active(self):
        return self.size and self.scan_position == 0

    def __str__(self):
        return ' '.join(
            '*' if self.scan_position == i else '_'
            for i in range(self.size)
        )


def score(input_data):
    firewall = parse_input(input_data)
    while firewall.packed_in_motion():
        firewall.tick()

    return firewall.score


def undetected(firewall):
    while firewall.packed_in_motion():
        firewall.tick()
        if firewall.score:
            return False
    return True


def required_wait(input_data):
    wait = 0
    while True:
        firewall = parse_input(input_data)
        firewall.wait_for(wait)

        if undetected(firewall):
            break
        wait += 1

    return wait


def parse_input(input_data):
    return Firewall(
        _parse_line(line)
        for line in input_data
    )


def _parse_line(line):
    layer, width = line.split(': ')
    return int(layer), int(width)


def main():
    test()

    input_data = utils.get_input_data(13).split('\n')
    firewall_score = score(input_data)
    print(f'part a: {firewall_score}')

    wait = required_wait(input_data)
    print(f'part b: {wait}')


def test():

    test_score = score(TEST_INPUT)
    assert test_score == 24, test_score

    wait = required_wait(TEST_INPUT)
    assert wait == 10, wait


if __name__ == '__main__':
    main()
