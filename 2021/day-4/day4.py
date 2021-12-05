from typing import List


def check_board_for_bingo(board: List[List[str]]) -> bool:

    # Check if all the values in a row are marked
    for row in range(len(board)):
        x_count = 0
        for col in range(len(board[row])):
            if board[row][col] == 'X':
                x_count += 1
            else:
                break
        if x_count == len(board[row]):
            return True

    # Check if all the values in a columns are marked
    for col in range(len(board[0])):
        x_count = 0
        for row in range(len(board)):
            if board[row][col] == 'X':
                x_count += 1
            else:
                break
        if x_count == len(board):
            return True

    return False


def compute_board_score(number: int, board: List[List[str]]) -> int:
    board_sum = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != 'X':
                board_sum += int(board[row][col])

    return board_sum * number


def create_bingo_boards(lines: List[str]) -> List[List[List[str]]]:
    boards: List[List[List[str]]] = []

    # Start on line 2, since that is the line on which the numbers for the first board start.
    board: List[List[str]] = []
    for i in range(2, len(lines)):
        line = lines[i]
        if line == '':
            boards.append(board)
            board: List[List[str]] = []
            continue

        board.append(line.split())

    if len(board) > 0:
        boards.append(board)

    return boards

def problem_1():
    print("problem 1")
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.rstrip() for line in lines]

        numbers: List[str] = lines[0].split(",")

        boards: List[List[List[str]]] = create_bingo_boards(lines)

        for number in numbers:
            for board in boards:
                for row in board:
                    for i in range(len(row)):
                        if row[i] == number:
                            row[i] = 'X'
                            bingo = check_board_for_bingo(board)
                            if bingo:
                                print("board score:", compute_board_score(int(number), board))
                                return

def problem_2():
    print("problem 2")
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.rstrip() for line in lines]

        numbers: List[str] = lines[0].split(",")

        boards: List[List[List[str]]] = create_bingo_boards(lines)

        for number in numbers:
            for board in boards:
                for row in board:
                    bingo: bool = False
                    for i in range(len(row)):
                        if row[i] == number:
                            row[i] = 'X'
                            bingo = check_board_for_bingo(board)
                            if bingo:
                                if len(boards) == 1:
                                    print("board score:", compute_board_score(int(number), board))
                                break
                    if bingo:
                        new_boards: List[List[List[str]]] = []
                        for other_board in boards:
                            if other_board is board:
                                continue
                            new_boards.append(other_board)
                        boards = new_boards
                        break


if __name__ == '__main__':
    problem_1()
    problem_2()
