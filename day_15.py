"""Day 15: Oxygen System"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import copy
from collections import defaultdict, deque
from functools import cache

DIRECTIONS = {1: 1j, 2: -1j, 3: -1, 4: 1}


def main():
    """Solve day 15 puzzles."""
    with open("data/day_15.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    program = load_program(puzzle_input)

    return explore(program)[0]


def star_2(puzzle_input):
    """Solve second puzzle."""
    program = load_program(puzzle_input)

    _, oxygen, locations = explore(program)
    current = {oxygen}
    locations.remove(oxygen)
    i = 0

    while locations:
        i += 1
        new_current = set()

        for location in current:
            for direction in DIRECTIONS.values():
                if location + direction in locations:
                    new_current.add(location + direction)
                    locations.remove(location + direction)

        current = new_current

    return i


class Droid:
    """Repair droid."""

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

    def run(self, input_):
        """Run droid with given input."""
        output = None

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
                    self._program[index_1] = input_
                    self._i += 2
                case 4:
                    output = self.get_value(self._i + 1, mode_1)
                    self._i += 2
                    break
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


@cache
def explore(program):
    """Explore the map given by the program."""
    droid = Droid(program)

    oxygen = None
    distances = defaultdict(lambda: float("inf"))
    queue = deque([(droid, 0 + 0j, 0)])

    while queue:
        droid_0, location, steps = queue.popleft()

        if steps > distances[location]:
            continue

        distances[location] = steps

        for command, direction in DIRECTIONS.items():
            droid_1 = copy.deepcopy(droid_0)

            match droid_1.run(command):
                case 0:
                    continue
                case 1:
                    queue.append((droid_1, location + direction, steps + 1))
                case 2:
                    queue.append((droid_1, location + direction, steps + 1))
                    oxygen = location + direction

    return distances[oxygen], oxygen, set(distances.keys())


def load_program(puzzle_input):
    """Load program from input."""
    return tuple(map(int, puzzle_input.split(",")))


if __name__ == "__main__":
    main()
