import argparse
import re
import math

from pathlib import Path

# import functions from solve.py

# Set constants
INPUT_UPPER_BOUND = 25  # the number of units the program will accept


# Throw an exception with given description
def throw_exception(s: str):
    pass


# Validate input is comma separated list of positive integers
def validate_input(s: str):

    # Declare regex pattern for list of positive ints
    # Check input against regex
    # Call throw exception on failure

    pass


# Transform string of ints to list
def string_to_list(s: str) -> list:

    # Call Validate input function
    # Split string by comma

    # Return list of ints
    return None


# Read file to list of lists
def read_csv(p: Path) -> list:

    # Handle concurrent computing
    # For each line
    ## Call Transform function

    # Return list of lists of ints
    return None


# Enforce limits
def enforce_limits(l: list) -> int:

    # Validate length meets INPUT_UPPER_BOUND
    # Call throw exception on failure

    # Return length
    return None


def init_argparse() -> argparse.ArgumentParser:

    # Create ArgumentParser instance

    # Create Arguments
    #   data arg: string or csv
    #   parameter arg: upper bound on total units
    #   (?) parameter arg: upper bounds on individual units

    # Return parser
    return None


if __name__ == "__main__":

    # Initialize parser
    # Parse args

    # If string given
    ## Call Transform function
    ## Append list to input variable

    # Else if file
    ## Create Path obj
    ## Check for .csv
    ## Call Read function

    # If size of 1
    ## Call solve for 1 function

    # Else
    ## Call reorder function
    ## (?) Handle gcd > 1

    ### If size of 2
    #### Call solve for coprimes function

    ### Else 3+
    #### Call Enforce Limits function
    #### Call solve for many function

    # Return Solution
    pass
