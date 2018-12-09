import itertools

TEST_PLAYS = (
    # players, last_marble, expected_highest_score
    (9, 25, 32),
    (10, 1618, 8317),
    (13, 7999, 146373),
    (17, 1104, 2764),
    (21, 6111, 54718),
    (30, 5807, 37305)
)
NUM_PLAYERS = 476
LAST_MARBLE = 71431


class Player:

    def __init__(self):
        self.score = 0


class Marble:

    def __init__(self, id, clockwise=None, anticlockwise=None):
        self.id = id
        self.clockwise = clockwise or self
        self.anticlockwise = anticlockwise or self

    def __str__(self):
        return '{}<({})>{}'.format(
            self.anticlockwise.id,
            self.id,
            self.clockwise.id
        )


class Ring:

    def __init__(self, zeroth_marble):
        self.zeroth_marble = zeroth_marble
        self.current_marble = zeroth_marble
        self.marbles = {zeroth_marble.id: zeroth_marble}

    def take_turn(self, player, marble_id):
        if not marble_id % 23:
            to_remove = self.current_marble
            for _ in range(7):
                to_remove = to_remove.anticlockwise
            self.current_marble = to_remove.clockwise
            self.remove_marble(to_remove.id)
            player.score += to_remove.id + marble_id
        else:
            self.add_marble(marble_id)

    def add_marble(self, id):
        marble = Marble(
            id,
            clockwise=self.current_marble.clockwise.clockwise,
            anticlockwise=self.current_marble.clockwise
        )
        marble.anticlockwise.clockwise = marble
        marble.clockwise.anticlockwise = marble
        self.marbles[id] = marble
        self.current_marble = marble

    def remove_marble(self, id):
        marble_to_remove = self.marbles[id]
        clockwise = marble_to_remove.clockwise
        anticlockwise = marble_to_remove.anticlockwise
        clockwise.anticlockwise = anticlockwise
        anticlockwise.clockwise = clockwise
        del self.marbles[id]


def play_game(num_players, highest_marble):
    players = [Player() for _ in range(num_players)]
    players_and_marbles = zip(
        itertools.cycle(players),
        range(1, highest_marble + 1)
    )
    zeroth_marble = Marble(0)
    ring = Ring(zeroth_marble)
    for player, marble_id in players_and_marbles:
        ring.take_turn(player, marble_id)

    return players


def test_highest_score():
    for num_players, highest_marble, expected_highest_score in TEST_PLAYS:
        players = play_game(num_players, highest_marble)
        highest_score = max(player.score for player in players)
        assert highest_score == expected_highest_score, highest_score


def main():
    test_highest_score()

    players = play_game(NUM_PLAYERS, LAST_MARBLE)
    highest_score = max(player.score for player in players)
    print(highest_score)

    players = play_game(NUM_PLAYERS, LAST_MARBLE * 100)
    highest_score = max(player.score for player in players)
    print(highest_score)


if __name__ == '__main__':
    main()
