import ast
import unittest
import day18


class TestDay18Methods(unittest.TestCase):
    def test_explode_snailfish_number_1(self):
        input_list = ast.literal_eval("[[[[[9,8],1],2],3],4]")
        day18.explode_snailfish_number(input_list, 1)
        self.assertEqual([[[[0, 9], 2], 3], 4], input_list)

    def test_explode_snailfish_number_2(self):
        input_list = ast.literal_eval("[7,[6,[5,[4,[3,2]]]]]")
        day18.explode_snailfish_number(input_list, 1)
        self.assertEqual([7, [6, [5, [7, 0]]]], input_list)

    def test_explode_snailfish_number_3(self):
        input_list = ast.literal_eval("[[6,[5,[4,[3,2]]]],1]")
        day18.explode_snailfish_number(input_list, 1)
        self.assertEqual([[6, [5, [7, 0]]], 3], input_list)

    def test_explode_snailfish_number_4(self):
        input_list = ast.literal_eval("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
        day18.explode_snailfish_number(input_list, 1)
        self.assertEqual([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]], input_list)

    def test_explode_snailfish_number_5(self):
        input_list = ast.literal_eval("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
        day18.explode_snailfish_number(input_list, 1)
        self.assertEqual([[3, [2, [8, 0]]], [9, [5, [7, 0]]]], input_list)

    def test_split_snailfish_number_1(self):
        input_list = ast.literal_eval("[[[[0,7],4],[15,[0,13]]],[1,1]]")
        day18.split_snailfish_number(input_list)
        self.assertEqual([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]], input_list)

    def test_split_snailfish_number_2(self):
        input_list = ast.literal_eval("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
        day18.split_snailfish_number(input_list)
        self.assertEqual([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]], input_list)

    def test_addition_and_reduction_1(self):
        a = [[[[4, 3], 4], 4], [7, [[8, 4], 9]]]
        b = [1, 1]

        c = day18.add_snailfish_numbers(a, b)
        day18.reduce_snailfish_numbers(c)

        self.assertEqual([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]], c)

    def test_compute_magnitude_1(self):
        self.assertEqual(143, day18.compute_magnitude([[1, 2], [[3, 4], 5]]))

    def test_compute_magnitude_2(self):
        self.assertEqual(3488,
                         day18.compute_magnitude([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]))
