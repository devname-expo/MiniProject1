import unittest
from typing import Optional, List
from frobenius import solve_for_frobenius_number


class TestFrobeniusNumber(unittest.TestCase):
    """Test suite for the Frobenius number solver function."""

    def test_empty_list(self):
        """Test that an empty list returns None."""
        self.assertIsNone(solve_for_frobenius_number([]))

    def test_single_element(self):
        """Test that a list with single element returns None."""
        self.assertIsNone(solve_for_frobenius_number([5]))

    def test_coprime_numbers(self):
        """Test known Frobenius numbers for coprime pairs.

        Cases:
        - (2,3) -> 1: Can make all numbers > 1 using combinations of 2 and 3
        - (3,4) -> 5: Can make all numbers > 5 using combinations of 3 and 4
        """
        self.assertEqual(solve_for_frobenius_number([2, 3]), 1)
        self.assertEqual(solve_for_frobenius_number([3, 4]), 5)

    def test_non_coprime_numbers(self):
        """Test that numbers with GCD > 1 return None.

        When numbers aren't coprime, infinite numbers can't be represented,
        so there's no valid Frobenius number.
        """
        self.assertIsNone(solve_for_frobenius_number([4, 6]))

    def test_three_numbers(self):
        """Test Frobenius number calculation with three input numbers.

        Tests the known case where [6, 9, 20] has Frobenius number 43.
        """
        self.assertEqual(solve_for_frobenius_number([6, 9, 20]), 43)

    def test_ascending_order(self):
        """Test that input order doesn't affect result (ascending case)."""
        self.assertEqual(solve_for_frobenius_number([3, 5, 7]), 4)

    def test_descending_order(self):
        """Test that input order doesn't affect result (descending case)."""
        self.assertEqual(solve_for_frobenius_number([7, 5, 3]), 4)

    def test_no_order(self):
        """Test that input order doesn't affect result."""
        self.assertEqual(solve_for_frobenius_number([5, 7, 3]), 4)

    def test_zero(self):
        """Test that zero order doesn't affect result."""
        self.assertEqual(solve_for_frobenius_number([0, 3, 5, 7]), 4)

    def test_all_zeros(self):
        """Test that zero order doesn't affect result."""
        self.assertIsNone(solve_for_frobenius_number([0, 0, 0, 0]))

    def test_repeats(self):
        """Test that repeated number don't affect result."""
        self.assertEqual(solve_for_frobenius_number([3, 3, 5, 7]), 4)

    def test_non_integer(self):
        """Test that non-integer inputs raise TypeError."""
        with self.assertRaises(TypeError):
            solve_for_frobenius_number([2.5, 3])

    def test_large_numbers(self):
        """Test Frobenius number calculation with three input numbers.

        Tests the known case where [9901, 10000, 10099] has Frobenius number 49980149.
        """
        self.assertEqual(solve_for_frobenius_number([9901, 10000, 10099]), 49980149)

    def test_large_non_coprime_numbers(self):
        """Test that large numbers with GCD > 1 return None.

        When numbers aren't coprime, infinite numbers can't be represented,
        so there's no valid Frobenius number.
        """
        self.assertIsNone(solve_for_frobenius_number([10000, 20000]))

    def test_long_sequences(self):
        """Test Frobenius number calculation with three input numbers.

        Tests the known case where
        [101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173]
        has Frobenius number 402.
        """
        self.assertEqual(
            solve_for_frobenius_number(
                [
                    101,
                    103,
                    107,
                    109,
                    113,
                    127,
                    131,
                    137,
                    139,
                    149,
                    151,
                    157,
                    163,
                    167,
                    173,
                ]
            ),
            402,
        )

    def test_long_sequences_large_numbers(self):
        """Test Frobenius number calculation with three input numbers.

        Test long sequences of large numbers.
        """
        self.assertEqual(
            solve_for_frobenius_number(
                [
                    1000001,
                    1000003,
                    1000007,
                    1000009,
                    1000013,
                    1000027,
                    1000031,
                    1000037,
                    1000039,
                    1000049,
                    1000051,
                    1000057,
                    1000063,
                    1000067,
                    1000073,
                ]
            ),
            27779027777,
        )


if __name__ == "__main__":
    unittest.main()
