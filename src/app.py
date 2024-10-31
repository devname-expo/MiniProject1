import argparse
import csv
import re
from pathlib import Path
from typing import List
from frobenius import solve_for_frobenius_number

INTEGER_LIST_PATTERN = re.compile(r"\d+(,\d+)*$")


def validate_comma_separated_integers(input_str: str) -> None:
    """Validates that a string contains only comma-separated positive integers.

    Args:
        input_str: String to validate

    Raises:
        ValueError: If string contains invalid characters or format
    """
    if not INTEGER_LIST_PATTERN.match(input_str):
        raise ValueError(
            "Input must be positive integers separated by commas. Example: '1,2,3'"
        )


def parse_integer_string(input_str: str) -> List[int]:
    """Converts a comma-separated string of integers into a list.

    Args:
        input_str: String of comma-separated integers

    Returns:
        List of integers parsed from the string
    """
    validate_comma_separated_integers(input_str)
    return [int(num) for num in input_str.split(",")]


def read_csv_to_integer_lists(file_path: Path) -> List[List[int]]:
    """Reads CSV file and returns lists of integers from each line.

    Args:
        file_path: Path to CSV file

    Returns:
        List of integer lists, one per CSV line
    """
    integer_lists = []

    with open(file_path, mode="r") as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            validate_comma_separated_integers(",".join(line))
            integer_lists.append([int(num) for num in line])

    return integer_lists


def process_input_args(args: argparse.Namespace) -> List[List[int]]:
    """Processes command line arguments into lists of integers.

    Args:
        args: Parsed command line arguments

    Returns:
        List of integer lists to process

    Raises:
        ValueError: If file is not CSV format
    """
    if args.units:
        return [parse_integer_string(args.units)]

    path = Path(args.file)
    if path.suffix.lower() != ".csv":
        raise ValueError("Input file must be in CSV format")

    return read_csv_to_integer_lists(path)


def create_argument_parser() -> argparse.ArgumentParser:
    """Creates and configures the argument parser.

    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description=(
            "Calculate the largest integer that cannot be reached using "
            "non-negative combinations of given integers."
        )
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-u", "--units", help="Comma-separated integers (e.g., '1,2,3')", type=str
    )
    group.add_argument(
        "-f",
        "--file",
        help="CSV file with integers (one combination per line for multiple calculations)",
        type=str,
    )
    # Add verbose flag
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",  # This makes it a flag that's False by default
        help="Increase output verbosity",
    )
    return parser


def calculate_and_print_results(integer_lists: List[List[int]], verbose: bool) -> None:
    """Calculates and prints Frobenius numbers for each integer list.

    Args:
        integer_lists: List of integer lists to process
    """
    for numbers in integer_lists:
        result = solve_for_frobenius_number(numbers)

        if verbose:
            if result is not None:
                print(
                    f"The largest order volume that is NOT perfectly purchasable "
                    f"for units {numbers} is {result}."
                )

            else:
                print(f"There is no finite solution for units {numbers}.")
        else:
            print(f"{numbers} -> {result}")


def main():
    """Main entry point for the Frobenius calculator."""
    parser = create_argument_parser()
    args = parser.parse_args()

    integer_lists = process_input_args(args)
    calculate_and_print_results(integer_lists, args.verbose)


if __name__ == "__main__":
    main()
