import ast
import copy
import math
from typing import Optional, List, Tuple

DEBUG = False


# Add the left real number in this pair to first real number to the left.
def add_left_real_number(i: int, n: List, real_number: int) -> bool:
    real_number_added = False
    for j in range(i - 1, -1, -1):
        if type(n[j]) is list:
            return add_left_real_number(len(n[j]), n[j], real_number)

        n[j] += real_number
        real_number_added = True
        break

    return real_number_added


# Add the right real number in this pair to first real number to the right.
def add_right_real_number(i: int, n: List, real_number: int) -> bool:
    real_number_added = False
    for j in range(i + 1, len(n)):
        if type(n[j]) is list:
            return add_right_real_number(-1, n[j], real_number)

        n[j] += real_number
        real_number_added = True
        break

    return real_number_added


def explode_snailfish_number(n: List, level: int) -> [bool, Optional[int], Optional[int]]:
    operation_performed: bool = False
    left_number = None
    right_number = None

    if level == 5:
        raise ValueError("This level of nesting was not expected.")

    if level == 4:
        index_to_replace = None
        for i in range(len(n)):

            if type(n[i]) is not list:
                continue

            index_to_replace = i
            # Add the left real number in this pair to first real number to the left.
            left_number_added = add_left_real_number(i, n, n[i][0])

            if not left_number_added:
                left_number = n[i][0]

            # Add the right real number in this pair to first real number to the right.
            right_number_added = add_right_real_number(i, n, n[i][1])

            if not right_number_added:
                right_number = n[i][1]

            break

        if index_to_replace is not None:
            operation_performed = True
            n[index_to_replace] = 0
        return operation_performed, left_number, right_number

    for i in range(len(n)):
        if type(n[i]) is not list:
            continue

        result = explode_snailfish_number(n[i], level + 1)
        if result[0]:
            operation_performed = result[0]
            if result[1] is not None and not add_left_real_number(i, n, real_number=result[1]):
                left_number = result[1]
            if result[2] is not None and not add_right_real_number(i, n, real_number=result[2]):
                right_number = result[2]

            break

    return operation_performed, left_number, right_number


def split_number(n: List, i: int):
    left_number = math.floor(n[i] / 2)
    right_number = math.ceil(n[i] / 2)

    n[i] = [left_number, right_number]


def split_snailfish_number(n: List) -> bool:
    for i in range(len(n)):
        if type(n[i]) is list:
            # If a number has already been split, then return true, since this would be the left-most number, and we do
            # not want to split any more numbers.
            if split_snailfish_number(n[i]):
                return True
        elif n[i] >= 10:
            split_number(n, i)
            # Return true since we only want to split the left-most number.
            return True

    # Return false if no numbers are split.
    return False


def reduce_snailfish_numbers(n: List) -> List:
    snailfish_number_exploded = True
    snailfish_number_split = True
    if DEBUG:
        print("original", n)
    while snailfish_number_exploded or snailfish_number_split:
        snailfish_number_exploded = explode_snailfish_number(n, 1)[0]
        if DEBUG:
            print("After explode:", n)
        if snailfish_number_exploded:
            continue

        snailfish_number_split = split_snailfish_number(n)
        if DEBUG:
            print("After split:", n)

    return n


def add_snailfish_numbers(a: List, b: List) -> List:
    return [a, b]


def compute_magnitude(n: List) -> int:
    a = n[0]
    b = n[1]
    if type(a) is list:
        a = compute_magnitude(a)

    if type(b) is list:
        b = compute_magnitude(b)

    return 3 * a + 2 * b


def compute_snailfish_numbers_addition_result() -> Tuple[int, int]:
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        a: List = ast.literal_eval(lines[0])

        for i in range(1, len(lines)):
            b: List = ast.literal_eval(lines[i])
            c: List = add_snailfish_numbers(a, b)

            reduce_snailfish_numbers(c)

            a = c

        largest_sum = 0
        for line_a in lines:
            a = ast.literal_eval(line_a)
            for line_b in lines:
                b = ast.literal_eval(line_b)
                if a == b:
                    continue

                largest_sum = max(largest_sum,
                                  max(compute_magnitude(reduce_snailfish_numbers(
                                      add_snailfish_numbers(copy.deepcopy(a), copy.deepcopy(b)))),
                                      compute_magnitude(reduce_snailfish_numbers(
                                          add_snailfish_numbers(copy.deepcopy(b), copy.deepcopy(a))))
                                  )
                                  )

        return compute_magnitude(c), largest_sum


if __name__ == '__main__':
    print(compute_snailfish_numbers_addition_result())
