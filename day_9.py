"""Day 9: Sensor Boost"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from collections import defaultdict


def main():
    """Solve day 9 puzzles."""
    with open("data/day_9.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    program = load_program(puzzle_input)

    return run_program(program, 1)[0]


def star_2(puzzle_input):
    """Solve second puzzle."""
    program = load_program(puzzle_input)

    return run_program(program, 2)[0]


def get_value(program, index, mode, relative_base):
    """Get value of operand."""
    match mode:
        case 0:
            return program[program[index]]
        case 1:
            return program[index]
        case 2:
            return program[program[index] + relative_base]


def load_program(puzzle_input):
    """Load program from input."""
    return tuple(map(int, puzzle_input.split(",")))


def run_program(program_, input_):
    """Run program with given parameters."""
    program = defaultdict(int)

    for i, number in enumerate(program_):
        program[i] = number

    output = []
    i = 0
    relative_base = 0

    while True:
        instruction = f"{program[i]:05}"
        opcode = int(instruction[3:])
        mode_1 = int(instruction[2])
        mode_2 = int(instruction[1])
        index_1 = program[i + 1] + relative_base * (instruction[2] == "2")
        index_3 = program[i + 3] + relative_base * (instruction[0] == "2")

        match opcode:
            case 1:
                program[index_3] = get_value(
                    program, i + 1, mode_1, relative_base
                ) + get_value(program, i + 2, mode_2, relative_base)
                i += 4
            case 2:
                program[index_3] = get_value(
                    program, i + 1, mode_1, relative_base
                ) * get_value(program, i + 2, mode_2, relative_base)
                i += 4
            case 3:
                program[index_1] = input_
                i += 2
            case 4:
                output.append(get_value(program, i + 1, mode_1, relative_base))
                i += 2
            case 5:
                if get_value(program, i + 1, mode_1, relative_base) != 0:
                    i = get_value(program, i + 2, mode_2, relative_base)
                else:
                    i += 3
            case 6:
                if get_value(program, i + 1, mode_1, relative_base) == 0:
                    i = get_value(program, i + 2, mode_2, relative_base)
                else:
                    i += 3
            case 7:
                program[index_3] = int(
                    get_value(program, i + 1, mode_1, relative_base)
                    < get_value(program, i + 2, mode_2, relative_base)
                )
                i += 4
            case 8:
                program[index_3] = int(
                    get_value(program, i + 1, mode_1, relative_base)
                    == get_value(program, i + 2, mode_2, relative_base)
                )
                i += 4
            case 9:
                relative_base += get_value(
                    program, i + 1, mode_1, relative_base
                )
                i += 2
            case 99:
                break

    return tuple(output)


if __name__ == "__main__":
    main()
