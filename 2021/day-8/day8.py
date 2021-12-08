from typing import List, Dict, FrozenSet

SEGMENT_COUNT_DIGIT_LIST_DICT: Dict[int, List[int]] = {
    2: [1],
    4: [4],
    3: [7],
    5: [2, 3, 5],
    6: [0, 6, 9],
    7: [8]
}


def count_unique_segment_count_digits() -> int:

    unique_digit_count_digits = 0
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        for line in lines:
            output_value = line.split("|")[1].strip()
            digits = output_value.split(" ")

            for digit in digits:
                segment_count = len(digit)
                digit_list = SEGMENT_COUNT_DIGIT_LIST_DICT.get(segment_count)
                if len(digit_list) == 1:
                    unique_digit_count_digits += 1

    return unique_digit_count_digits


def sum_output_values() -> int:
    output_value_sum = 0
    segment_set_digit_dict: Dict[FrozenSet[str], int] = {}
    digit_segment_set_dict: Dict[int, FrozenSet[str]] = {}

    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        for line in lines:
            unique_signal_patterns: List[str] = line.split("|")[0].strip().split(" ")
            output_signal_patterns: List[str] = line.split("|")[1].strip().split(" ")

            for digit in unique_signal_patterns:
                segment_count = len(digit)
                digit_list = SEGMENT_COUNT_DIGIT_LIST_DICT.get(segment_count)
                if len(digit_list) == 1:
                    segment_set = construct_segment_set(digit)

                    segment_set_digit_dict[segment_set] = digit_list[0]
                    digit_segment_set_dict[digit_list[0]] = segment_set

            for digit in unique_signal_patterns:
                segment_count = len(digit)
                digit_list = SEGMENT_COUNT_DIGIT_LIST_DICT.get(segment_count)
                if len(digit_list) == 1:
                    continue

                segment_set = construct_segment_set(digit)

                if segment_count == 5:
                    # If there are 5 segments, this either a 2, 3, or 5.
                    # If this digit contains 2 segments from a 4, then it is a 2.
                    # Otherwise, if it contains 3 segments from a 7, then it is a 3.
                    # Otherwise, it is a 5.
                    four_segment_set = digit_segment_set_dict.get(4)
                    found_count = calculate_found_count(digit, four_segment_set)
                    if found_count == 2:
                        segment_set_digit_dict[segment_set] = 2
                    else:
                        seven_segment_set = digit_segment_set_dict.get(7)
                        found_count = calculate_found_count(digit, seven_segment_set)
                        if found_count == 3:
                            segment_set_digit_dict[segment_set] = 3
                        else:
                            segment_set_digit_dict[segment_set] = 5

                elif segment_count == 6:
                    # If there are 6 segments, this is either a 0, 6, or 9
                    # If this digit contains all 4 segments from a 4, then is a 9.
                    # Otherwise, it contains both segments from a 1, then it is a 0.
                    # Otherwise, this a 6.
                    four_segment_set = digit_segment_set_dict.get(4)
                    found_count = calculate_found_count(digit, four_segment_set)

                    if found_count == len(four_segment_set):
                        segment_set_digit_dict[segment_set] = 9
                    else:

                        one_segment_set = digit_segment_set_dict.get(1)
                        found_count = calculate_found_count(digit, one_segment_set)

                        if found_count == len(one_segment_set):
                            segment_set_digit_dict[segment_set] = 0
                        else:
                            segment_set_digit_dict[segment_set] = 6

            number_str: str = ""
            for digit in output_signal_patterns:
                segment_set = construct_segment_set(digit)
                number_str += str(segment_set_digit_dict.get(segment_set))

            number: int = int(number_str)
            output_value_sum += number

    return output_value_sum


def construct_segment_set(digit: str) -> FrozenSet[str]:
    letter_list = []
    for letter in digit:
        letter_list.append(letter)
    return frozenset(letter_list)


def calculate_found_count(digit: str, segment_set: FrozenSet[str]) -> int:
    found_count = 0
    for letter in digit:
        if letter in segment_set:
            found_count += 1

    return found_count


if __name__ == '__main__':
    print("Unique segment count digits:", count_unique_segment_count_digits())
    print("Output value sum:", sum_output_values())
