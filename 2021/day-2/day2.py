from typing import List


def problem_1():
    print("problem 1")
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.rstrip() for line in lines]

        depth: int = 0
        horizontal_position: int = 0
        for line in lines:
            tokens: List[str] = line.split(" ")
            direction = tokens[0]
            amount = int(tokens[1])

            if direction == "forward":
                horizontal_position += amount
            elif direction == "down":
                depth += amount
            elif direction == "up":
                depth -= amount

        print("horizontal_position: " + str(horizontal_position) + " depth: " + str(depth))
        print("ans: " + str(horizontal_position * depth))


def problem_2():
    print("problem 2")
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.rstrip() for line in lines]

        depth: int = 0
        horizontal_position: int = 0
        aim: int = 0
        for line in lines:
            tokens: List[str] = line.split(" ")
            direction = tokens[0]
            amount = int(tokens[1])

            if direction == "forward":
                horizontal_position += amount
                depth += (aim * amount)
            elif direction == "down":
                aim += amount
            elif direction == "up":
                aim -= amount

        print("horizontal_position: " + str(horizontal_position) + " depth: " + str(depth) + " aim: " + str(aim))
        print("ans: " + str(horizontal_position * depth))


if __name__ == '__main__':
    problem_1()
    problem_2()
