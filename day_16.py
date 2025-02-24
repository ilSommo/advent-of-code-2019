"""Day 16: Flawed Frequency Transmission"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from collections import deque


def main():
    """Solve day 16 puzzles."""
    with open("data/day_16.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    signal = load_signal(puzzle_input)
    patterns = compute_patterns(len(signal))

    for _ in range(100):
        signal = compute_signal(signal, patterns)

    return "".join(map(str, signal[:8]))


def star_2(puzzle_input):
    """Solve second puzzle."""
    signal = 10000 * load_signal(puzzle_input)
    offset = int("".join(map(str, signal[:7])))
    signal = signal[offset:]

    for _ in range(100):
        new_signal = deque()
        total = 0

        for digit in signal[::-1]:
            total = (total + digit) % 10
            new_signal.appendleft(total)

        signal = tuple(new_signal)

    return "".join(map(str, signal[:8]))


def compute_pattern(i, length):
    """Computer a single pattern."""
    add = []
    sub = []

    i += 1
    j = i

    while j < length + 1:
        add.extend([k - 1 for k in range(j, min(j + i, length + 1))])
        j += 2 * i

        if j < length + 1:
            sub.extend([k - 1 for k in range(j, min(j + i, length + 1))])
            j += 2 * i

    return (tuple(add), tuple(sub))


def compute_patterns(length):
    """Compute all patterns."""
    return tuple(compute_pattern(i, length) for i in range(length))


def compute_signal(signal, patterns):
    """Compute new signal."""
    outputs = []

    for pattern in patterns:
        output = 0

        for i in pattern[0]:
            output += signal[i]

        for i in pattern[1]:
            output -= signal[i]

        outputs.append(output)

    return tuple(abs(output) % 10 for output in outputs)


def load_signal(puzzle_input):
    """Load signal from input."""
    return tuple(int(digit) for digit in puzzle_input)


if __name__ == "__main__":
    main()
