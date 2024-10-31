import unittest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path

import app


class TestApp(unittest.TestCase):
    """Test suite for app file"""

    @patch("argparse.ArgumentParser")
    def test_create_argument_parser(self, mock_ArgumentParser):
        """Test argument parser initialization"""

        # Arrange
        mock_parser = Mock()
        mock_group = Mock()
        mock_parser.add_mutually_exclusive_group.return_value = mock_group
        mock_ArgumentParser.return_value = mock_parser

        # Apply
        app.create_argument_parser()

        # Assert
        mock_parser.add_mutually_exclusive_group.assert_called_once()
        mock_group.add_argument.assert_any_call(
            "-u",
            "--units",
            help="Comma-separated integers (e.g., '1,2,3')",
            type=str,
        )
        mock_group.add_argument.assert_any_call(
            "-f",
            "--file",
            help="CSV file with integers (one combination per line for multiple calculations)",
            type=str,
        )

    def test_validate_comma_separated_integers_valid_cases(self):
        """Test input validation with valid inputs"""

        # Arrange
        valid_inputs = {
            "1,2,3": "simple list",
            "10": "single digit",
            "1,2,3,4,5": "list of ones",
            "11,22,33,44,55": "list of tens",
            "123,456,789": "list of hundreds",
            "1,23,456,7890": "increasing list",
            "10,20,30,40,50,60,70,80,90,100": "long list",
            "0": "single zero",
            "0,1,2": "leading zero",
            "1,2,0": "trailing zero",
            "01,2,3": "padded zero",
            "999999999999": "very large number",
        }

        for input_str, description in valid_inputs.items():

            with self.subTest(input=input_str, description=description):

                # Apply
                try:
                    app.validate_comma_separated_integers(input_str)

                # Assert
                except ValueError as e:
                    self.fail(
                        f"Validation failed for edge case '{description}': {str(e)}"
                    )

    def test_validate_comma_separated_integers_invalid_cases(self):
        """Test various invalid input formats"""

        # Arrange
        invalid_inputs = {
            "": "empty string",
            "1,2,": "trailing comma",
            ",1,2,3": "leading comma",
            "1,,2": "double comma",
            "1,2, 3": "space after comma",
            " 1,2,3": "leading space",
            "1,2,3 ": "trailing space",
            "a,b,c": "letters",
            "1,2,3,a": "mix of numbers and letters",
            "1.2,3,4": "decimal numbers",
            "-1,2,3": "negative numbers",
            "1;2;3": "wrong separator",
            "1,2,3,": "trailing comma",
            "1,2,,3": "empty value between commas",
            "1,2,3,+4": "plus sign",
            "0x1,2,3": "hexadecimal",
            "1e2,3,4": "scientific notation",
            "2.0,4.5,6.7": "floats",
            "-3,-5,-2": "negatives",
        }

        for input_str, description in invalid_inputs.items():
            with self.subTest(input=input_str, description=description):

                # Assert
                with self.assertRaises(
                    ValueError,
                    msg=f"Failed to raise ValueError for {description}: {input_str}",
                ):
                    # Apply
                    app.validate_comma_separated_integers(input_str)

    def test_validate_comma_separated_integers_input_types(self):
        """Test input type validation"""

        # Arrange
        invalid_types = [None, 123, [1, 2, 3], {"1": "2"}, True, 3.14]

        for invalid_input in invalid_types:
            with self.subTest(input=invalid_input):

                # Assert
                with self.assertRaises(
                    (ValueError, AttributeError, TypeError),
                    msg=f"Failed to raise error for invalid type: {type(invalid_input)}",
                ):
                    # Apply
                    app.validate_comma_separated_integers(None, invalid_input)  # type: ignore

    @patch("app.validate_comma_separated_integers")
    def test_parse_integer_string(self, mock_validate_input):
        """Test string to list conversion"""

        # Arrange
        test_cases = [
            ("1,2,3", [1, 2, 3]),
            ("42", [42]),
            ("1,23,456", [1, 23, 456]),
        ]

        for input_str, expected in test_cases:
            with self.subTest(input=input_str):

                # Apply
                result = app.parse_integer_string(input_str)

                # Assert
                self.assertEqual(result, expected)
                mock_validate_input.assert_called()

    @patch("builtins.open", mock_open(read_data="1,2,3\n4,5,6\n7,8,9"))
    def test_read_csv_to_integer_lists_valid(self):
        """Test CSV file reading with valid content"""
        # Arrange

        # Apply
        with patch(
            "app.validate_comma_separated_integers"
        ) as mock_validate_comma_separated_integers:
            result = app.read_csv_to_integer_lists(Path("test.csv"))

        # Assert
        expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(result, expected)
        self.assertEqual(
            mock_validate_comma_separated_integers.call_count, len(expected)
        )

    @patch("app.parse_integer_string")
    def test_process_input_args_units(self, mock_string_to_list):
        """Test input formatting with units argument"""

        # Arrange
        mock_args = Mock()
        mock_args.units = "1,2,3"
        mock_args.file = None

        mock_string_to_list.return_value = ["1", "2", "3"]

        # Apply
        result = app.process_input_args(mock_args)

        # Assert
        mock_string_to_list.assert_called_once_with("1,2,3")
        self.assertEqual(result, [["1", "2", "3"]])

    @patch("app.read_csv_to_integer_lists")
    def test_process_input_args_file(self, mock_read_csv):
        """Test input formatting with file type"""

        # Arrange
        mock_args = Mock()
        mock_args.units = None
        mock_args.file = "test.csv"

        mock_read_csv.return_value = [["1", "2", "3"], ["2", "3", "4"]]

        # Apply
        result = app.process_input_args(mock_args)

        # Assert
        mock_read_csv.assert_called_once()
        self.assertEqual(result, [["1", "2", "3"], ["2", "3", "4"]])

    @patch("app.read_csv_to_integer_lists")
    def test_process_input_args_invalid_file(self, mock_read_csv):
        """Test input formatting with invalid file type"""

        # Arrange
        mock_args = Mock()
        mock_args.units = None
        mock_args.file = "test.txt"

        # Assert
        with self.assertRaises(ValueError):

            # Apply
            app.process_input_args(mock_args)

            # Assert
            mock_read_csv.assert_not_called()

    @patch("app.solve_for_frobenius_number")
    def test_calculate_and_print_results(self, mock_solve):
        """Test Frobenius calculator execution"""

        # Arrange
        mock_input = [[5, 8, 9, 12]]
        mock_solve.return_value = 11

        with patch("builtins.print") as mock_print:

            # Apply
            app.calculate_and_print_results(mock_input)

            # Assert
            mock_solve.assert_called_once()
            mock_print.assert_called_once_with(
                f"The largest order volume that is NOT perfectly purchasable for units {mock_input[0]} is 11."
            )

    @patch("app.solve_for_frobenius_number")
    def test_calculate_and_print_results_None(self, mock_solve):
        """Test Frobenius calculator execution if result is None"""

        # Arrange
        mock_input = [[5], [2, 4]]
        mock_solve.return_value = None

        with patch("builtins.print") as mock_print:

            # Apply
            app.calculate_and_print_results(mock_input)

            # Assert
            self.assertEqual(mock_print.call_count, 2)
            mock_print.assert_called_with(
                f"There is no finite solution for units {mock_input[1]}."
            )


if __name__ == "__main__":
    unittest.main()
