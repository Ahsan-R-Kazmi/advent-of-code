from typing import List, Dict, Tuple


def compute_overlapping_points(consider_diagonals: bool = False):
    print("considering_diagonals:", consider_diagonals)

    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        point_count_dict: Dict[Tuple[int, int], int] = {}
        for line in lines:
            points: List[str] = line.split(" -> ")

            point1: List[str] = points[0].split(",")
            point2: List[str] = points[1].split(",")

            x1 = int(point1[0])
            y1 = int(point1[1])
            x2 = int(point2[0])
            y2 = int(point2[1])

            # Skip if this is not a horizontal or vertical line.
            if x1 == x2 or y1 == y2:
                for x in range(x1, (x2 + 1) if x2 >= x1 else x2 - 1, 1 if x2 >= x1 else -1):
                    for y in range(y1, (y2 + 1) if y2 >= y1 else y2 - 1, 1 if y2 >= y1 else -1):
                        point = (x, y)
                        count = point_count_dict.get(point, 0) + 1
                        point_count_dict[point] = count
            elif consider_diagonals:
                count = point_count_dict.get((x1, y1), 0) + 1
                point_count_dict[(x1, y1)] = count
                count = point_count_dict.get((x2, y2), 0) + 1
                point_count_dict[(x2, y2)] = count
                x, y = x1 + (1 if x2 > x1 else -1), y1 + (1 if y2 > y1 else -1)
                while (x, y) != (x2, y2):
                    count = point_count_dict.get((x, y), 0) + 1
                    point_count_dict[(x, y)] = count
                    x, y = x + (1 if x2 >= x1 else -1), y + (1 if y2 > y1 else -1)

        counts_greater_than_1 = 0
        for _, count in point_count_dict.items():
            if count > 1:
                counts_greater_than_1 += 1

        print("Points where multiple lines overlap:", counts_greater_than_1)


if __name__ == '__main__':
    compute_overlapping_points()
    compute_overlapping_points(consider_diagonals=True)
