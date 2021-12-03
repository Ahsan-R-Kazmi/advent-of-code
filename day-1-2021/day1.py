from typing import List


def problem_1():
    with open("./problem-1-input.txt") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

        increased_count = 0
        for i in range(1, len(lines)):
            if int(lines[i]) > int(lines[i - 1]):
                increased_count += 1

        print(increased_count)


def problem_2():
    n = 3
    with open("./problem-1-input.txt") as file:
        lines = file.readlines()
        lines: List[str] = [line.rstrip() for line in lines]

        n = 3
        window: List[int] = []

        for i in range(0, n):
            window.append(int(lines[i]))

        previous_sum = sum(window)

        increased_count = 0
        for line in lines:
            window.append(int(line))
            window.pop(0)

            window_sum = sum(window)
            if window_sum > previous_sum:
                increased_count += 1

            previous_sum = window_sum
        print(increased_count)


if __name__ == '__main__':
    problem_1()
    problem_2()
