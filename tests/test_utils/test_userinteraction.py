"""
Created on 23.01.2016

@author: Philip Schoemig
"""

import unittest
from unittest.mock import call, patch

from savegamebackup.utils import userinteraction


class TestUserInteraction(unittest.TestCase):
    input_helper = None

    def setUp(self):
        self.input_helper = userinteraction.InputHelper()

    def tearDown(self):
        pass

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_choice(self, input_mock, print_mock):
        expected = 'y'
        expected_input_calls = [
            call('Test [Y/n] '),
        ]
        expected_print_calls = [
        ]

        input_mock.side_effect = ['y']

        value = self.input_helper.choice(
            'Test', ['y', 'n'], 'y')
        self.assertEqual(expected, value)
        self.assertEqual(expected_input_calls, input_mock.mock_calls)
        self.assertEqual(expected_print_calls, print_mock.mock_calls)

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_choice_with_default_input(self, input_mock, print_mock):
        expected = 'y'
        expected_input_calls = [
            call('Test [Y/n] '),
        ]
        expected_print_calls = [
        ]

        input_mock.side_effect = ['']

        value = self.input_helper.choice(
            'Test', ['y', 'n'], 'y')
        self.assertEqual(expected, value)
        self.assertEqual(expected_input_calls, input_mock.mock_calls)
        self.assertEqual(expected_print_calls, print_mock.mock_calls)

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_choice_with_default_missing(self, input_mock, print_mock):
        expected = 'y'
        expected_input_calls = [
            call('Test [y/n] '),
            call('Test [y/n] '),
        ]
        expected_print_calls = [
            call('Please enter a valid option.'),
        ]

        input_mock.side_effect = ['', 'y']

        value = self.input_helper.choice(
            'Test', ['y', 'n'])
        self.assertEqual(expected, value)
        self.assertEqual(expected_input_calls, input_mock.mock_calls)
        self.assertEqual(expected_print_calls, print_mock.mock_calls)

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_choice_with_empty_options(self, input_mock, print_mock):
        with self.assertRaisesRegex(ValueError, r'Options may not be empty'):
            self.input_helper.choice('Test', [], 'y')

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_choice_with_invalid_default(self, input_mock, print_mock):
        with self.assertRaisesRegex(ValueError,
                                    r'Default must be included in options'):
            self.input_helper.choice('Test', ['y', 'n'], 'z')

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_choice_with_invalid_input(self, input_mock, print_mock):
        expected = 'y'
        expected_input_calls = [
            call('Test [Y/n] '),
            call('Test [Y/n] '),
            call('Test [Y/n] '),
        ]
        expected_print_calls = [
            call('Please enter a valid option.'),
            call('Please enter a valid option.'),
        ]

        input_mock.side_effect = ['t', 'x', 'y']

        value = self.input_helper.choice(
            'Test', ['y', 'n'], 'y')
        self.assertEqual(expected, value)
        self.assertEqual(expected_input_calls, input_mock.mock_calls)
        self.assertEqual(expected_print_calls, print_mock.mock_calls)

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_choice_with_uppercase_input(self, input_mock, print_mock):
        expected = 'y'
        expected_input_calls = [
            call('Test [Y/n] '),
        ]
        expected_print_calls = [
        ]

        input_mock.side_effect = ['Y']

        value = self.input_helper.choice(
            'Test', ['y', 'n'], 'y')
        self.assertEqual(expected, value)
        self.assertEqual(expected_input_calls, input_mock.mock_calls)
        self.assertEqual(expected_print_calls, print_mock.mock_calls)

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_choice_with_whitespace_input(self, input_mock, print_mock):
        expected = 'y'
        expected_input_calls = [
            call('Test [Y/n] '),
        ]
        expected_print_calls = [
        ]

        input_mock.side_effect = ['  y\n']

        value = self.input_helper.choice(
            'Test', ['y', 'n'], 'y')
        self.assertEqual(expected, value)
        self.assertEqual(expected_input_calls, input_mock.mock_calls)
        self.assertEqual(expected_print_calls, print_mock.mock_calls)

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_choice_with_none_option(self, input_mock, print_mock):
        with self.assertRaises(AttributeError):
            self.input_helper.choice(
                'Test', ['y', 'n', None], 'y')

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_confirm(self, input_mock, print_mock):
        expected = True
        expected_input_calls = [
            call('Test [y/N] '),
        ]
        expected_print_calls = [
        ]

        input_mock.side_effect = ['y']

        value = self.input_helper.confirm('Test')
        self.assertEqual(expected, value)
        self.assertEqual(expected_input_calls, input_mock.mock_calls)
        self.assertEqual(expected_print_calls, print_mock.mock_calls)

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_confirm_with_default_input(self, input_mock, print_mock):
        expected = True
        expected_input_calls = [
            call('Test [Y/n] '),
        ]
        expected_print_calls = [
        ]

        input_mock.side_effect = ['']

        value = self.input_helper.confirm('Test', True)
        self.assertEqual(expected, value)
        self.assertEqual(expected_input_calls, input_mock.mock_calls)
        self.assertEqual(expected_print_calls, print_mock.mock_calls)

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_select(self, input_mock, print_mock):
        expected = 0
        expected_input_calls = [
            call('Test [0/1/2] '),
        ]
        expected_print_calls = [
            call('0. zero'),
            call('1. one'),
            call('2. two'),
        ]

        input_mock.side_effect = ['0']

        select = ['zero', 'one', 'two']
        value = self.input_helper.select('Test', select)
        self.assertEqual(expected, value)
        self.assertEqual(expected_input_calls, input_mock.mock_calls)
        self.assertEqual(expected_print_calls, print_mock.mock_calls)

    @patch.object(userinteraction, 'print', create=True)
    @patch.object(userinteraction, 'input', create=True)
    def test_select_with_one_option(self, input_mock, print_mock):
        expected = 0
        expected_input_calls = [
        ]
        expected_print_calls = [
        ]

        input_mock.side_effect = []

        select = ['zero']
        value = self.input_helper.select('Test', select)
        self.assertEqual(expected, value)
        self.assertEqual(expected_input_calls, input_mock.mock_calls)
        self.assertEqual(expected_print_calls, print_mock.mock_calls)


if __name__ == '__main__':
    unittest.main()
