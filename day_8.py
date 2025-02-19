"""Day 8: Space Image Format"""

__author__ = "Martino M. L. Pulici <martinomarelakota@yahoo.it>"
__date__ = "2025"
__license__ = "MIT"

HEIGHT = 6
WIDTH = 25


def main():
    """Solve day 8 puzzles."""
    with open("data/day_8.txt", encoding="ascii") as input_file:
        puzzle_input = input_file.read().rstrip()

    print(star_1(puzzle_input))
    print(star_2(puzzle_input))


def star_1(puzzle_input):
    """Solve first puzzle."""
    image = load_image(puzzle_input)

    layers = ["".join(row for row in layer) for layer in image]
    layer_zeros = [layer.count("0") for layer in layers]
    layer = layers[layer_zeros.index(min(layer_zeros))]

    return layer.count("1") * layer.count("2")


def star_2(puzzle_input):
    """Solve second puzzle."""
    image = load_image(puzzle_input)
    decoded_image = []

    for i, row in enumerate(image[0]):
        decoded_row = ""

        for j, _ in enumerate(row):
            for layer in image:
                if layer[i][j] != "2":
                    decoded_row += " " if layer[i][j] == "0" else "#"
                    break

        decoded_image.append(decoded_row)

    return "\n".join(decoded_image)


def load_image(puzzle_input):
    """Load encrypted from input."""
    layer_size = HEIGHT * WIDTH
    image = tuple(
        tuple(
            puzzle_input[i * layer_size : (i + 1) * layer_size][
                j * WIDTH : (j + 1) * WIDTH
            ]
            for j in range(layer_size // WIDTH)
        )
        for i in range(len(puzzle_input) // layer_size)
    )
    return image


if __name__ == "__main__":
    main()
