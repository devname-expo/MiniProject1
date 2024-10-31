# Mini Project

A command-line tool for calculating Frobenius numbers - the largest integer that cannot be expressed as a non-negative linear combination of given integers. This problem is also known as the "Coin Change Problem" or "Chicken McNugget Problem"

## What's a Frobenius Number? 🤔

Imagine you're at a restaurant that only sells chicken strips in boxes of 3 or 5. Hungry for exactly 1, 2, 4, or 7 strips? Tough cluck! 🐔 No matter how you combine the boxes, those amounts are impossible. But here's where the magic happens - after 7 strips, you can order ANY amount your hungry heart desires! Want 8 strips? Grab a 3-box and a 5-box. Craving 9? Triple down on 3-boxes. Need 10? Two 5-boxes and you're feasting. The chicken strip possibilities become endless!

And now that we are all good and hungry, let's get back to the math, because this phenomenon goes beyond just chicken strips. For any set of numbers that share no common factors, there's always a threshold where every larger number can be created from their combinations. This threshold - the "largest impossible amount" - is called the Frobenius number an it shows up everywhere from currency design to chemical compound analysis (though we prefer the chicken strip example, for obvious delicious reasons).

## Installation

1. Clone this repository:
```bash
git clone https://github.com/devname-expo/MiniProject1.git
cd frobenius-calculator
```


## Usage

The calculator can be used in two ways:

### 1. Direct Input

Use the `-u` or `--units` flag followed by a comma-separated list of positive integers:

```bash
python frobenius_calculator.py -u "3,5,7"
```

### 2. CSV File Input

Use the `-f` or `--file` flag to process multiple sets of numbers from a CSV file:

```bash
python frobenius_calculator.py -f input.csv
```

**Note**: use flag --verbose for more detailed response

The CSV file should contain one set of comma-separated positive integers per line:
```csv
3,5,7
4,6,9,12
6,8,12
```

## Examples

### Command Line Input
```bash
$ python frobenius_calculator.py -u "3,5,7"
Input [3, 5, 7]: Frobenius number = 4
```

### CSV File Input
```bash
$ python frobenius_calculator.py -f examples.csv
Input [3, 5, 7]: Frobenius number = 4
Input [4, 6, 9]: Frobenius number = 11
Input [6, 8, 12]: No finite solution exists
```


## Technical Details

### Input Requirements

- All numbers must be positive integers
- For CSV files:
  - One set of numbers per line
  - Numbers should be comma-separated
  - No empty lines 
  - No headers
  - No trailing commas

### Mathematical Considerations

- The program will indicate when no finite solution exists (e.g., when the input numbers share a common factor)
- The implementation uses efficient algorithms to calculate the Frobenius number
- For certain large inputs, computation time may be significant


## License

[MIT License](LICENSE)

## Acknowledgments

This implementation uses the Round Robin approach for calculating Frobenius numbers as described by Sebastian Böcker and Zsuzsanna Lipták in their paper "The Money Changing Problem revisited: Computing the Frobenius number in time O(k a1)". For more information about the mathematical background, see:
- [Coin Problem on Wikipedia](https://en.wikipedia.org/wiki/Coin_problem)
- [Postage Stamp Problem / Chicken McNugget Theorem on Brilliant](https://brilliant.org/wiki/postage-stamp-problem-chicken-mcnugget-theorem/)
