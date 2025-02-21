"""Day 14: Space Stoichiometry"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import math
from collections import defaultdict

MAX_ORE = 1000000000000


def main():
    """Solve day 14 puzzles."""
    with open("data/day_14.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    reactions = load_reactions(puzzle_input)

    return fuel_to_ore(reactions, 1)


def star_2(puzzle_input):
    """Solve second puzzle."""
    reactions = load_reactions(puzzle_input)
    min_fuel = 0
    max_fuel = MAX_ORE

    while max_fuel - min_fuel > 1:
        fuel = (max_fuel + min_fuel) // 2
        ore = fuel_to_ore(reactions, fuel)

        if ore <= MAX_ORE:
            min_fuel = fuel
        else:
            max_fuel = fuel

    return min_fuel


def fuel_to_ore(reactions, fuel):
    """Convert fuel to ore."""
    totals = defaultdict(lambda: [0, 0])
    totals["ORE"] = 0
    needed = [("FUEL", fuel)]

    while needed:
        element, needed_quantity = needed.pop(0)

        if element == "ORE":
            totals[element] += needed_quantity
            continue

        min_quantity, inputs = reactions[element]

        if totals[element][1] - totals[element][0] < needed_quantity:
            batches = math.ceil(
                (needed_quantity - totals[element][1] + totals[element][0])
                / min_quantity
            )

            totals[element][1] += batches * min_quantity

            for chemical in inputs:
                needed.append((chemical[0], batches * chemical[1]))

        totals[element][0] += needed_quantity

    return totals["ORE"]


def load_reactions(puzzle_input):
    """Load reactions from input."""
    return dict(parse_rection(line) for line in puzzle_input)


def parse_chemical(chemical):
    """Parse a single chemical."""
    chemical = chemical.split()

    return chemical[1], int(chemical[0])


def parse_rection(reaction):
    """Parse a single reaction."""
    inputs, output = reaction.split(" => ")
    inputs = inputs.split(", ")

    inputs = tuple(parse_chemical(chemical) for chemical in inputs)
    output = parse_chemical(output)

    return output[0], (output[1], inputs)


if __name__ == "__main__":
    main()
