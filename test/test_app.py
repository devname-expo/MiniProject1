import unittest
import sys
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from io import StringIO

sys.path.append("./src")
from app import App


class TestApp(unittest.TestCase):
    """Test suite for App class"""

    @patch("argparse.ArgumentParser")
    def test_init_argparse(self, mock_ArgumentParser):
        """Test argument parser initialization"""

        # Arrange
        mock_parser = Mock()
        mock_group = Mock()
        mock_parser.add_mutually_exclusive_group.return_value = mock_group
        mock_ArgumentParser.return_value = mock_parser

        # Apply
        App._init_argparse(None)

        # Assert
        mock_parser.add_mutually_exclusive_group.assert_called_once()
        mock_group.add_argument.assert_any_call(
            "-u",
            "--units",
            help="string of comma separated integers for combination",
            type=str,
        )
        mock_group.add_argument.assert_any_call(
            "-f",
            "--file",
            help="file containing comma separated integers for combination (Multiline will run multiple iterations with each line as input.)",
            type=str,
        )

    def test_validate_input_valid_cases(self):
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
                    App._validate_input(None, input_str)

                # Assert
                except ValueError as e:
                    self.fail(
                        f"Validation failed for edge case '{description}': {str(e)}"
                    )

    def test_validate_input_invalid_cases(self):
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
                    App._validate_input(None, input_str)

    def test_validate_input_input_types(self):
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
                    App._validate_input(None, invalid_input)  # type: ignore

    def test_string_to_list(self):
        """Test string to list conversion"""

        # Arrange
        test_cases = [
            ("1,2,3", ["1", "2", "3"]),
            ("42", ["42"]),
            ("1,23,456", ["1", "23", "456"]),
        ]

        for input_str, expected in test_cases:
            with self.subTest(input=input_str):
                mock_app = Mock()
                mock_app._validate_input = Mock()

                # Apply
                result = App._string_to_list(mock_app, input_str)

                # Assert
                self.assertEqual(result, expected)
                mock_app._validate_input.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    def test_read_csv_valid(self, mock_file):
        """Test CSV file reading with valid content"""

        # Arrange
        mock_file.return_value.__enter__.return_value = StringIO("1,2,3\n4,5,6\n7,8,9")
        mock_app = Mock()
        mock_app._validate_list = Mock()

        # Apply
        result = App._read_csv(mock_app, Path("test.csv"))

        # Assert
        expected = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(result, expected)
        self.assertEqual(mock_app._validate_list.call_count, len(expected))

    def test_format_input_units(self):
        """Test input formatting with units argument"""

        # Arrange
        mock_app = Mock()

        mock_args = Mock()
        mock_args.units = "1,2,3"
        mock_args.file = None
        mock_app.args = mock_args

        mock_string_to_list = Mock()
        mock_string_to_list.return_value = ["1", "2", "3"]
        mock_app._string_to_list = mock_string_to_list

        # Apply
        result = App._format_input(mock_app)

        # Assert
        mock_string_to_list.assert_called_once_with("1,2,3")
        self.assertEqual(result, [["1", "2", "3"]])

    def test_format_input_file(self):
        """Test input formatting with file type"""

        # Arrange
        mock_app = Mock()

        mock_args = Mock()
        mock_args.units = None
        mock_args.file = "test.csv"
        mock_app.args = mock_args

        mock_read_csv = Mock()
        mock_read_csv.return_value = [["1", "2", "3"], ["2", "3", "4"]]
        mock_app._read_csv = mock_read_csv

        # Apply
        result = App._format_input(mock_app)

        # Assert
        mock_read_csv.assert_called_once()
        self.assertEqual(result, [["1", "2", "3"], ["2", "3", "4"]])

    def test_formay_input_invalid_file(self):
        """Test input formatting with invalid file type"""

        # Arrange
        mock_app = Mock()

        mock_args = Mock()
        mock_args.units = None
        mock_args.file = "test.txt"
        mock_app.args = mock_args

        mock_read_csv = Mock()
        mock_app.__read_csv = mock_read_csv

        # Assert
        with self.assertRaises(ValueError):

            # Apply
            App._format_input(mock_app)

            # Assert
            mock_read_csv.assert_not_called()

    @patch("frobenius.FrobeniusCalc.solve_for_frobenius_number")
    def test_run_frobenius_calculator(self, mock_solve):
        """Test Frobenius calculator execution"""

        # Arrange
        mock_app = Mock()
        mock_input = [[5, 8, 9, 12]]
        mock_app.input = mock_input

        mock_solve.return_value = 11

        with patch("builtins.print") as mock_print:

            # Apply
            App.run_frobenius_calculator(mock_app)

            # Assert
            mock_solve.assert_called_once()
            mock_print.assert_called_once_with(
                f"The Frobenius number of {mock_input[0]} is 11."
            )


if __name__ == "__main__":
    unittest.main()
