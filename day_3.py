######### Day 3 #########
from itertools import combinations
from typing import List, Tuple

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


# Check battery bank for largest n joltage batteries
def find_largest_joltage_from_n_batteries_in_bank(battery_bank:str, number_of_batteries:int) -> int:
    """Finds the largest joltage from n batteries in a battery bank"""
    battery_bank_split = [int(battery) for battery in battery_bank]
    joltage_combinations: List[int] = []
    for combination in combinations(battery_bank_split, number_of_batteries):
        joltage_combinations.append(int("".join([str(x) for x in combination])))
    return max(joltage_combinations)


# Part 1 script
def part_1_script():
    """The script for my solution of part 1"""
    battery_banks = import_puzzle_input(
        path="puzzle_inputs/day_3.txt",
        test=False,
    )

    total_output_joltage = 0
    for battery_bank in battery_banks:
        total_output_joltage += find_largest_joltage_from_n_batteries_in_bank(
            battery_bank=battery_bank,
            number_of_batteries=2,
        )
    
    print(f"The total output joltage is {total_output_joltage} jolts")

# Part 2 script
def part_2_script():
    print("STARTING PART 2")
    """The script for my solution of part 1"""
    battery_banks = import_puzzle_input(
        path="puzzle_inputs/day_3.txt",
        test=True,
    )
    
    total_output_joltage = 0
    for battery_bank in battery_banks:
        total_output_joltage += find_largest_joltage_from_n_batteries_in_bank(
            battery_bank = battery_bank, 
            number_of_batteries=12,
        )
    
    print(f"The total output joltage is {total_output_joltage} jolts")


part_1_script()
part_2_script()