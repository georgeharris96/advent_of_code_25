######### Day 3 #########
from itertools import combinations
from typing import List

# Get sample input
def get_sample_input() -> List[str]:
    """Returns the sample input from the problem statment in the same format as the real puzzle input"""
    sample_input = [
        "987654321111111\n",
        "811111111111119\n",
        "234234234234278\n",
        "818181911112111\n",
        ]
    return sample_input


# Import puzzle input
def import_puzzle_input(path: str, test: bool = False) -> List[str]:
    """Checks if you are running a test and then returns either the sample input or the real puzzle input"""
    if test:
        puzzle_input = get_sample_input()
    else:
        with open(path) as f:
            puzzle_input = f.readlines()
    return [line.strip("\n") for line in puzzle_input]


# Check battery bank for largest joltage batteries
def find_largest_in_battery_bank(battery_bank: str) -> int:
    """Finds the largest joltage from a battery pair in a battery bank"""
    # Create all joltage pairs
    battery_bank_split: List[str] = [battery for battery in battery_bank]
    joltage_pairs = [int(battery_1 + battery_2) for battery_1, battery_2 in combinations(battery_bank_split, 2)]
    return max(joltage_pairs)


# Part 1 script
def part_1_script():
    """The script for my solution of part 1"""
    battery_banks = import_puzzle_input(
        path="puzzle_inputs/day_3.txt",
        test=False,
    )
    
    total_output_joltage = 0
    for battery_bank in battery_banks:
        total_output_joltage += find_largest_in_battery_bank(battery_bank)
    
    print(f"The total output joltage is {total_output_joltage} jolts")


part_1_script()