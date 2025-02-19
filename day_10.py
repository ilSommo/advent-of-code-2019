"""Day 10: Monitoring Station"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import cmath
from collections import defaultdict, deque
from math import pi


def main():
    """Solve day 10 puzzles."""
    with open("data/day_10.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    asteroids = load_asteroids(puzzle_input)

    return get_station(asteroids)[1]


def star_2(puzzle_input):
    """Solve second puzzle."""
    asteroids = load_asteroids(puzzle_input)

    station = get_station(asteroids)[0]
    asteroids.remove(station)

    asteroids = sorted(asteroids, key=lambda asteroid: abs(asteroid - station))

    groups = defaultdict(deque)

    for asteroid in asteroids:
        groups[cmath.phase(asteroid - station)].append(asteroid)

    groups = deque(
        [groups[direction] for direction in sorted(groups, key=shift_phase)]
    )

    order = []

    while len(order) < 200:
        group = groups.popleft()
        order.append(group.popleft())

        if group:
            groups.append(group)

    last = order[-1]

    return int(last.real * 100 + last.imag)


def get_station(asteroids):
    """Get coordinate and visibility of the best asteroid to use as station."""
    return max(
        {
            asteroid_0: len(
                {
                    cmath.phase(asteroid_1 - asteroid_0)
                    for asteroid_1 in asteroids - {asteroid_0}
                }
            )
            for asteroid_0 in asteroids
        }.items(),
        key=lambda item: item[1],
    )


def load_asteroids(puzzle_input):
    """Load asteroids from input."""
    return {
        i + j * 1j
        for j, row in enumerate(puzzle_input)
        for i, elem in enumerate(row)
        if elem == "#"
    }


def shift_phase(phase):
    """Shift the phase in order to start from the top."""
    return phase if phase >= -pi / 2 else phase + 2 * pi


if __name__ == "__main__":
    main()
