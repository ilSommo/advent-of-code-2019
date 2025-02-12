"""Day 6: Universal Orbit Map"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

from functools import cache


def main():
    """Solve day 6 puzzles."""
    with open("data/day_6.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    orbits = load_orbits(puzzle_input)

    return sum(count_orbits(k[0], orbits) for k in orbits)


def star_2(puzzle_input):
    """Solve second puzzle."""
    orbits = load_orbits(puzzle_input)

    return compute_distance("YOU", "SAN", orbits)


def compute_distance(object_0, object_1, orbits):
    """Compute distance between two objects."""
    path_0 = compute_path(object_0, dict(orbits))
    path_1 = compute_path(object_1, dict(orbits))

    for object_ in path_0:
        if object_ in path_1:
            return path_0.index(object_) + path_1.index(object_)

    return 0


def compute_path(object_, orbits):
    """Compute path from object to origin."""
    path = []
    object_ = orbits[object_]
    while object_ != "COM":
        path.append(object_)
        object_ = orbits[object_]

    return path


@cache
def count_orbits(object_0, orbits):
    """Count direct and indirect orbits of an object."""
    object_1 = dict(orbits)[object_0]

    return 0 if object_1 is None else 1 + count_orbits(object_1, orbits)


def load_orbits(puzzle_input):
    """Load orbits graph from input."""
    orbits = {"COM": None}

    for line in puzzle_input:
        object_0, object_1 = line.split(")")
        orbits[object_1] = object_0

    return tuple(orbits.items())


if __name__ == "__main__":
    main()
