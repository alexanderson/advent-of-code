TEST_INPUT_A = '3,4,1,5'
TEST_INPUT_B = {
    '': 'a2582a3a0e66e6e86e3812dcb672a272',
    'AoC 2017': '33efeb34ea91902bb2f59c9920caa6cd',
    '1,2,3': '3efbe78a8d82f29979031a4aa0b16a9d',
    '1,2,4': '63960835bcdc130f0b66d7ff4f6a5a8e'
}

INPUT = '83,0,193,1,254,237,187,40,88,27,2,255,149,29,42,100'

SUFFIX = [17, 31, 73, 47, 23]


class Loop:

    def __init__(self, size=256):
        self._size = size
        self._data = list(range(size))
        self._pointer = 0
        self._skip_size = 0

    def move(self, n):
        self._pointer = (self._pointer + n) % self._size

    def get(self, size):
        start = self._pointer
        end = start + size
        if end > self._size:
            data_a = self._data[start:]
            data_b = self._data[:end - self._size]
            return data_a + data_b
        else:
            return self._data[start:end]

    def apply(self, chunk):
        chunk_size = len(chunk)
        if self._pointer + chunk_size > self._size:
            size_a = self._size - self._pointer
            size_b = chunk_size - size_a
            self._data[self._pointer:] = chunk[:size_a]
            self._data[:size_b] = chunk[size_a:]
        else:
            self._data[self._pointer:self._pointer + chunk_size] = chunk

    def twist(self, twist_size):
        chunk = self.get(twist_size)
        chunk.reverse()
        self.apply(chunk)
        self.move(twist_size + self._skip_size)
        self._skip_size += 1

    def knot_hash(self, input_data):
        twists = [int(t) for t in input_data.split(',')]
        for twist_size in twists:
            self.twist(twist_size)
        return self._data[0] * self._data[1]

    def sparse_hash(self, input_data):
        twists = lengths(input_data)
        for _ in range(64):
            for twist_size in twists:
                self.twist(twist_size)
        return self._data

    def dense_hash(self, input_data):
        sparse_hash = self.sparse_hash(input_data)
        blocks = [sparse_hash[i:i + 16] for i in range(0, 256, 16)]
        assert len(blocks) == 16
        assert all(len(block) == 16 for block in blocks)
        elements = [_xor_all(block) for block in blocks]
        return ''.join(_hex(element) for element in elements)

    def __str__(self):
        data = self._data[:]
        data[self._pointer] = str(data[self._pointer]).join('[]')
        return str(data)


def lengths(input_data):
    input_data = [ord(c) for c in input_data]
    input_data += SUFFIX
    return input_data


def _xor_all(items):
    value = 0
    for item in items:
        value ^= item
    return value


def _hex(value):
    value = hex(value)[2:]
    if len(value) == 1:
        value = '0' + value
    return value


def main():
    test()

    knot_hash = Loop().knot_hash(INPUT)
    print(f'part a: {knot_hash}')

    dense_hash = Loop().dense_hash(INPUT)
    print(f'part b: {dense_hash}')


def test():
    loop = Loop(5)
    assert loop.knot_hash(TEST_INPUT_A) == 12

    assert lengths('1,2,3') == [49, 44, 50, 44, 51, 17, 31, 73, 47, 23]

    for input_data, hash_ in TEST_INPUT_B.items():
        dense_hash = Loop().dense_hash(input_data)
        assert dense_hash == hash_, dense_hash


if __name__ == '__main__':
    main()
