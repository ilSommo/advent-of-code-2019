"""Day 19: Tractor Beam"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import itertools
from collections import defaultdict

DIRECTIONS = {1j, -1j, -1, 1}


def main():
    """Solve day 19 puzzles."""
    with open("data/day_19.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    return sum(
        scan(i, j, puzzle_input)
        for i, j in itertools.product(range(50), repeat=2)
    )


def star_2(puzzle_input):
    """Solve second puzzle."""
    x = 99
    y = 0

    while (
        not scan(x, y, puzzle_input) == scan(x - 99, y + 99, puzzle_input) == 1
    ):
        if scan(x, y, puzzle_input) == 0:
            y += 1
        else:
            x += 1

    x -= 99

    return 10000 * x + y


class Intcode:
    """Intcode program."""

    def __init__(self, program):
        self._program = defaultdict(int)
        self._i = 0
        self._relative_base = 0

        for i, number in enumerate(program):
            self._program[i] = number

    def get_value(self, index, mode):
        """Get value of operand."""
        match mode:
            case 0:
                return self._program[self._program[index]]
            case 1:
                return self._program[index]
            case 2:
                return self._program[
                    self._program[index] + self._relative_base
                ]

    def run(self, inputs=None):
        """Run code with given input."""
        output = []

        while True:
            instruction = f"{self._program[self._i]:05}"
            opcode = int(instruction[3:])
            mode_1 = int(instruction[2])
            mode_2 = int(instruction[1])
            index_1 = self._program[self._i + 1] + self._relative_base * (
                instruction[2] == "2"
            )
            index_3 = self._program[self._i + 3] + self._relative_base * (
                instruction[0] == "2"
            )

            match opcode:
                case 1:
                    self._program[index_3] = self.get_value(
                        self._i + 1, mode_1
                    ) + self.get_value(self._i + 2, mode_2)
                    self._i += 4
                case 2:
                    self._program[index_3] = self.get_value(
                        self._i + 1, mode_1
                    ) * self.get_value(self._i + 2, mode_2)
                    self._i += 4
                case 3:
                    self._program[index_1] = inputs.pop(0)
                    self._i += 2
                case 4:
                    output.append(self.get_value(self._i + 1, mode_1))
                    self._i += 2
                case 5:
                    if self.get_value(self._i + 1, mode_1) != 0:
                        self._i = self.get_value(self._i + 2, mode_2)
                    else:
                        self._i += 3
                case 6:
                    if self.get_value(self._i + 1, mode_1) == 0:
                        self._i = self.get_value(self._i + 2, mode_2)
                    else:
                        self._i += 3
                case 7:
                    self._program[index_3] = int(
                        self.get_value(self._i + 1, mode_1)
                        < self.get_value(self._i + 2, mode_2)
                    )
                    self._i += 4
                case 8:
                    self._program[index_3] = int(
                        self.get_value(self._i + 1, mode_1)
                        == self.get_value(self._i + 2, mode_2)
                    )
                    self._i += 4
                case 9:
                    self._relative_base += self.get_value(self._i + 1, mode_1)
                    self._i += 2
                case 99:
                    break

        return output[0]


def load_program(puzzle_input):
    """Load program from input."""
    return Intcode(tuple(map(int, puzzle_input.split(","))))


def scan(x, y, puzzle_input):
    """Scan a location."""
    intcode = load_program(puzzle_input)

    return intcode.run([x, y])


if __name__ == "__main__":
    main()
