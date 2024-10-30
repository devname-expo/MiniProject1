import argparse
import csv
import re

from pathlib import Path
from frobenius import FrobeniusCalc


class App:

    def __init__(self):
        self.parser = self._init_argparse()
        self.args = self.parser.args
        self.input = self._format_input()

    def _init_argparse(self) -> argparse.ArgumentParser:
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

    def _validate_input(self, s: str):
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

    def _string_to_list(self, s: str) -> list:
        """Transforms string of integers to list

        Args:
            s (str): string to transform into list

        Returns:
            list: list of integers
        """
        self._validate_input(s)
        l = s.split(",")

        return l

    def _validate_list(self, l: list):
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

    def _read_csv(self, csv_file: Path) -> list:
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
                self._validate_list(line)
                list_f.append([int(_) for _ in line])

        return list_f

    def _format_input(self) -> list:
        """Sets units to list of positive integers scraped from input.

        Returns:
            list: a list of lists of positive integers

        Raises:
            ValueError: raises error if file is given without .csv suffix
        """
        input = []
        if self.args.units:
            units_l = self._string_to_list(self.args.units)
            input.append(units_l)

        # Handle csv input
        else:
            path = Path(self.args.file)
            if path.suffix == ".csv":
                input = self._read_csv(path)
            else:
                raise ValueError("File must be csv format.")

        return input

    def run_frobenius_calculator(self):
        """Runs Frobenius Calculator on each given input"""
        calc = FrobeniusCalc()

        for units in self.input:
            result = FrobeniusCalc.solve_for_frobenius_number(units)
            print(f"The Frobenius number of {units} is {result}.")


if __name__ == "__main__":

    app = App()
    app.run_frobenius_calculator()
