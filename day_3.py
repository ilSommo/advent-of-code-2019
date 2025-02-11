"""Day 3: Crossed Wires"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

DIRECTIONS = {"D": -1j, "L": -1, "R": +1, "U": +1j}


def main():
    """Solve day 3 puzzles."""
    with open("data/day_3.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    wire_0, wire_1 = load_wires(puzzle_input)

    return min(
        map(
            lambda point: int(abs(point.real) + abs(point.imag)),
            set(wire_0[1:]) & set(wire_1[1:]),
        )
    )


def star_2(puzzle_input):
    """Solve second puzzle."""
    wire_0, wire_1 = load_wires(puzzle_input)

    return min(
        map(
            lambda point: wire_0.index(point) + wire_1.index(point),
            set(wire_0[1:]) & set(wire_1[1:]),
        )
    )


def load_wire(path):
    """Load wire from path."""
    wire = [0 + 0j]

    for step in path.split(","):
        wire.extend(
            [
                wire[-1] + DIRECTIONS[step[0]] * (i + 1)
                for i in range(int(step[1:]))
            ]
        )

    return wire


def load_wires(puzzle_input):
    """Load wires from input."""
    return load_wire(puzzle_input[0]), load_wire(puzzle_input[1])


if __name__ == "__main__":
    main()
