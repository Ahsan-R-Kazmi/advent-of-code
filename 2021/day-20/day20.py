from typing import List
import numpy as np

WINDOW_SIZE = 3


def create_blank_input_image(input_image: List[List[str]]) -> List[List[str]]:
    new_image: List[List[str]] = [['.' for _ in range(len(input_image))] for _ in range(len(input_image[0]))]
    return new_image


def get_pad_fill_values(iteration: int, enhancement_algorithm: str):
    if enhancement_algorithm[0] == '#' and enhancement_algorithm[-1] == ".":
        if iteration % 2 == 0:
            return 0
        else:
            return 1
    elif enhancement_algorithm[0] == "#" and enhancement_algorithm[-1] == '#':
        return 1
    return 0


def enhance_image(input_image: List[List[int]], enhancement_algorithm: str, iteration: int) -> List[List[int]]:
    input_image = np.pad(input_image, (WINDOW_SIZE - 1, WINDOW_SIZE - 1), mode='constant',
                         constant_values=get_pad_fill_values(iteration, enhancement_algorithm))
    new_input_image = np.copy(input_image)
    for i in range(len(input_image)):
        for j in range(len(input_image[i])):
            binary_str = ""
            for k in range(-1, WINDOW_SIZE - 1):
                for l in range(-1, WINDOW_SIZE - 1):
                    row = k + i
                    col = l + j

                    if row < 0 or col < 0 or row >= len(new_input_image) or col >= len(input_image[i]):
                        continue

                    binary_str += str(input_image[row][col])

            num = int(binary_str, 2)
            new_input_image[i][j] = 1 if enhancement_algorithm[num] == "#" else 0

    return new_input_image


def print_image(image: List[List[int]]):
    for i in range(len(image)):
        row: str = ""
        for j in range(len(image[0])):
            row += "#" if image[i][j] == 1 else '.'

        print(row)


def count_lit_image_pixels(image: List[List[int]]) -> int:
    lit_pixels = 0
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] == 1:
                lit_pixels += 1

    return lit_pixels


def count_lit_output_image_pixels() -> int:
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        enhancement_algorithm: str = lines[0]
        input_image: List[List[int]] = []
        for i in range(2, len(lines)):
            row: List[str] = list(lines[i])
            row: List[int] = [0 if row[i] == "." else 1 for i in range(len(row))]
            input_image.append(row)
        input_image = np.asarray(input_image)

        for iteration in range(2):
            output_image = enhance_image(input_image, enhancement_algorithm, iteration)
            input_image = output_image
            print_image(output_image)
            print()

        return count_lit_image_pixels(output_image)


if __name__ == '__main__':
    print(count_lit_output_image_pixels())
