from statistics import median
from typing import List, Dict, Tuple


def calculate_syntax_error_and_completion_score() -> Tuple[int, int]:
    with open("problem-input.txt") as file:
        lines: List[str] = file.readlines()
        lines: List[str] = [line.strip() for line in lines]

        closing_brace_open_brace_dict: Dict[str, str] = {
            ")": "(",
            "]": "[",
            "}": "{",
            ">": "<"
        }

        open_brace_closing_brace_dict: Dict[str, str] = {
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">"
        }

        closing_brace_error_dict: Dict[str, int] = {
            ")": 3,
            "]": 57,
            "}": 1197,
            ">": 25137
        }

        closing_brace_cost_dict: Dict[str, int] = {
            ")": 1,
            "]": 2,
            "}": 3,
            ">": 4
        }

        error_score = 0
        completion_scores = []
        for line in lines:
            open_brace_stack = []

            corrupted: bool = False
            for c in line:
                if c == "(" or c == "[" or c == "{" or c == "<":
                    open_brace_stack.append(c)
                else:
                    expected_open_brace: str = closing_brace_open_brace_dict.get(c)
                    if len(open_brace_stack) == 0 or (open_brace_stack.pop(-1) != expected_open_brace):
                        error_score += closing_brace_error_dict.get(c)
                        corrupted = True
                        break
            if not corrupted:
                completion_score = 0
                while len(open_brace_stack) > 0:
                    cost = closing_brace_cost_dict.get(open_brace_closing_brace_dict.get(open_brace_stack.pop(-1)))
                    completion_score *= 5
                    completion_score += cost
                completion_scores.append(completion_score)

        completion_scores.sort()
        return error_score, median(completion_scores)


if __name__ == '__main__':
    print("syntax error score, completion score:", calculate_syntax_error_and_completion_score())
