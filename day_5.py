"""Day 5: Sunny with a Chance of Asteroids"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"


def main():
    """Solve day 5 puzzles."""
    with open("data/day_5.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    numbers = load_numbers(puzzle_input)

    return run_program(numbers, 1)


def star_2(puzzle_input):
    """Solve second puzzle."""
    numbers = load_numbers(puzzle_input)

    return run_program(numbers, 5)


def get_value(numbers, index, mode):
    """Get value of operand."""
    match mode:
        case 0:
            return numbers[numbers[index]]
        case 1:
            return numbers[index]


def load_numbers(puzzle_input):
    """Load list of integers from input."""
    return tuple(map(int, puzzle_input.split(",")))


def run_program(numbers, input_):
    """Run program with given parameters."""
    numbers = list(numbers)
    output = 0
    i = 0

    while i < len(numbers):
        instruction = f"{numbers[i]:05}"
        opcode = int(instruction[3:])
        mode_1 = int(instruction[2])
        mode_2 = int(instruction[1])

        match opcode:
            case 1:
                numbers[numbers[i + 3]] = get_value(
                    numbers, i + 1, mode_1
                ) + get_value(numbers, i + 2, mode_2)
                i += 4
            case 2:
                numbers[numbers[i + 3]] = get_value(
                    numbers, i + 1, mode_1
                ) * get_value(numbers, i + 2, mode_2)
                i += 4
            case 3:
                numbers[numbers[i + 1]] = input_
                i += 2
            case 4:
                output = get_value(numbers, i + 1, mode_1)
                i += 2
            case 5:
                if get_value(numbers, i + 1, mode_1) != 0:
                    i = get_value(numbers, i + 2, mode_2)
                else:
                    i += 3
            case 6:
                if get_value(numbers, i + 1, mode_1) == 0:
                    i = get_value(numbers, i + 2, mode_2)
                else:
                    i += 3
            case 7:
                numbers[numbers[i + 3]] = int(
                    get_value(numbers, i + 1, mode_1)
                    < get_value(numbers, i + 2, mode_2)
                )
                i += 4
            case 8:
                numbers[numbers[i + 3]] = int(
                    get_value(numbers, i + 1, mode_1)
                    == get_value(numbers, i + 2, mode_2)
                )
                i += 4
            case 99:
                break

        if output != 0:
            return output

    return 0


if __name__ == "__main__":
    main()
