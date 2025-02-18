"""Day 7: Amplification Circuit"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import itertools
from collections import deque


class Amplifier:
    """Amplifier."""

    def __init__(self, program, phase):
        self._program = list(program)
        self._i = 0
        self.inputs = deque([phase])
        self.halted = False

    def get_value(self, index, mode):
        """Get value of operand."""
        match mode:
            case 0:
                return self._program[self._program[index]]
            case 1:
                return self._program[index]

    def run(self):
        """Run program."""
        while self._i < len(self._program):
            instruction = f"{self._program[self._i]:05}"
            opcode = int(instruction[3:])
            mode_1 = int(instruction[2])
            mode_2 = int(instruction[1])

            match opcode:
                case 1:
                    self._program[self._program[self._i + 3]] = self.get_value(
                        self._i + 1, mode_1
                    ) + self.get_value(self._i + 2, mode_2)
                    self._i += 4
                case 2:
                    self._program[self._program[self._i + 3]] = self.get_value(
                        self._i + 1, mode_1
                    ) * self.get_value(self._i + 2, mode_2)
                    self._i += 4
                case 3:
                    if not self.inputs:
                        return None
                    self._program[self._program[self._i + 1]] = (
                        self.inputs.popleft()
                    )
                    self._i += 2
                case 4:
                    output = self.get_value(self._i + 1, mode_1)
                    self._i += 2
                    return output
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
                    self._program[self._program[self._i + 3]] = int(
                        self.get_value(self._i + 1, mode_1)
                        < self.get_value(self._i + 2, mode_2)
                    )
                    self._i += 4
                case 8:
                    self._program[self._program[self._i + 3]] = int(
                        self.get_value(self._i + 1, mode_1)
                        == self.get_value(self._i + 2, mode_2)
                    )
                    self._i += 4
                case 99:
                    break

        self.halted = True

        return 0


def main():
    """Solve day 7 puzzles."""
    with open("data/day_7.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    program = load_program(puzzle_input)
    max_signal = 0

    for phases in itertools.permutations(range(5)):
        amplifiers = [Amplifier(program, phase) for phase in phases]
        signal = 0

        for amplifier in amplifiers:
            amplifier.inputs.append(signal)
            signal = amplifier.run()

        max_signal = max(max_signal, signal)

    return max_signal


def star_2(puzzle_input):
    """Solve second puzzle."""
    program = load_program(puzzle_input)
    max_signal = 0

    for phases in itertools.permutations(range(5, 10)):
        amplifiers = [Amplifier(program, phase) for phase in phases]
        amplifiers[0].inputs.append(0)
        output = 0
        i = 0

        while any(not amplifier.halted for amplifier in amplifiers):
            signal = amplifiers[i].run()

            if signal is not None:
                amplifiers[(i + 1) % 5].inputs.append(signal)

            if i == 4 and signal:
                output = signal

            i = (i + 1) % 5

        max_signal = max(max_signal, output)

    return max_signal


def load_program(puzzle_input):
    """Load program from input."""
    return tuple(map(int, puzzle_input.split(",")))


if __name__ == "__main__":
    main()
