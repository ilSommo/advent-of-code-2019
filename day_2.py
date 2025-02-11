"""Day 2: 1202 Program Alarm"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"


def main():
    """Solve day 2 puzzles."""
    with open("data/day_2.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    numbers = load_numbers(puzzle_input)

    return run_program(numbers, 12, 2)


def star_2(puzzle_input):
    """Solve second puzzle."""
    numbers = load_numbers(puzzle_input)
    noun = 0

    while True:
        for verb in range(noun):
            if run_program(numbers, noun, verb) == 19690720:
                return 100 * noun + verb

        noun += 1


def load_numbers(puzzle_input):
    """Load list of integers from input."""
    return tuple(map(int, puzzle_input.split(",")))


def run_program(numbers, noun, verb):
    """Run program with given parameters."""
    numbers = list(numbers)
    numbers[1] = noun
    numbers[2] = verb

    for i in range(0, len(numbers), 4):
        try:
            match numbers[i]:
                case 1:
                    numbers[numbers[i + 3]] = (
                        numbers[numbers[i + 1]] + numbers[numbers[i + 2]]
                    )
                case 2:
                    numbers[numbers[i + 3]] = (
                        numbers[numbers[i + 1]] * numbers[numbers[i + 2]]
                    )
                case 99:
                    break
        except IndexError:
            break

    return numbers[0]


if __name__ == "__main__":
    main()
