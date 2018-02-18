import unittest

from drawing_program.commands import (
    CreateCanvasCommand, DrawLineCommand, DrawRectangleCommand,
    BucketFillCommand, QuitCommand,
)
from drawing_program.utils import (
    InvalidInputException, UnknownCommandException, UserExitException
)


class TestCreateCanvasCommand(unittest.TestCase):
    def test_valid_input(self):
        state, command_line = None, 'C 20 4'
        command = CreateCanvasCommand(
            state, command_line
        )
        result = command.do()
        self.assertEqual(result, [[' '] * 20] * 4)

    def test_missing_param_input(self):
        state, command_line = None, 'C 20'
        command = CreateCanvasCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_more_param_input(self):
        state, command_line = None, 'C 20 3 4'
        command = CreateCanvasCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_invalid_param_input(self):
        state, command_line = None, 'C 20 abcd'
        command = CreateCanvasCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_invalid_logic_input(self):
        state, command_line = None, 'C 20 -1'
        command = CreateCanvasCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()


class TestDrawLineCommand(unittest.TestCase):
    def test_valid_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'L 1 2 6 2'
        command = DrawLineCommand(
            state, command_line
        )
        result = command.do()
        expected = state
        for idx in range(0, 6):
            expected[1][idx] = 'x'
        self.assertEqual(result, expected)

    def test_missing_param_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'L 1 2 6'
        command = DrawLineCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_more_param_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'L 1 2 6 2 3'
        command = DrawLineCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_invalid_param_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'L 1 2 6 abcd'
        command = DrawLineCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_invalid_logic_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'L 1 2 6 3'
        command = DrawLineCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()


class TestDrawRectangleCommand(unittest.TestCase):
    def test_valid_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'R 14 1 18 3'
        command = DrawRectangleCommand(
            state, command_line
        )
        result = command.do()
        expected = state
        for idx in range(13, 18):
            expected[0][idx] = 'x'
        for idx in range(13, 18):
            expected[2][idx] = 'x'
        expected[1][13] = 'x'
        expected[1][17] = 'x'
        self.assertEqual(result, expected)

    def test_missing_param_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'R 14 1 18'
        command = DrawRectangleCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_more_param_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'R 14 1 18 3 4'
        command = DrawRectangleCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_invalid_param_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'R 14 1 18 abcd'
        command = DrawRectangleCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_invalid_logic_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'R 14 1 18 25'
        command = DrawRectangleCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()


class BucketFillCommandCommand(unittest.TestCase):
    def test_valid_input(self):
        state = [[' '] * 20 for _ in range(4)]
        for idx in range(13, 18):
            state[0][idx] = 'x'
        for idx in range(13, 18):
            state[2][idx] = 'x'
        state[1][13] = 'x'
        state[1][17] = 'x'
        command_line = 'B 10 3 o'
        command = BucketFillCommand(
            state, command_line
        )
        result = command.do()
        expected = [['o'] * 20 for _ in range(4)]
        for idx in range(13, 18):
            expected[0][idx] = 'x'
        for idx in range(13, 18):
            expected[2][idx] = 'x'
        expected[1][13] = 'x'
        expected[1][17] = 'x'
        expected[1][14] = ' '
        expected[1][15] = ' '
        expected[1][16] = ' '
        self.assertEqual(result, expected)

    def test_missing_param_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'B 10 3'
        command = BucketFillCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_more_param_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'B 10 3 o b'
        command = BucketFillCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_invalid_param_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'B 10 3 obd'
        command = BucketFillCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()

    def test_invalid_logic_input(self):
        state = [[' '] * 20 for _ in range(4)]
        command_line = 'B 10 18 obd'
        command = BucketFillCommand(
            state, command_line
        )
        with self.assertRaises(InvalidInputException):
            command.do()
