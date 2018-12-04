import collections
import datetime
import re


TEST_LOG = (
    '[1518-11-01 00:00] Guard #10 begins shift',
    '[1518-11-01 00:05] falls asleep',
    '[1518-11-01 00:25] wakes up',
    '[1518-11-01 00:30] falls asleep',
    '[1518-11-01 00:55] wakes up',
    '[1518-11-01 23:58] Guard #99 begins shift',
    '[1518-11-02 00:40] falls asleep',
    '[1518-11-02 00:50] wakes up',
    '[1518-11-03 00:05] Guard #10 begins shift',
    '[1518-11-03 00:24] falls asleep',
    '[1518-11-03 00:29] wakes up',
    '[1518-11-04 00:02] Guard #99 begins shift',
    '[1518-11-04 00:36] falls asleep',
    '[1518-11-04 00:46] wakes up',
    '[1518-11-05 00:03] Guard #99 begins shift',
    '[1518-11-05 00:45] falls asleep',
    '[1518-11-05 00:55] wakes up',
)


LOG_RE = re.compile(
    r'\[1518-(?P<date>[\d\-]+) '
    r'(?P<hour>\d\d):(?P<minute>\d\d)\] '
    r'(?P<message>.*)'
)


BEGINS_SHIFT = 'begins shift'
FALLS_ASLEEP = 'falls asleep'
WAKES_UP = 'wakes up'


Event = collections.namedtuple('Event', 'date time action guard_id')
Sleep = collections.namedtuple('Sleep', 'guard_id date start end')


def parse_log(raw_log):
    return sorted(
        (parse_log_line(line) for line in raw_log),
        key=lambda event: (event.date, event.time)
    )


def parse_log_line(line):
    match = LOG_RE.match(line)
    groups = match.groupdict()
    date = groups['date']
    time = datetime.time(int(groups['hour']), int(groups['minute']))
    message = groups['message']
    action, guard_id = parse_message(message)
    return Event(date, time, action, guard_id)


def parse_message(message):
    guard_id = None
    if message.endswith(BEGINS_SHIFT):
        action = BEGINS_SHIFT
        guard_id = extract_id(message)
    elif message == FALLS_ASLEEP:
        action = FALLS_ASLEEP
    elif message == WAKES_UP:
        action = WAKES_UP
    else:
        raise ValueError('Could not parse: {}'.format(message))
    return action, guard_id


def extract_id(message):
    match = re.findall('#\d+', message)[0]
    return int(match.lstrip('#'))


def extract_sleeps(log):
    sleeps = []

    guard_id = None
    date = None
    start = None
    end = None

    for event in log:
        if event.action == BEGINS_SHIFT:
            guard_id = event.guard_id
        elif event.action == FALLS_ASLEEP:
            assert start is None
            date = event.date
            start = event.time.minute
        elif event.action == WAKES_UP:
            assert end is None
            end = event.time.minute
            assert event.date == date
            assert end > start
            # complete
            sleeps.append(Sleep(guard_id, date, start, end))
            # reset just the date and times, new guards reset guard
            date = None
            start = None
            end = None

    return sleeps


def strategy_1(sleeps):
    longest_sleeper = get_longest_sleeper(sleeps)
    most_slept_minute = most_frequently_slept_minute(sleeps, longest_sleeper)
    return longest_sleeper * most_slept_minute


def get_longest_sleeper(sleeps):
    total_sleep_times = collections.defaultdict(int)
    for sleep in sleeps:
        total_sleep_times[sleep.guard_id] += sleep.end - sleep.start
    return _max_by_value(total_sleep_times)


def most_frequently_slept_minute(sleeps, guard_id):
    sleeps_by_minute = collections.defaultdict(int)
    guard_sleeps = (sleep for sleep in sleeps if sleep.guard_id == guard_id)
    for sleep in guard_sleeps:
        for minute in range(sleep.start, sleep.end):
            sleeps_by_minute[minute] += 1
    return _max_by_value(sleeps_by_minute)


def _max_by_value(dct):
    return max(dct, key=lambda key: dct[key])


def strategy_2(sleeps):
    sleeps_by_minute = collections.defaultdict(collections.Counter)
    for sleep in sleeps:
        for minute in range(sleep.start, sleep.end):
            sleeps_by_minute[minute][sleep.guard_id] += 1
    worst_guard = None
    worst_minute = None
    highest_frequency = 0
    for minute, counter in sleeps_by_minute.items():
        guard_id, frequency = counter.most_common(1)[0]
        if frequency > highest_frequency:
            worst_guard = guard_id
            worst_minute = minute
            highest_frequency = frequency
    return worst_guard * worst_minute


def test_strategy_1(sleeps):
    value = strategy_1(sleeps)
    assert value == 240, value


def test_strategy_2(sleeps):
    value = strategy_2(sleeps)
    assert value == 4455, value


def get_input():
    with open('input.txt') as input_file:
        data = input_file.readlines()
    lines = (line.rstrip('\n') for line in data)
    return [line for line in lines if line]


if __name__ == '__main__':
    test_log = parse_log(TEST_LOG)
    test_sleeps = extract_sleeps(test_log)
    test_strategy_1(test_sleeps)
    test_strategy_2(test_sleeps)

    raw_log = get_input()
    log = parse_log(raw_log)
    sleeps = extract_sleeps(log)
    part_1 = strategy_1(sleeps)
    print(part_1)

    part_2 = strategy_2(sleeps)
    print(part_2)
