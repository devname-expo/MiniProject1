import argparse
import csv
import re

from pathlib import Path
from frobenius import solve_for_frobenius_number


# Validate input is comma separated list of positive integers
def validate_input(s: str):
    """Validates string is comma separated list of positive integers

    Args:
        s (str): string to validate

    Raises:
        ValueError: throws error if string is not only digits and commas
    """
    # Declare regex pattern for list of positive ints
    pattern = re.compile(r"\d+(,\d+)*$")
    if not pattern.match(s):
        raise ValueError(
            "Input must be a string of positive integers separated by commas. Ex: '1,2,3'"
        )


# Transform string of ints to list
def string_to_list(s: str) -> list:
    """Transforms string of integers to list

    Args:
        s (str): string to transform into list

    Returns:
        list: list of integers
    """
    validate_input(s)
    l = s.split(",")

    return l


def validate_list(l: list):
    """Validates list contains only digits

    Args:
        l (list): list to validate

    Raises:
        ValueError: throws error if list is not only positive digits
    """
    # Declare regex pattern for list of positive ints
    pattern = re.compile(r"(\d+,?)+$")
    if not pattern.match(",".join(l)):
        raise ValueError("Csv must contain only positive integers.")


# Read file to list of lists
def read_csv(csv_file: Path) -> list:
    """Reads csv file to list of lists of integers

    Args:
        csv_file (Path): Path object to a csv file

    Returns:
        list: a list of positive integers
    """
    with open(csv_file, mode="r") as file:
        csvFile = csv.reader(file)
        list_f = []
        for line in csvFile:
            validate_list(line)
            list_f.append([int(_) for _ in line])

    return list_f


def format_input(args: object):
    """Sets units to list of positive integers scraped from input.

    Returns:
        list: a list of lists of positive integers

    Raises:
        ValueError: raises error if file is given without .csv suffix
    """
    input = []
    if args.units:
        units_l = string_to_list(args.units)
        input.append(units_l)

    # Handle csv input
    else:
        path = Path(args.file)
        if path.suffix == ".csv":
            input = read_csv(path)
        else:
            raise ValueError("File must be csv format.")

    return input


def init_argparse() -> argparse.ArgumentParser:
    """Initializes argparse object

    Returns:
        argparse.ArgumentParser: a parser
    """
    parser = argparse.ArgumentParser(
        description="Determine the largest integer that cannot be reached using non-negative combinations of given integers.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-u",
        "--units",
        help="string of comma separated integers for combination",
        type=str,
    )
    group.add_argument(
        "-f",
        "--file",
        help="file containing comma separated integers for combination (Multiline will run multiple iterations with each line as input.)",
        type=str,
    )
    return parser


def run_frobenius_calculator(input: list):
    """Runs Frobenius Calculator on each given input"""

    for units in input:
        result = solve_for_frobenius_number(units)
        if result:
            print(
                f"The largest order volume that is NOT perfectly purchasable for units {units} is {result}."
            )
        else:
            print(f"There is no finite solution for units {units}.")


if __name__ == "__main__":

    parser = init_argparse()
    input = format_input(parser.args)
    run_frobenius_calculator(input)
