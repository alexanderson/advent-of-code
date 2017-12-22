
class Spinlock:

    def __init__(self, steps_per_move):
        self.buffer = [0]
        self.value = 0

        self.position = 0
        self.steps_per_move = steps_per_move

    def step(self, steps):
        self.position = (self.position + steps) % len(self.buffer)

    def move(self):
        self.step(self.steps_per_move)
        self.value += 1
        self.position += 1
        self.buffer.insert(self.position, self.value)

    def run(self, num_moves):
        for _ in range(num_moves):
            self.move()

    def get_next(self):
        return self.buffer[self.position + 1]


class ShortcutSpinLock(Spinlock):
    """Spinlock simulator which doesn't evolve the buffer, but tracks the
    number after 0."""

    def __init__(self, steps_per_move):
        super().__init__(steps_per_move)
        self.size = 1
        self.value_after_zero = 0

    def step(self, steps):
        self.position = (self.position + steps) % self.size

    def move(self):
        self.step(self.steps_per_move)
        self.value += 1
        self.position += 1
        self.size += 1
        if self.position == 1:
            self.value_after_zero = self.value


def main():
    test()

    lock = Spinlock(steps_per_move=355)
    lock.run(2017)
    next_val = lock.get_next()

    print(f'part a: {next_val}')

    lock = ShortcutSpinLock(steps_per_move=355)
    lock.run(50000000)
    value = lock.value_after_zero

    print(f'part b: {value}')


def test():
    lock = Spinlock(steps_per_move=3)
    lock.run(2017)
    next_val = lock.get_next()

    assert next_val == 638, next_val


if __name__ == '__main__':
    main()
