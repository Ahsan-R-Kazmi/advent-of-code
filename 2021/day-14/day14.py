import copy
from typing import Tuple, List, Set, Dict


def calculate_difference_of_most_and_least_frequent_elements_in_polymer(steps: int) -> int:
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        first_break_encountered: bool = False
        template = ""
        pair_insertion_dict: Dict[str, str] = {}
        for line in lines:
            if line == "":
                first_break_encountered = True
                continue

            if not first_break_encountered:
                template = line
            else:
                pair_insertion_dict[line.split(" -> ")[0]] = line.split(" -> ")[1]

        pair_count_dict: Dict[str, int] = {}
        element_count_dict: Dict[str, int] = {}
        for i in range(len(template) - 1):
            pair = template[i:i+2]
            pair_count_dict[pair] = pair_count_dict.get(pair, 0) + 1
            element_count_dict[template[i]] = element_count_dict.get(template[i], 0) + 1

        element_count_dict[template[-1]] = element_count_dict.get(template[-1], 0) + 1

        for step in range(steps):
            new_pair_count_dict: Dict[str, int] = {}
            for pair, count in pair_count_dict.items():
                new_element = pair_insertion_dict.get(pair)
                new_pair_1 = pair[0:1] + new_element
                new_pair_2 = new_element + pair[1:]

                element_count_dict[new_element] = element_count_dict.get(new_element, 0) + count

                new_pair_count_dict[new_pair_1] = new_pair_count_dict.get(new_pair_1, 0) + count
                new_pair_count_dict[new_pair_2] = new_pair_count_dict.get(new_pair_2, 0) + count

            pair_count_dict = new_pair_count_dict

        most_frequent_element_count = 0
        least_frequent_element_count = float("inf")

        for element, count in element_count_dict.items():
            most_frequent_element_count = max(count, most_frequent_element_count)
            least_frequent_element_count = min(count, least_frequent_element_count)

    return most_frequent_element_count - least_frequent_element_count


if __name__ == '__main__':
    n = 10
    print(str.format("Count of most common element subtracted by count of least common element after n = {} steps: {}",
                     n, calculate_difference_of_most_and_least_frequent_elements_in_polymer(n)))

    n = 40
    print(str.format("Count of most common element subtracted by count of least common element after n = {} steps: {}",
                     n, calculate_difference_of_most_and_least_frequent_elements_in_polymer(n)))

