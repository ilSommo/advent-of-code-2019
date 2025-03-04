"""Day 17: Set and Forget"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from collections import defaultdict

DIRECTIONS = {1j, -1j, -1, 1}


def main():
    """Solve day 17 puzzles."""
    with open("data/day_17.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    scaffolds = get_scaffolds(puzzle_input)[0]
    intersections = {
        scaffold
        for scaffold in scaffolds
        if all(scaffold + direction in scaffolds for direction in DIRECTIONS)
    }

    return sum(
        int(intersection.real * intersection.imag)
        for intersection in intersections
    )


def star_2(puzzle_input):
    """Solve second puzzle."""
    robot = load_program("2" + puzzle_input[1:])

    path = compute_path(puzzle_input)

    return robot.run(path)[-1]


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

        return output


def compress(instructions):
    """Compress instructions into parsable form."""
    for i in range(1, 21):
        if instructions[i].isdigit() or instructions[i - 1] == ",":
            continue

        a = instructions[:i]
        instructions_a = instructions.replace(a, i * "A")

        while instructions_a[i] in ",A":
            i += 1

        for j in range(1, 21):
            if instructions[i + j].isdigit() or instructions[i + j - 1] == ",":
                continue

            b = instructions_a[i : i + j]
            instructions_b = instructions_a.replace(b, j * "B")

            while instructions_b[i + j] in ",AB":
                j += 1

            for k in range(1, 21):
                if (
                    instructions[i + j + k].isdigit()
                    or instructions[i + j + k - 1] == ","
                ):
                    continue

                c = instructions_b[i + j : i + j + k]
                instructions_c = instructions_b.replace(c, k * "C")

                if all(char in ",ABC" for char in instructions_c):
                    instructions_c = (
                        instructions_c.replace("A" * len(a), "A")
                        .replace("B" * len(b), "B")
                        .replace("C" * len(c), "C")
                    )

                    return list(
                        map(
                            ord, "\n".join((instructions_c, a, b, c)) + "\nn\n"
                        )
                    )

    return None


def compute_path(puzzle_input):
    """Compute robot path from input."""
    scaffolds, robot = get_scaffolds(puzzle_input)
    location, direction = robot
    path = []
    visited = {location}

    while visited != scaffolds:
        if location + direction in scaffolds:
            location += direction
            visited.add(location)
            path[-1] += 1
        elif location + direction * 1j in scaffolds:
            direction *= 1j
            path += ["L", 0]
        else:
            direction *= -1j
            path += ["R", 0]

    return compress(",".join(map(str, path)))


def get_scaffolds(puzzle_input):
    """Get scaffolds from input."""
    intcode = load_program(puzzle_input)
    output = intcode.run()

    scaffolds = set()
    i = j = 0

    for char in output:
        match char:
            case 35:
                scaffolds.add(i + j * 1j)
            case 60:
                robot = (i + j * 1j, -1j)
            case 62:
                robot = (i + j * 1j, +1j)
            case 94:
                robot = (i + j * 1j, -1)
            case 118:
                robot = (i + j * 1j, +1)
            case 10:
                j = -1
                i += 1

        j += 1

    return scaffolds | {robot[0]}, robot


def load_program(puzzle_input):
    """Load program from input."""
    return Intcode(tuple(map(int, puzzle_input.split(","))))


if __name__ == "__main__":
    main()
