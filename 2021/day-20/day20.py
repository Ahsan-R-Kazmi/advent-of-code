from typing import List, Dict, Tuple

WINDOW_SIZE = 3
WINDOW = [[-1, -1], [-1, 0], []]
DEBUG = True


def get_default_value(iteration: int, enhancement_algorithm: str):
    if enhancement_algorithm[0] == '#' and enhancement_algorithm[-1] == ".":
        if iteration % 2 == 0:
            return "."
        else:
            return "#"
    elif enhancement_algorithm[0] == "#" and enhancement_algorithm[-1] == '#':
        return "#"
    return "."


def enhance_image(input_image: Dict[Tuple[int, int], str], enhancement_algorithm: str, iteration: int) -> Dict[Tuple[int, int], str]:

    new_input_image: Dict[Tuple[int, int], str] = {}
    for point, _ in input_image.items():

        for i in range(-2, 1):
            for j in range(-2, 1):
                row = point[0] + i
                col = point[1] + j
                binary_str = ""
                for k in range(0, 3):
                    for m in range(0, 3):
                        a = row + k
                        b = col + m
                        value = input_image.get((a, b), get_default_value(iteration, enhancement_algorithm))
                        binary_str += '1' if value == '#' else '0'

                new_input_image[(row, col)] = enhancement_algorithm[int(binary_str, 2)]

    return new_input_image


def print_image(image: Dict[Tuple[int, int], str]):
    min_row = float("inf")
    min_col = float("inf")
    max_row = 0
    max_col = 0
    for point, _ in image.items():
        min_row = min(min_row, point[0])
        min_col = min(min_col, point[1])
        max_row = max(max_row, point[0])
        max_col = max(max_col, point[1])

    image_grid = [['.' for _ in range(max_col + 1)] for _ in range(max_row + 1)]

    for point, value in image.items():
        image_grid[point[0]][point[1]] = value

    for i in range(min_row, max_row + 1):
        row: str = ""
        for j in range(min_col, max_col + 1):
            row += image.get((i, j), '.')

        print(row)

    print()


def count_lit_image_pixels(image: Dict[Tuple[int, int], str]) -> int:
    lit_pixels = 0
    for _, value in image.items():
        if value == '#':
            lit_pixels += 1
    return lit_pixels


def count_lit_output_image_pixels(iterations: int) -> int:
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        enhancement_algorithm: str = lines[0]
        input_image: Dict[Tuple[int, int], str] = {}
        lines = lines[2:]
        for i in range(0, len(lines)):
            row: List[str] = list(lines[i])
            for j in range(len(row)):
                input_image[(i, j)] = row[j]

        for iteration in range(iterations):
            output_image = enhance_image(input_image, enhancement_algorithm, iteration)
            input_image = output_image
            if DEBUG:
                print_image(output_image)

        return count_lit_image_pixels(output_image)


if __name__ == '__main__':
    print(count_lit_output_image_pixels(2))
    print(count_lit_output_image_pixels(50))

