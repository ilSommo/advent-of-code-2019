"""Day 12: The N-Body Problem"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import itertools
import math
from dataclasses import dataclass, field


@dataclass
class Moon:
    """Moon."""

    position: list[int]
    velocity: list[int] = field(default_factory=lambda: [0, 0, 0])


def main():
    """Solve day 12 puzzles."""
    with open("data/day_12.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    moons = load_moons(puzzle_input)

    for _ in range(1000):
        moons = step(moons)

    return sum(
        sum(abs(dimension) for dimension in moon.position)
        * sum(abs(dimension) for dimension in moon.velocity)
        for moon in moons
    )


def star_2(puzzle_input):
    """Solve second puzzle."""
    moons = load_moons(puzzle_input)
    initial = [
        [(moon.position[i], moon.velocity[i]) for moon in moons]
        for i in range(3)
    ]
    periods = []
    dimensions = {0, 1, 2}
    moons = step(moons, dimensions)
    i = 1

    while len(periods) < 3:
        to_remove = set()

        for j in dimensions:
            entry = [(moon.position[j], moon.velocity[j]) for moon in moons]

            if entry == initial[j]:
                periods.append(i)
                to_remove.add(j)

        if to_remove:
            dimensions -= to_remove

        moons = step(moons, dimensions)
        i += 1

    return math.lcm(*periods)


def load_moons(puzzle_input):
    """Load moons from input."""
    return [
        Moon(
            list(
                map(
                    int,
                    (chunk.split("=")[1] for chunk in line[1:-1].split(", ")),
                )
            ),
        )
        for line in puzzle_input
    ]


def step(moons, dimensions=(0, 1, 2)):
    """Perform a step on given dimensions."""
    return update_positions(update_velocities(moons, dimensions), dimensions)


def update_positions(moons, dimensions):
    """Update moons positions."""
    for moon in moons:
        for i in dimensions:
            moon.position[i] += moon.velocity[i]

    return moons


def update_velocities(moons, dimensions):
    """Update moons velocities."""
    for moon_0, moon_1 in itertools.combinations(moons, 2):
        for i in dimensions:
            if moon_1.position[i] > moon_0.position[i]:
                moon_0.velocity[i] += 1
                moon_1.velocity[i] -= 1
            elif moon_1.position[i] < moon_0.position[i]:
                moon_0.velocity[i] -= 1
                moon_1.velocity[i] += 1

    return moons


if __name__ == "__main__":
    main()
