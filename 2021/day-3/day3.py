from typing import List


def problem_1():
    print("problem 1")
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.rstrip() for line in lines]

        length = len(lines[0])

        ones_count_list = [0 for i in range(length)]
        zeros_count_list = [0 for i in range(length)]

        for line in lines:
            for i in range(len(line)):
                if line[i] == "1":
                    ones_count_list[i] += 1
                else:
                    zeros_count_list[i] += 1

        gamma = ""
        epsilon = ""

        for i in range(length):
            if ones_count_list[i] >= zeros_count_list[i]:
                gamma += "1"
                epsilon += "0"
            else:
                gamma += "0"
                epsilon += "1"

        gamma = int(gamma, 2)
        epsilon = int(epsilon, 2)

        print("gamma: " + str(gamma) + " epsilon: " + str(epsilon) + " power consumption: " + str(gamma * epsilon))


def filter_input(use_most_frequent_bit: bool = True) -> List[str]:
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.rstrip() for line in lines]
        binary_number_length: int = len(lines[0])
        i: int = 0
        while len(lines) > 1 and i < binary_number_length:
            ones_count: int = 0
            zeros_count: int = 0
            for line in lines:
                if line[i] == "1":
                    ones_count += 1
                else:
                    zeros_count += 1

            new_lines: List[str] = []
            filter_bit = ""
            if use_most_frequent_bit:
                filter_bit = "1" if ones_count >= zeros_count else "0"
            else:
                filter_bit = "0" if ones_count >= zeros_count else "1"
            for line in lines:
                if line[i] == filter_bit:
                    new_lines.append(line)
            i += 1
            lines = new_lines

        return lines


def problem_2():
    print("problem 2")
    oxygen_generator_rating = filter_input(True)
    print("oxygen_generator_rating list: ")
    print(oxygen_generator_rating)

    co2_scrubber_rating = filter_input(False)
    print("co2_scrubber_rating  list: ")
    print(co2_scrubber_rating)
    life_support_rating: int = int(oxygen_generator_rating[0], 2) * int(co2_scrubber_rating[0], 2)
    print("life_support_rating: " + str(life_support_rating))


if __name__ == '__main__':
    problem_1()
    problem_2()
