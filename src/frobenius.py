import math
from typing import Optional, List


def compute_gcd_values(first_number: int, number_list: list) -> tuple:
    """Computes GCD between a number and each number in a list, plus overall GCD.

    Args:
        first_number: A positive integer
        number_list: A list of positive integers

    Returns:
        A tuple containing (overall_gcd, list_of_pairwise_gcds)
    """
    pairwise_gcds = [math.gcd(first_number, number_list[0])]
    overall_gcd = pairwise_gcds[0]

    # Calculate GCD with remaining numbers
    for num in number_list[1:]:
        current_gcd = math.gcd(first_number, num)
        pairwise_gcds.append(current_gcd)
        overall_gcd = math.gcd(overall_gcd, current_gcd)

    return (overall_gcd, pairwise_gcds)


def is_list_coprime(remaining_nums: list) -> bool:
    """Checks if list is coprime

    Args:
        remaining_nums (list): a list of positive integers

    Returns:
        bool: True if coprime; False if not
    """
    # Start with first pair
    total_gcd = math.gcd(remaining_nums[0], remaining_nums[1])

    # Then step through each remaining unit
    for u in remaining_nums[1:]:
        total_gcd = math.gcd(u, total_gcd)
    return total_gcd == 1


def solve_for_frobenius_number(numbers: list) -> Optional[int]:
    """Computes the Frobenius number using the Round Robin Algorithm.

    For a set of numbers [a₁, a₂, ..., aₖ] where:
    - a₁ < a₂ < ... < aₖ
    - gcd(a₁, ..., aₖ) = 1

    The Frobenius number is the largest integer that cannot be expressed
    as a sum of these numbers with non-negative coefficients.

    More Detail:

    The algorithm builds a residue table [n₀, n₁, ..., n_{a₁-1}] where saved_val is the
    smallest number congruent to p modulo a₁ that can be represented using the remaining_nums.

    Example execution with remaining_nums [5,8,9]:
    ```
    Step             | n₀ | n₁ | n₂ | n₃ | n₄ | Current operation
    -----------------+----+----+----+----+----+-------------------------
    Initial          |  0 |  ∞ |  ∞ |  ∞ |  ∞ | Start with just a₁=5
    -----------------+----+----+----+----+----+-------------------------
    Add a₂=8 loop 1  |  0 |  ∞ |  ∞ |  8 |  ∞ | 0+8=8 (mod 5 = 3)
    Add a₂=8 loop 2  |  0 | 16 |  ∞ |  8 |  ∞ | 8+8=16 (mod 5 = 1)
    Add a₂=8 loop 3  |  0 | 16 |  ∞ |  8 | 24 | 16+8=24 (mod 5 = 4)
    Add a₂=8 loop 4  |  0 | 16 | 32 |  8 | 24 | 24+8=32 (mod 5 = 2)
    -----------------+----+----+----+----+----+-------------------------
    Add a₃=9 loop 1  |  0 | 16 | 32 |  8 |  9 | 0+9=9 (mod 5 = 4)
    Add a₃=9 loop 2  |  0 | 16 | 32 |  8 |  9 | 9+9=18 > 8, no change
    Add a₃=9 loop 3  |  0 | 16 | 17 |  8 |  9 | 18+9=27→17 (mod 5 = 2)
    Add a₃=9 loop 4  |  0 | 16 | 17 |  8 |  9 | 27+9=36 > 16, stop
    -----------------+----+----+----+----+----+-------------------------
    Final            |  0 | 16 | 17 |  8 |  9 | Frobenius = 17-5 = 12
    --------------------------------------------------------------------
    ```

    The table shows how the residue table evolves as each unit is added:
    1. Start with n₀=0 and all other residues set to ∞
    2. For each new unit aᵢ:
       - Start with n=0
       - Repeatedly add aᵢ and update the corresponding residue saved_val if the new
         value is smaller than the existing one
       - Stop when we return to a residue with a larger existing value
    3. The Frobenius number is max(saved_val) - a₁


    Args:
        numbers: A sorted list of positive integers

    Returns:
        The Frobenius number or None if no solution exists

    """

    # Validate input
    if len(numbers) < 2:
        return None

    # Handle leading zeros issues
    if not numbers[0]:
        numbers = list(filter(lambda x: x > 0, numbers))
        if not numbers:
            return None

    first_num = numbers[0]
    remaining_nums = numbers[1:]

    # Initialize residue table
    residue_table = [float("inf")] * first_num
    residue_table[0] = 0

    overall_gcd, pairwise_gcds = compute_gcd_values(first_num, remaining_nums)
    if not overall_gcd or overall_gcd > 1:
        return None

    # Main loop to step through the remaining_nums
    # Ex: [5,8,9]
    for idx, current_num in enumerate(remaining_nums):  # Ex: current_num = 8
        current_gcd = pairwise_gcds[idx]

        # Process each remainder class
        for remainder in range(current_gcd):  # Ex: r = 0

            # Save minimum value in current remainder class
            saved_val = min(
                [
                    residue_table[p]
                    for p in range(first_num)
                    if p % current_gcd == remainder
                ]
            )

            # Update residue table if we found a finite value
            if saved_val != float("inf"):  # Ex: saved_val = 8
                for _ in range(first_num // current_gcd):  # Ex: _ = 2;

                    # Compute the next multiple and position
                    new_val = saved_val + current_num  # Ex: 8 + 8 = 16
                    table_position = new_val % first_num  # Ex: (mod 5 = 1)

                    # Keep smaller value
                    saved_val = min(
                        new_val, residue_table[table_position]
                    )  # Ex: 16 < ∞
                    residue_table[table_position] = saved_val  # [0, 16, ∞, 8, ∞]

    return max(residue_table) - first_num
