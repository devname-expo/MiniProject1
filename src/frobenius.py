import math
from typing import Optional, List


def solve_for_frobenius_number(l: list) -> Optional[List[int]]:
    """Given a list of positive integer numbers, solves for the Frobenius number.

    Args:
        l (list): a list of positive integers

    Returns:
        Optional[List[int]]: The largest number that cannot be expressed as a linear combination of positive integers. None if no solution or list size of 1.
    """

    try:

        # NOTE: Adding check for lists with 0s
        while True:
            if l[0]:
                # Initialize head and units
                head_unit = l[0]
                units = l[1:]
                break
            else:
                l = l[1:]

    except IndexError:  # l < 2
        return None

    # Initialize residue_table by setting first index of list to 0, and all other indices to infinity
    res_table = [float("inf")] * head_unit
    res_table[0] = 0

    # NOTE: Adding check for performance on very large non-coprime numbers
    if sum(l) > 10000:
        # check for total gcd.
        total_gcd = math.gcd(l[0], l[1])
        for u in units[1:]:
            total_gcd = math.gcd(u, total_gcd)
        if total_gcd != 1:
            return None

    # For each additional unit (2nd through last)
    for curr_unit in units:

        # Find the gcd between the first unit and this additional unit
        gcd = math.gcd(head_unit, curr_unit)

        # For the range of the gcd
        for r in range(gcd):

            # Step through the table, using the loop number as a step size, and take the minimum value
            min_val = min([res_table[i] for i in range(head_unit) if i % gcd == r])

            # If the min is a finite value, then
            if min_val != float("inf"):

                # Loop (first_unit / gcd - 1) times
                for _ in range(int(head_unit / gcd)):

                    # Add the current unit value to min_value
                    min_val = min_val + curr_unit

                    # Get remainder when divided by first unit
                    i = min_val % head_unit

                    # Update res table value to be minimum of min_value and what's saved in residue_table
                    min_val = min(min_val, res_table[i])
                    res_table[i] = min_val

    # return max(residue_table) - first_unit
    max_value = max(res_table)
    if max_value != float("inf"):
        return max_value - head_unit
    else:
        return None
