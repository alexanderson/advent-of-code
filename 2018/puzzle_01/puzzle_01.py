TEST_CHANGES = {
    ('+1', '+1', '+1'): 3,
    ('+1', '+1', '-2'): 0,
    ('-1', '-2', '-3'): -6,
}
TEST_CHANGES_2 = {
    ('+1', '-1'): 0,
    ('+3', '+3', '+4', '-2', '-4'): 10,
    ('-6', '+3', '+8', '+5', '-6'): 5,
    ('+7', '+7', '-2', '-7', '-4'): 14,
}


def calibrate(deltas):
    frequency = 0
    for delta in deltas:
        frequency += int(delta)
    return frequency


def calibrate_2(deltas):
    current_frequency = 0
    frequency_history = {0}
    while True:
        for delta in deltas:
            current_frequency += int(delta)
            if current_frequency in frequency_history:
                return current_frequency
            frequency_history.add(current_frequency)


def test_calibrate(test_data, calibration_fn):
    for deltas, expected_frequency in test_data.items():
        frequency = calibration_fn(deltas)
        assert frequency == expected_frequency, '{} != {}'.format(
            frequency, expected_frequency
        )


def get_input():
    with open('input.txt') as input_file:
        data = input_file.read()
    lines = data.split('\n')
    return list(filter(None, lines))


if __name__ == '__main__':
    deltas = get_input()
    test_calibrate(TEST_CHANGES, calibrate)
    frequency = calibrate(deltas)
    print(frequency)

    test_calibrate(TEST_CHANGES_2, calibrate_2)
    frequency = calibrate_2(deltas)
    print(frequency)
