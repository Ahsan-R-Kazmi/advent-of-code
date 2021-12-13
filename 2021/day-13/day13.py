import copy
from typing import Tuple, List, Set, Dict


def reflect_about_y(point: Tuple[int, int], y: int) -> Tuple[int, int]:
    if point[1] <= y:
        return point
    return point[0], y - abs(point[1] - y)


def reflect_about_x(point: Tuple[int, int], x: int) -> Tuple[int, int]:
    if point[0] <= x:
        return point
    return x - abs(point[0] - x), point[1]


def print_point_count_dict(point_count_dict: Dict[Tuple[int, int], int]) -> None:
    max_x = 0
    max_y = 0
    for point, count in point_count_dict.items():
        max_x = max(point[0], max_x)
        max_y = max(point[1], max_y)

    graph: List[List[str]] = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for point, count in point_count_dict.items():
        graph[point[1]][point[0]] = "#"

    for i in range(len(graph)):
        line = ""
        for j in range(len(graph[i])):
            line += graph[i][j]

        print(line)
    print()


def count_dot_after_folds(folds: int) -> int:
    point_count = 0
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        point_count_dict: Dict[Tuple[int, int], int] = {}
        first_break_encountered = False
        fold_instructions: List[str] = []
        for line in lines:
            if line == "":
                first_break_encountered = True
                continue
            if not first_break_encountered:
                coordinates: List[str] = line.split(",")
                point = (int(coordinates[0]), int(coordinates[1]))
                point_count_dict[point] = point_count_dict.get(point, 0) + 1
            else:
                fold_instructions.append(line)

        for i in range(folds):
            print_point_count_dict(point_count_dict)
            axis = fold_instructions[i].split("=")[0]
            value = int(fold_instructions[i].split("=")[1])
            new_point_count_dict = copy.deepcopy(point_count_dict)
            for point, count in point_count_dict.items():
                new_point_count_dict[point] = 0
                if new_point_count_dict.get(point) <= 0:
                    new_point_count_dict.pop(point)

                if axis[-1] == 'x':
                    new_point = reflect_about_x(point, value)
                else:
                    new_point = reflect_about_y(point, value)

                new_point_count_dict[new_point] = new_point_count_dict.get(new_point, 0) + count

            point_count_dict = new_point_count_dict

        print_point_count_dict(point_count_dict)
        for point, count in point_count_dict.items():
            if count > 0:
                point_count += 1

    return point_count


if __name__ == '__main__':
    print("Dots after fist fold:", count_dot_after_folds(1))
    print("Dots after all folds:", count_dot_after_folds(12))
