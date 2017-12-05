import os


def get_input_data(day):
    """Read input file for puzzle for given day.

    :param day: int, day of puzzle.
    :returns: str of input data.
    """
    path = _get_path(day)

    with open(path) as data_file:
        return data_file.read().strip()


def _get_path(day):
    filename = 'aoc_{:02d}.txt'.format(day)
    return os.path.join('data', filename)
