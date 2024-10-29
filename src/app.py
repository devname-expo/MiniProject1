import argparse
import csv
import re

from pathlib import Path
from frobenius import FrobeniusCalc


class App:
    def __init__(self):
        # Initialize parser
        self.parser = None
        # Parse args
        self.args = None
        # Format input given in args
        self.input = None

    def _init_argparse(self) -> argparse.ArgumentParser:
        """Initializes argparse object

        Returns:
            argparse.ArgumentParser: a parser
        """

        # Create ArgumentParser instance

        # Create Arguments
        #   data arg: string or csv
        #   parameter arg: upper bound on total units
        #   (?) parameter arg: upper bounds on individual units

        # Return parser
        return None

    # Validate input is comma separated list of positive integers
    def _validate_input(self, s: str):

        # Declare regex pattern for list of positive ints
        # Check input against regex
        # Call throw exception on failure

        pass

    # Transform string of ints to list
    def _string_to_list(self, s: str) -> list:

        # Call Validate input function
        # Split string by comma

        # Return list of ints
        return None

    # Validate list contains only digits for csvs
    def _validate_list(self, l: list):

        # Declare regex pattern
        # join list to string
        # Throw ValueError if not match

        pass

    # Read file to list of lists
    def _read_csv(self, csv_file: Path) -> list:

        # Read csv
        # For each line
        ## Validate list
        ## Transform to list of ints

        # Return list of lists of ints
        return None

    # Set units to list of positive integers scraped from input
    def _set_input(self) -> list:
        # If string given
        ## Call Transform function
        ## Append list to input variable

        # Else if file
        ## Create Path obj
        ## Check for .csv
        ## Call Read function
        pass

    # Run Frobenius calc on all input
    def run_frobenius_calculator(self):

        # Initialize FrobeniusCalc
        # For each input
        ## Get result
        ## Print output
        pass


if __name__ == "__main__":

    # Initialize App
    # Run Frobenius calculator
    pass
