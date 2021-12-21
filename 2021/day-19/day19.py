import ast
import copy
import math
from typing import Tuple, List, Set, Dict
import numpy as np

MINIMUM_MATCH_COUNT = 11
DIFFERENCE_THRESHOLD = 0.001


# This function will return a Tuple with the first element in the tuple, the manhattan distance, and the subsequent
# elements a set of with the values: abs(x2 - x1), abs(y2 - y1), abs(z2-z1)
def calculate_manhattan_distance(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> Tuple[int, Set[int]]:
    component_set: Set[int] = set()
    component_set.add(abs(x2 - x1))
    component_set.add(abs(y2 - y1))
    component_set.add(abs(z2 - z1))
    return abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1), component_set


# This function takes a point list and calculates the distances from the reference point to all the other points.
def create_distance_list(point_list: List[Tuple[int, int, int]], reference_point: Tuple[int, int, int]) \
        -> List[Tuple[int, Set[int], Tuple[int, int, int]]]:
    distance_list: List[Tuple[int, Set[int], Tuple[int, int, int]]] = []

    for i in range(len(point_list)):
        if point_list[i] == reference_point:
            continue
        x1 = reference_point[0]
        y1 = reference_point[1]
        z1 = reference_point[2]

        x2 = point_list[i][0]
        y2 = point_list[i][1]
        z2 = point_list[i][2]

        distance_list.append((calculate_manhattan_distance(x1, y1, z1, x2, y2, z2)[0],
                              calculate_manhattan_distance(x1, y1, z1, x2, y2, z2)[1],
                              point_list[i]))

    return distance_list


def do_unresolved_points_remain(scanner_points_dict: Dict[str, List[Tuple[int, int, int]]]) -> bool:
    for scanner, points in scanner_points_dict.items():
        if scanner == "scanner 0":
            continue
        if len(points) > 0:
            return True

    return False


# A distance match is recorded if the manhattan distance as well as the unordered set of the components of the
# manhattan distances match. (There is still a chance that two points have the same manhattan distance and component
# parts. However, for this problem we assume that error negligible).
def count_distance_matches(dist_list_1: List[Tuple[int, Set[int], Tuple[int, int, int]]],
                           dist_list_2: List[Tuple[int, Set[int], Tuple[int, int, int]]]) -> int:
    matches = 0
    for dist1 in dist_list_1:
        for dist2 in dist_list_2:
            if dist2[0] == dist1[0] and dist1[1] == dist2[1]:
                matches += 1

    return matches


def create_matching_points_lists(dist_list_1: List[Tuple[int, Set[int], Tuple[int, int, int]]],
                                 dist_list_2: List[Tuple[int, Set[int], Tuple[int, int, int]]]) \
        -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
    scanner_a_matching_points: List[Tuple[int, int, int]] = []
    scanner_b_matching_points: List[Tuple[int, int, int]] = []
    for i in range(len(dist_list_1)):
        for j in range(len(dist_list_2)):
            if dist_list_1[i][0] == dist_list_2[j][0] and dist_list_1[i][1] == dist_list_2[j][1]:
                scanner_a_matching_points.append(dist_list_1[i][2])
                scanner_b_matching_points.append(dist_list_2[j][2])

    return scanner_a_matching_points, scanner_b_matching_points


def determine_potential_scanner_locations(reference_point: Tuple[int, int, int], matched_point: Tuple[int, int, int]) \
        -> Set[Tuple[int, int, int, int, int, int]]:
    potential_scanner_locations: Set[Tuple[int, int, int, int, int, int]] = set()

    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            for k in range(3):
                if k == i or k == j:
                    continue
                potential_scanner_locations.add((reference_point[0] - matched_point[i],
                                                 reference_point[1] - matched_point[j],
                                                 reference_point[2] - matched_point[k], i, j, k))
                potential_scanner_locations.add((reference_point[0] + matched_point[i],
                                                 reference_point[1] + matched_point[j],
                                                 reference_point[2] + matched_point[k], i, j, k))
                potential_scanner_locations.add((reference_point[0] + matched_point[i],
                                                 reference_point[1] + matched_point[j],
                                                 reference_point[2] - matched_point[k], i, j, k))
                potential_scanner_locations.add((reference_point[0] + matched_point[i],
                                                 reference_point[1] - matched_point[j],
                                                 reference_point[2] - matched_point[k], i, j, k))
                potential_scanner_locations.add((reference_point[0] - matched_point[i],
                                                 reference_point[1] + matched_point[j],
                                                 reference_point[2] - matched_point[k], i, j, k))
                potential_scanner_locations.add((reference_point[0] - matched_point[i],
                                                 reference_point[1] + matched_point[j],
                                                 reference_point[2] + matched_point[k], i, j, k))
                potential_scanner_locations.add((reference_point[0] + matched_point[i],
                                                 reference_point[1] - matched_point[j],
                                                 reference_point[2] + matched_point[k], i, j, k))
                potential_scanner_locations.add((reference_point[0] - matched_point[i],
                                                 reference_point[1] - matched_point[j],
                                                 reference_point[2] + matched_point[k], i, j, k))

    return potential_scanner_locations


def translate_points(this_scanner_matching_points: List[Tuple[int, int, int]],
                     scanner_position_and_axes: Tuple[int, int, int, int, int, int],
                     sign1: str, sign2: str, sign3: str, final_sign1: str, final_sign2: str, final_sign3: str) \
        -> List[Tuple[int, int, int]]:
    scanner_points = np.copy(this_scanner_matching_points)
    scanner_position = np.asarray((scanner_position_and_axes[0], scanner_position_and_axes[1],
                                   scanner_position_and_axes[2]))

    x = scanner_position_and_axes[3]
    y = scanner_position_and_axes[4]
    z = scanner_position_and_axes[5]
    a = (scanner_points[:, x]).reshape(scanner_points.shape[0], 1)
    b = (scanner_points[:, y]).reshape(scanner_points.shape[0], 1)
    c = (scanner_points[:, z]).reshape(scanner_points.shape[0], 1)

    scanner_points = np.hstack((a, b, c))

    if sign1 == "-":
        scanner_position[0] *= -1
    if sign2 == "-":
        scanner_position[1] *= -1
    if sign3 == "-":
        scanner_position[2] *= -1

    scanner_points += scanner_position

    if final_sign1 == '-':
        scanner_points[:, 0] *= -1
    if final_sign2 == '-':
        scanner_points[:, 1] *= -1
    if final_sign3 == '-':
        scanner_points[:, 2] *= -1

    a = list(map(tuple, scanner_points))
    return a


def resolve_scanner_location_and_orientation(potential_scanner_locations: Set[Tuple[int, int, int, int, int, int]],
                                             scanner_0_matching_points: List[Tuple[int, int, int]],
                                             this_scanner_matching_points: List[Tuple[int, int, int]]) \
        -> Tuple[Tuple[int, int, int, int, int, int], str, str, str, str, str, str]:
    scanner_0_matching_points = np.asarray(scanner_0_matching_points)
    this_scanner_matching_points = np.asarray(this_scanner_matching_points)

    operation_signs = ["-", "+"]
    final_signs = ["-", "+"]
    sign1: str
    sign2: str
    sign3: str
    final_sign1: str
    final_sign2: str
    final_sign3: str
    for point_and_axes in potential_scanner_locations:
        for i in range(len(operation_signs)):
            for j in range(len(operation_signs)):
                for k in range(len(operation_signs)):
                    for m in range(len(final_signs)):
                        for n in range(len(final_signs)):
                            for o in range(len(final_signs)):

                                sign1 = operation_signs[i]
                                sign2 = operation_signs[j]
                                sign3 = operation_signs[k]
                                final_sign1 = final_signs[m]
                                final_sign2 = final_signs[n]
                                final_sign3 = final_signs[o]

                                scanner_points = translate_points(this_scanner_matching_points, point_and_axes, sign1,
                                                                  sign2, sign3, final_sign1, final_sign2,
                                                                  final_sign3)

                                scanner_points = np.asarray(scanner_points)

                                if np.array_equal(scanner_0_matching_points, scanner_points):
                                    return point_and_axes, sign1, sign2, sign3, final_sign1, final_sign2, final_sign3

    raise ValueError("The scanner location and orientation could not be resolved.")


def resolve_points(scanner_points_dict: Dict[str, List[Tuple[int, int, int]]]) -> Set[Tuple[int, int, int]]:
    resolved_beacons_set: Set[Tuple[int, int, int]] = set()
    resolved_beacons_set.update(set(scanner_points_dict.get("scanner 0")))
    points_used_for_distance_comparison: Set[Tuple[int, int, int]] = set()

    counter = 0
    for point in scanner_points_dict.get("scanner 0"):
        resolved_beacons_set.add(point)

    while do_unresolved_points_remain(scanner_points_dict):
        scanner_0_points = scanner_points_dict.get("scanner 0")
        counter += 1
        print(counter)
        for reference_point in scanner_0_points:
            dist_list_1 = create_distance_list(scanner_0_points, reference_point)

            for scanner, points in scanner_points_dict.items():
                if scanner == "scanner 0":
                    continue

                match_found = False
                for point in points:
                    dist_list_2 = create_distance_list(points, point)
                    matches = count_distance_matches(dist_list_1, dist_list_2)
                    if matches >= MINIMUM_MATCH_COUNT:
                        # Resolve the current points using the reference point.
                        # First create two matrices containing the matching points from the perspective of each scanner.
                        scanner_0_matching_points, other_scanner_matching_points \
                            = create_matching_points_lists(dist_list_1, dist_list_2)

                        scanner_0_matching_points.append(reference_point)
                        other_scanner_matching_points.append(point)

                        # Determine the position and orientation for the other scanner, then
                        potential_scanner_locations = determine_potential_scanner_locations(reference_point, point)
                        other_scanner_position, sign1, sign2, sign3, final_sign1, final_sign2, final_sign3 = \
                            resolve_scanner_location_and_orientation(potential_scanner_locations,
                                                                     scanner_0_matching_points,
                                                                     other_scanner_matching_points)

                        if other_scanner_position is None:
                            continue

                        # Add these resolved points into scanner 0's list and create a new dictionary removing the entry
                        # for the scanner whose points were just resolved.
                        other_scanner_points_set = set(points)
                        other_scanner_matching_points = set(other_scanner_matching_points)

                        other_scanner_points_set -= other_scanner_matching_points

                        other_scanner_points_set = set(translate_points(np.asarray(list(other_scanner_points_set)),
                                                                        other_scanner_position,
                                                                        sign1, sign2, sign3, final_sign1, final_sign2,
                                                                        final_sign3))
                        print(scanner + ": " + str(other_scanner_position))
                        new_scanner_points_dict: Dict[str, List[Tuple[int, int, int]]] = \
                            copy.deepcopy(scanner_points_dict)
                        new_scanner_points_dict.pop(scanner)

                        scanner_0_points = new_scanner_points_dict.get("scanner 0")
                        scanner_0_points.extend(other_scanner_points_set)
                        resolved_beacons_set.update(other_scanner_points_set)

                        scanner_points_dict = new_scanner_points_dict

                        match_found = True
                        break
                if match_found:
                    break

    return resolved_beacons_set


def count_beacons() -> int:
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]
        scanner_points_dict: Dict[str, List[Tuple[int, int, int]]] = {}

        for line in lines:

            if line == "":
                continue
            if line.startswith("---"):
                name = line.split("---")[1].strip()
                continue

            line = line.split(",")
            point_list: List[Tuple[int, int, int]] = scanner_points_dict.get(name, [])
            point_list.append((int(line[0]), int(line[1]), int(line[2])))
            scanner_points_dict[name] = point_list

            a = 1
    resolved_beacons_set = resolve_points(scanner_points_dict)
    return len(resolved_beacons_set)


def get_max_manhattan_distance() -> int:
    scanner_locations: List[Tuple[int, int, int]] = []
    scanner_locations.append((0, 0, 0))
    max_dist = 0
    with open("scanner-locations.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        for line in lines:
            location_and_axes: Tuple[int, int, int] = ast.literal_eval(line.split(":")[1].strip())
            scanner_locations.append((location_and_axes[0], location_and_axes[1], location_and_axes[2]))

        for i in range(len(scanner_locations)):
            for j in range(len(scanner_locations)):
                dist = calculate_manhattan_distance(scanner_locations[i][0],
                                                    scanner_locations[i][1],
                                                    scanner_locations[i][2],
                                                    scanner_locations[j][0],
                                                    scanner_locations[j][1],
                                                    scanner_locations[j][2])[0]
                max_dist = max(max_dist, dist)

    return max_dist


if __name__ == '__main__':
    print(count_beacons())
    print(get_max_manhattan_distance())
