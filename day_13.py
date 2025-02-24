"""Day 13: Care Package"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from collections import defaultdict


def main():
    """Solve day 13 puzzles."""
    with open("data/day_13.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    program = load_program(puzzle_input)

    arcade = Arcade(program)
    arcade.play()

    return len(arcade.blocks)


def star_2(puzzle_input):
    """Solve second puzzle."""
    program = load_program(puzzle_input)

    arcade = Arcade(program)
    arcade.play(True)

    return arcade.score


class Arcade:
    """Arcade cabinet."""

    def __init__(self, program):
        self.blocks = set()
        self.score = 0
        self._program = defaultdict(int)
        self._i = 0
        self._relative_base = 0
        self._ball = None
        self._paddle = None

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

    def play(self, free=False):
        """Play a whole game."""
        if free:
            self._program[0] = 2

        joystick = 0
        halted = self.run(joystick)
        halted = self.run(joystick)

        old_ball = self._ball

        while not halted:
            if self._paddle[0] < 2 * self._ball[0] - old_ball[0]:
                joystick = 1
            elif self._paddle[0] > 2 * self._ball[0] - old_ball[0]:
                joystick = -1
            else:
                joystick = 0

            halted = self.run(joystick)
            old_ball = self._ball

    def run(self, input_):
        """Run arcade with given joystick input."""

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
                    self._program[index_1] = input_
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
                    return True

            if len(output) == 3:
                if output[:2] == [-1, 0]:
                    self.score = output[2]
                match output[2]:
                    case 0:
                        self.blocks.discard(tuple(output[:2]))
                    case 2:
                        self.blocks.add(tuple(output[:2]))
                    case 3:
                        self._paddle = tuple(output[:2])
                    case 4:
                        self._ball = tuple(output[:2])
                        break

                output = []

        return False


def load_program(puzzle_input):
    """Load program from input."""
    return tuple(map(int, puzzle_input.split(",")))


if __name__ == "__main__":
    main()
