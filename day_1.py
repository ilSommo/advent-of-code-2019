"""Day 1: The Tyranny of the Rocket Equation"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"


def main():
    """Solve day 1 puzzles."""
    with open("data/day_1.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    return sum(int(line) // 3 - 2 for line in puzzle_input)


def star_2(puzzle_input):
    """Solve second puzzle."""
    fuel = 0

    for line in puzzle_input:
        mass = int(line)

        while mass > 0:
            mass = mass // 3 - 2
            fuel += max(0, mass)

    return fuel


if __name__ == "__main__":
    main()
