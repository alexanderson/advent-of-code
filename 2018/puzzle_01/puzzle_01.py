TEST_CHANGES = {
    ('+1', '+1', '+1'): 3,
    ('+1', '+1', '-2'): 0,
    ('-1', '-2', '-3'): -6,
}


def calibrate(deltas):
    frequency = 0
    for delta in deltas:
        frequency += int(delta)
    return frequency


def test_calibrate():
    for deltas, expected_frequency in TEST_CHANGES.items():
        frequency = calibrate(deltas)
        assert frequency == expected_frequency


def get_input():
    with open('input.txt') as input_file:
        data = input_file.read()
    lines = data.split('\n')
    return filter(None, lines)


if __name__ == '__main__':
    test_calibrate()
    frequency = calibrate(get_input())
    print(frequency)
