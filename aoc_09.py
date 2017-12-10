import utils


TEST_INPUT_A = {
    '{}': 1,
    '{{{}}}': 6,
    '{{},{}}': 5,
    '{{{},{},{{}}}}': 16,
    '{<a>,<a>,<a>,<a>}': 1,
    '{{<ab>},{<ab>},{<ab>},{<ab>}}': 9,
    '{{<!!>},{<!!>},{<!!>},{<!!>}}': 9,
    '{{<a!>},{<a!>},{<a!>},{<ab>}}': 3
}
TEST_INPUT_B = {
    '<>': 0,
    '<random characters>': 17,
    '<<<<>': 3,
    '<{!>}>': 2,
    '<!!>': 0,
    '<!!!>>': 0,
    '<{o"i!a,<{i<a>': 10
}


class StreamParser:
    """Parser for data stream.

    Tracks score for groups encountered, nesting level, and characters of
    garbage collected.
    """

    def __init__(self):
        self.score = 0
        self.nesting = 0
        self.garbage = 0

        self._skip = False
        self._in_garbage = False

    def parse_stream(self, stream):
        for char in stream:
            self._process_char(char)

    def _process_char(self, char):
        if self._skip:
            self._skip = False
        elif char == '!':
            self._skip = True
        elif self._in_garbage:
            if char == '>':
                self._in_garbage = False
            else:
                self.garbage += 1
        elif char == '<':
            self._in_garbage = True
        elif char == '{':
            self.nesting += 1
        elif char == '}':
            self.score += self.nesting
            self.nesting -= 1
        else:
            pass


def main():
    test()

    input_data = utils.get_input_data(9)

    parser = StreamParser()
    parser.parse_stream(input_data)
    print(f'part a: {parser.score}')
    print(f'part b: {parser.garbage}')


def test():
    for stream, score in TEST_INPUT_A.items():
        parser = StreamParser()
        parser.parse_stream(stream)
        assert parser.score == score, (stream, parser.score)

    for stream, garbage in TEST_INPUT_B.items():
        parser = StreamParser()
        parser.parse_stream(stream)
        assert parser.garbage == garbage, (stream, parser.garbage)


if __name__ == '__main__':
    main()
