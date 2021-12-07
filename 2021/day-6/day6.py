from typing import List

EXISTING_FISH_REPRODUCTION_DAYS = 6
NEW_FISH_REPRODUCTION_DAYS = EXISTING_FISH_REPRODUCTION_DAYS + 2


def calculate_number_fish_after_n_days(fish_reproduction_days_list: List[int], days: int) -> int:
    # The list stores a count of fish at each index, where each index represents the number of days till reproduction
    # for that group of fish.
    fish_count_list: List[int] = [0 for _ in range(NEW_FISH_REPRODUCTION_DAYS + 1)]

    for reproduction_days in fish_reproduction_days_list:
        fish_count_list[reproduction_days] += 1

    for i in range(days):
        new_fish_count = fish_count_list[0]
        temp1 = fish_count_list[NEW_FISH_REPRODUCTION_DAYS]
        for j in range(len(fish_count_list) - 2, -1, -1):
            temp2 = fish_count_list[j]
            fish_count_list[j] = temp1
            temp1 = temp2

        fish_count_list[EXISTING_FISH_REPRODUCTION_DAYS] += new_fish_count
        fish_count_list[NEW_FISH_REPRODUCTION_DAYS] = new_fish_count

    return sum(fish_count_list)


if __name__ == '__main__':
    d = 256
    input_fish_list = [3, 5, 3, 5, 1, 3, 1, 1, 5, 5, 1, 1, 1, 2, 2, 2, 3, 1, 1, 5, 1, 1, 5, 5, 3, 2, 2, 5, 4, 4, 1, 5,
                       1, 4, 4, 5, 2, 4, 1, 1, 5, 3, 1, 1, 4, 1, 1, 1, 1, 4, 1, 1, 1, 1, 2, 1, 1, 4, 1, 1, 1, 2, 3, 5,
                       5, 1, 1, 3, 1, 4, 1, 3, 4, 5, 1, 4, 5, 1, 1, 4, 1, 3, 1, 5, 1, 2, 1, 1, 2, 1, 4, 1, 1, 1, 4, 4,
                       3, 1, 1, 1, 1, 1, 4, 1, 4, 5, 2, 1, 4, 5, 4, 1, 1, 1, 2, 2, 1, 4, 4, 1, 1, 4, 1, 1, 1, 2, 3, 4,
                       2, 4, 1, 1, 5, 4, 2, 1, 5, 1, 1, 5, 1, 2, 1, 1, 1, 5, 5, 2, 1, 4, 3, 1, 2, 2, 4, 1, 2, 1, 1, 5,
                       1, 3, 2, 4, 3, 1, 4, 3, 1, 2, 1, 1, 1, 1, 1, 4, 3, 3, 1, 3, 1, 1, 5, 1, 1, 1, 1, 3, 3, 1, 3, 5,
                       1, 5, 5, 2, 1, 2, 1, 4, 2, 3, 4, 1, 4, 2, 4, 2, 5, 3, 4, 3, 5, 1, 2, 1, 1, 4, 1, 3, 5, 1, 4, 1,
                       2, 4, 3, 1, 5, 1, 1, 2, 2, 4, 2, 3, 1, 1, 1, 5, 2, 1, 4, 1, 1, 1, 4, 1, 3, 3, 2, 4, 1, 4, 2, 5,
                       1, 5, 2, 1, 4, 1, 3, 1, 2, 5, 5, 4, 1, 2, 3, 3, 2, 2, 1, 3, 3, 1, 4, 4, 1, 1, 4, 1, 1, 5, 1, 2,
                       4, 2, 1, 4, 1, 1, 4, 3, 5, 1, 2, 1
                       ]
    print(
        "Number of fish after {} days is: {}.".format(d, calculate_number_fish_after_n_days(input_fish_list, d)))
