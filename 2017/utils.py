import os


def get_input_data(day, strip=True):
    """Read input file for puzzle for given day.

    :param day: int, day of puzzle.
    :returns: str of input data.
    """
    path = _get_path(day)

    with open(path) as data_file:
        data = data_file.read()

        if strip:
            data = data.strip()

        return data


def _get_path(day):
    filename = 'aoc_{:02d}.txt'.format(day)
    return os.path.join('data', filename)
