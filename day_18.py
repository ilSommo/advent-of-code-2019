"""Day 18: Many-Worlds Interpretation"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

import heapq
from collections import defaultdict, deque

DIRECTIONS = (1, 1j, -1, -1j)


def main():
    """Solve day 18 puzzles."""
    with open("data/day_18.txt", encoding="ascii") as input_file:
        puzzle_input = tuple(line.rstrip() for line in input_file.readlines())

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    entrances, state = load_map(puzzle_input)

    return compute_min_distance(entrances, state)


def star_2(puzzle_input):
    """Solve second puzzle."""
    entrances, state = load_map(puzzle_input, split=True)

    return compute_min_distance(entrances, state)


def assign_quadrants(entrances, locations):
    """Assign locations to quadrants."""
    quadrants = defaultdict(set)

    for k, v in locations.items():
        distances = [abs(v - entrance) for entrance in entrances]
        quadrants[distances.index(min(distances))].add(k)

    return quadrants


def compute_distance(start, end, owned, state):
    """Compute distance between two locations."""
    paths = deque([(start, 0)])
    passages = state[0] | {end}
    keys = state[1]
    doors = state[2]

    best_paths = defaultdict(lambda: float("inf"))

    for key in owned:
        passages.add(keys[key])

        if key in doors:
            passages.add(doors[key])

    while paths:
        location, steps = paths.pop()

        if location == end:
            return steps

        if steps < best_paths[location]:
            best_paths[location] = steps
            steps += 1

            for direction in DIRECTIONS:
                new_location = location + direction

                if new_location in passages:
                    paths.appendleft((new_location, steps))

    return None


def compute_min_distance(entrances, state):
    """Compute minimum distance to collect all keys."""
    quadrant_keys = assign_quadrants(entrances, state[1])
    quadrant_doors = assign_quadrants(entrances, state[2])

    paths = [
        (
            0,
            tuple(
                (int(location.real), int(location.imag))
                for location in entrances
            ),
            frozenset(),
        )
    ]
    best = {
        "locations": defaultdict(lambda: defaultdict(lambda: float("inf"))),
        "owned": defaultdict(lambda: float("inf")),
    }
    distances = defaultdict(dict)

    while paths:
        steps, locations, owned = heapq.heappop(paths)

        if len(owned) == len(state[1]):
            return steps

        if any(
            owned < k and steps >= v for k, v in best["owned"].items()
        ) or any(
            owned <= k and steps >= v
            for k, v in best["locations"][locations].items()
        ):
            continue

        best["locations"][locations][owned] = steps
        best["owned"][owned] = steps

        for i, _ in enumerate(locations):
            location = locations[i][0] + locations[i][1] * 1j

            for key, key_location in state[1].items():
                if key in owned or key not in quadrant_keys[i]:
                    continue

                distance = next(
                    (
                        v
                        for k, v in distances[(location, key_location)].items()
                        if owned & quadrant_doors[i] >= k
                    ),
                    None,
                )

                if not distance:
                    distance = compute_distance(
                        location, key_location, owned, state
                    )
                    distances[(location, key_location)][
                        owned & quadrant_doors[i]
                    ] = distance

                if distance:
                    heapq.heappush(
                        paths,
                        (
                            steps + distance,
                            locations[:i]
                            + (
                                (
                                    int(key_location.real),
                                    int(key_location.imag),
                                ),
                            )
                            + locations[i + 1 :],
                            frozenset(owned | {key}),
                        ),
                    )

    return None


def load_map(puzzle_input, split=False):
    """Load map from input."""
    entrances = []
    passages = set()
    keys = {}
    doors = {}

    for i, line in enumerate(puzzle_input):
        for j, char in enumerate(line):
            if char == ".":
                passages.add(i + j * 1j)
            elif char.islower():
                keys[char] = i + j * 1j
            elif char.isupper():
                doors[char.lower()] = i + j * 1j
            elif char == "@":
                passages.add(i + j * 1j)
                entrances.append(i + j * 1j)

    if split is True:
        entrance = entrances.pop(0)
        passages.remove(entrance)

        for offset in (1 + 1j, 1 - 1j, -1 - 1j, -1 + 1j):
            entrances.append(entrance + offset)

        for direction in DIRECTIONS:
            passages.remove(entrance + direction)

    return (
        entrances,
        (passages, keys, doors),
    )


if __name__ == "__main__":
    main()
