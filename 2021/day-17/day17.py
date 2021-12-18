from typing import Optional, Tuple


def highest_y_position_for_velocity(v_x: int, v_y: int, x1: int, x2: int, y1: int, y2: int) -> Optional[int]:
    max_y = 0
    x = 0
    y = 0
    target_reached = False
    while True:
        if (x1 <= x <= x2) and (y1 <= y <= y2):
            target_reached = True
        d1_x = abs(x - x2)
        x += v_x
        d2_x = abs(x - x2)
        if not (x1 <= x <= x2) and d2_x >= d1_x:
            break

        y += v_y
        if y < y1 and v_y < 0:
            break

        if v_x > 0:
            v_x -= 1
        elif v_x < 0:
            v_x += 1

        v_y -= 1
        max_y = max(max_y, y)

    return None if not target_reached else max_y


def find_highest_position(x1: int, x2: int, y1: int, y2: int) -> Tuple[int, int, int, int]:
    highest_position = 0
    corresponding_v_x = 0
    corresponding_v_y = 0
    velocity_counter = 0
    for v_x in range(-500, 500):
        for v_y in range(-500, 500):
            y_position = highest_y_position_for_velocity(v_x, v_y, x1, x2, y1, y2)
            if y_position is None:
                continue
            velocity_counter += 1
            if y_position >= highest_position:
                highest_position = y_position
                corresponding_v_x = v_x
                corresponding_v_y = v_y

    return corresponding_v_x, corresponding_v_y, highest_position, velocity_counter


if __name__ == '__main__':
    print("v_x,v_y, highest position, velocity_counter", find_highest_position(265, 287, -103, -58))
