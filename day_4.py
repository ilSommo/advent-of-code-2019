"""Day 4: Secure Container"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import re


def main():
    """Solve day 4 puzzles."""
    with open("data/day_4.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    return sum(map(is_password_1, load_range(puzzle_input)))


def star_2(puzzle_input):
    """Solve second puzzle."""
    return sum(map(is_password_2, load_range(puzzle_input)))


def is_password(password):
    """Check if a password is valid."""
    if len(password) != 6:
        return False

    for i, _ in enumerate(password[:-1]):
        if int(password[i]) > int(password[i + 1]):
            return False

    return True


def is_password_1(number):
    """Check if a password is valid for star 1."""
    password = str(number)

    if not is_password(password):
        return False

    return bool(re.search(r"(.)\1+", password))


def is_password_2(number):
    """Check if a password is valid for star 2."""
    password = str(number)

    if not is_password(password):
        return False

    return any(
        len(match_.group(0)) == 2
        for match_ in re.finditer(r"(.)\1+", password)
    )


def load_range(puzzle_input):
    """Load range from input."""
    return range(
        int(puzzle_input.split("-")[0]), int(puzzle_input.split("-")[1]) + 1
    )


if __name__ == "__main__":
    main()
