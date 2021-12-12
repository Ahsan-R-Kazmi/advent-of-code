import copy
from typing import List, Dict, Set, Tuple


def add_neighbor_to_graph(graph: Dict[str, List[str]], node: str, neighbor: str) -> None:
    neighbors: List[str] = graph.get(node, [])
    neighbors.append(neighbor)

    graph[node] = neighbors


def bfs_1(graph: Dict[str, List[str]]) -> int:
    count = 0
    visited: Set[str] = set()
    visited.add("start")
    q: List[Tuple[str, Set[str], str]] = [("start", visited, "start")]
    while len(q) > 0:

        node, visited, path = q.pop(0)

        if node == "end":
            print(path)
            count += 1
            continue

        neighbors = graph.get(node, [])

        for neighbor in neighbors:
            new_visited = copy.deepcopy(visited)
            if neighbor.islower() and neighbor in visited:
                continue

            new_visited.add(neighbor)
            q.append((neighbor, new_visited, path + "," + neighbor))

    print()
    return count


def bfs_2(graph: Dict[str, List[str]]) -> int:
    count = 0
    one_small_cave_visited_twice: bool = False
    cave_visit_count_dict: Dict[str, int] = {"start": 1}
    q: List[Tuple[str, str, Dict[str, int], bool]] = [("start", "start", cave_visit_count_dict,
                                                       one_small_cave_visited_twice)]
    while len(q) > 0:
        node, path, cave_visit_count_dict, one_small_cave_visited_twice = q.pop(0)

        if node == "end":
            print(path)
            count += 1
            continue

        neighbors = graph.get(node, [])

        for neighbor in neighbors:
            new_cave_visit_count_dict = copy.deepcopy(cave_visit_count_dict)
            if neighbor == "start":
                continue

            if neighbor.islower() and new_cave_visit_count_dict.get(neighbor, 0) >= 1 and one_small_cave_visited_twice:
                continue

            visit_count = new_cave_visit_count_dict.get(neighbor, 0) + 1
            new_cave_visit_count_dict[neighbor] = visit_count

            new_one_small_cave_visited_twice = one_small_cave_visited_twice
            if neighbor.islower() and visit_count == 2:
                new_one_small_cave_visited_twice = True

            q.append((neighbor, path + "," + neighbor, new_cave_visit_count_dict, new_one_small_cave_visited_twice))

    print()
    return count


def find_number_of_paths() -> Tuple[int, int]:
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        graph: Dict[str, List[str]] = {}
        for line in lines:
            nodes = line.split("-")
            add_neighbor_to_graph(graph, nodes[0], nodes[1])
            add_neighbor_to_graph(graph, nodes[1], nodes[0])

    return bfs_1(graph), bfs_2(graph)


if __name__ == '__main__':
    print("(Number of paths that visit small caves at most once, Number of paths that visit one small cave twice and "
          "the rest of the small caves at most once):", find_number_of_paths())
