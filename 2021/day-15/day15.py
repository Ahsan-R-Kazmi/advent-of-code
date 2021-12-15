import copy
import heapq
from typing import Tuple, List, Set, Dict

DIRECTIONS = [[1, 0], [-1, 0], [0, 1], [0, -1]]


def dijkstra_shortest_path_algorthm(grid: List[List[int]]) -> float:
    q: List[Tuple[float, int, int]] = [(0, 0, 0)]
    distances = [[float("inf") for _ in range(len(grid[i]))] for i in range(len(grid))]
    distances[0][0] = 0
    while len(q) > 0:

        distance, i, j = heapq.heappop(q)

        if i == len(grid) - 1 and j == len(grid[len(grid) - 1]) - 1:
            return distance

        for direction in DIRECTIONS:
            new_i = i + direction[0]
            new_j = j + direction[1]

            if new_i < 0 or new_i >= len(grid) or new_j < 0 or new_j >= len(grid[0]):
                continue

            if distances[new_i][new_j] > distance + grid[new_i][new_j]:
                distances[new_i][new_j] = distance + grid[new_i][new_j]
                heapq.heappush(q, (distances[new_i][new_j], new_i, new_j))

    return distances[len(grid) - 1][len(grid[len(grid) - 1]) - 1]


def find_least_risk_path_score() -> Tuple[float, float]:
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        grid: List[List[int]] = []

        for line in lines:
            r: List[int] = []
            for i in range(len(line)):
                r.append(int(line[i]))
            grid.append(r)

        expanded_grid: List[List[int]] = [[0 for _ in range(len(grid[0]) * 5)] for i in range(len(grid) * 5)]

        for i in range(len(expanded_grid)):
            for j in range(len(expanded_grid[i])):

                row = i
                col = j
                row_diff = 0
                col_diff = 0

                while row > 0:
                    row -= len(grid)
                    if row < 0:
                        row += len(grid)
                        break
                    row_diff += 1
                while col > 0:
                    col -= len(grid[0])
                    if col < 0:
                        col += len(grid[0])
                        break
                    col_diff += 1

                expanded_grid[i][j] = (grid[row][col] + row_diff + col_diff - 1) % 9 + 1

        return dijkstra_shortest_path_algorthm(grid), dijkstra_shortest_path_algorthm(expanded_grid)


if __name__ == '__main__':
    print("Least risk score (normal grid), Least risk score (expanded grid):", find_least_risk_path_score())

