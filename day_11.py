"""Day 11: Space Police"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from collections import defaultdict


def main():
    """Solve day 11 puzzles."""
    with open("data/day_11.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    program = load_program(puzzle_input)

    return len(full_run(program, 0)[0])


def star_2(puzzle_input):
    """Solve second puzzle."""
    program = load_program(puzzle_input)

    white = full_run(program, 1)[1]
    range_x, range_y = compute_ranges(white)

    return "\n".join(
        "".join("#" if i + j * 1j in white else " " for i in range_x)
        for j in range_y
    )


class Robot:
    """Painting robot."""

    def __init__(self, program):
        self.location = 0 + 0j
        self._direction = 1j
        self._i = 0
        self._relative_base = 0
        self._program = defaultdict(int)

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

    def run(self, panel):
        """Run robot with given panel."""
        output = []

        while len(output) < 2:
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
                    self._program[index_1] = panel
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
                    return None

        self._direction *= 1j if output[1] == 0 else -1j
        self.location += self._direction

        return output[0]


def compute_ranges(white):
    """Compute ranges to print."""
    min_x = int(min(location.real for location in white))
    max_x = int(max(location.real for location in white))
    min_y = int(min(location.imag for location in white))
    max_y = int(max(location.imag for location in white))

    return range(min_x, max_x + 1), range(max_y, min_y - 1, -1)


def full_run(program, panel):
    """Perform a full run starting with a given panel."""
    robot = Robot(program)
    paint = panel

    painted = set()
    white = {0 + 0j} if paint == 1 else set()

    while paint is not None:
        location = robot.location
        paint = robot.run(int(robot.location in white))

        if paint == 0:
            white.discard(location)
        elif paint == 1:
            white.add(location)

        painted.add(location)

    return painted, white


def load_program(puzzle_input):
    """Load program from input."""
    return tuple(map(int, puzzle_input.split(",")))


if __name__ == "__main__":
    main()
