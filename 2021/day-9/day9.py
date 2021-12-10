from typing import List, Dict

DIRECTIONS = [[1, 0], [-1, 0], [0, 1], [0, -1]]


def calculate_low_point_risk_level_sum() -> int:
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        grid: List[List[int]] = []

        for line in lines:
            row: List[int] = []
            for i in range(len(line)):
                row.append(int(line[i]))
            grid.append(row)

        risk_level_sum = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                less_than_adjacent_values = True
                for direction in DIRECTIONS:
                    new_i = i + direction[0]
                    new_j = j + direction[1]
                    if new_i < 0 or new_i >= len(grid) or new_j < 0 or new_j >= len(grid[i]):
                        continue
                    if grid[i][j] >= grid[new_i][new_j]:
                        less_than_adjacent_values = False
                        break

                if less_than_adjacent_values:
                    risk_level_sum += (1 + grid[i][j])
    return risk_level_sum


def dfs(i: int, j: int, grid: List[List[int]], connected_component_size: int) -> int:
    # If this is out of bounds, already visited (-1), or can not be visited because it is a border (9) return.
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[0]) or grid[i][j] == -1 or grid[i][j] == 9:
        return 0

    # Visit the location
    grid[i][j] = -1

    for direction in DIRECTIONS:
        connected_component_size += dfs(i + direction[0], j + direction[1], grid, 0)

    return connected_component_size + 1


def calculate_product_of_three_largest_basin_sizes() -> int:
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

    grid: List[List[int]] = []

    for line in lines:
        row: List[int] = []
        for i in range(len(line)):
            row.append(int(line[i]))
        grid.append(row)

    basin_sizes: List[int] = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == -1 or grid[i][j] == 9:
                continue
            basin_sizes.append(dfs(i, j, grid, connected_component_size=0))

    List.sort(basin_sizes, reverse=True)

    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


if __name__ == '__main__':
    print("low point risk level:", calculate_low_point_risk_level_sum())
    print("product of three largest basin sizes:", calculate_product_of_three_largest_basin_sizes())
