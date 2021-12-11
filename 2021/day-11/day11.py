from typing import List, Set, Tuple

DIRECTIONS = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]


def increment_grid_by_one(grid: List[List[int]]):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] += 1


def bfs(i: int, j: int, grid: List[List[int]], visited: Set[Tuple[int, int]]):
    q = []
    visited.add((i, j))
    q.append((i, j))

    while len(q) > 0:
        i, j = q.pop(0)
        for direction in DIRECTIONS:
            new_i = i + direction[0]
            new_j = j + direction[1]
            if 0 <= new_i < len(grid) and 0 <= new_j < len(grid[0]) and (new_i, new_j) not in visited:
                grid[new_i][new_j] += 1
                if grid[new_i][new_j] > 9:
                    visited.add((new_i, new_j))
                    q.append((new_i, new_j))


def print_grid(grid: List[List[int]]):
    for i in range(len(grid)):
        print(grid[i])


def count_flashes_after_n_steps(steps: int) -> int:
    flashes = 0

    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        grid: List[List[int]] = []

        for line in lines:
            row: List[int] = []
            for i in range(len(line)):
                row.append(int(line[i]))
            grid.append(row)

        for step in range(steps):
            increment_grid_by_one(grid)
            visited: Set[Tuple[int, int]] = set()
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] > 9 and (i, j) not in visited:
                        bfs(i, j, grid, visited)

            step_flash_count = 0
            for i in range(len(grid)):
                for j in range(len(grid[i])):

                    if grid[i][j] > 9:
                        step_flash_count += 1
                        flashes += 1
                        grid[i][j] = 0
            if step_flash_count == len(grid) * len(grid[0]):
                print(str.format("All octopuses flashed at step: {}", step + 1))

    return flashes


if __name__ == '__main__':

    n = 1000
    print(str.format("Flashes after n = {} steps: {}", n, count_flashes_after_n_steps(n)))
