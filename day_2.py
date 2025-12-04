######### Day 2 #########
import math
from typing import List


# Get sample input
def get_sample_input() -> List[str]:
    """Returns the sample input from the problem definition in the same format as the real puzzle input would be after import"""
    return ["11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124\n"]


# Import puzzle input
def import_puzzle_input(path:str, test:bool = False) -> str:
    """Imports the puzzle input from the file. If it is a test set the test arg to True and it will load the sample"""
    if test:
        puzzle_input = get_sample_input()
    else:
        with open(path) as f:
            puzzle_input = f.readlines()
    return puzzle_input[0].strip("\n")


# Split puzzle input into id_ranges
def split_input(input:str) -> List[str]:
    """Splits the puzzle input into a list of different ranges"""
    return input.split(",")


# Reformat ranges
def reformat_id_range(id_range:str) -> List[str]:
    """Splits each id range into the min and max numbers"""
    return id_range.split("-")


# Unpack range
def unpack_range(id_range: List[str]) -> List[str]:
    """Takes the min and max values of a range and unpacks them into a full list of numbers"""
    converted_types = [int(id_range[0]), int(id_range[1])]
    unpacked_range = list(range(converted_types[0], converted_types[-1]+1))
    return [str(x) for x in unpacked_range]


# Check length of ID
def check_id_length(id_to_check:str) -> bool:
    """Checks to see if the length of an id is odd"""
    if len(id_to_check) % 2 == 0:
        return False
    else:
        return True


# Check if ID is valid
def is_valid_pattern(id_to_check: str) -> bool:
    """Checks if an id is valid
    
    This function first checks if the length of the id makes it valid (the id is odd). Then if even, splits the id in two and checks the two halfs against each other to see if they match.
    """

    # Check length of number
    if check_id_length(id_to_check):
        return True
    else:
        mid_point = math.floor(len(id_to_check) / 2)
        left_hand_side, right_hand_side = id_to_check[:mid_point], id_to_check[mid_point:]
        if left_hand_side == right_hand_side:
            return False
        else:
            return True
        

# Check if ID is repetitive
def is_repetitve_id(id_to_check: str) -> bool:
    """Checks if an id is a repetitve pattern
    
    This code iterates through different chunk sizes to see if an id is made up of repetitive patterns. It does this by creating a chunk and reconstructing the id by repeating the chunk. If the reconstructed id is the same as the input then it is a repetitve id.
    """
    length = len(id_to_check)
    for chunk_size in range(1, (length // 2) + 1):
        if length % chunk_size == 0:

            pattern = id_to_check[:chunk_size]
            multiplier = length // chunk_size
            reconstructed_id = pattern * multiplier
        
            if reconstructed_id == id_to_check:
                return True
    return False


# Part 1 script
def part_1_script():
    """Contains the solution to part 1"""

    raw_puzzle_input = import_puzzle_input(
        path = "puzzle_inputs/day_2.txt",
        test = False,
        )
    
    split_puzzle_input = split_input(raw_puzzle_input)

    sum_of_invalid_ids = 0
    for raw_id_range in split_puzzle_input:
        reformed_id_range = reformat_id_range(raw_id_range)
        unpacked_id_range = unpack_range(reformed_id_range)


        for id_number in unpacked_id_range:
            id_status = is_valid_pattern(id_number)

            if id_status:
                pass
            else:
                sum_of_invalid_ids += int(id_number)
    print(f"The sum of all the invalid ids is: {sum_of_invalid_ids}")


#Part 2 script
def part_2_script():
    """Contains the solution to part 2"""
    raw_puzzle_input = import_puzzle_input(
        path = "puzzle_inputs/day_2.txt",
        test = False,
    )

    split_puzzle_input = split_input(raw_puzzle_input)

    sum_of_invalid_ids = 0
    for raw_id_range in split_puzzle_input:
            reformed_id_range = reformat_id_range(raw_id_range)
            unpacked_id_range = unpack_range(reformed_id_range)


            for id_number in unpacked_id_range:
                id_status = is_valid_pattern(id_number)
                id_repetitive = is_repetitve_id(id_number)

                if id_status == True and id_repetitive == False:
                    pass
                else:
                    sum_of_invalid_ids += int(id_number)

    print(f"The sum of all the invalid ids is: {sum_of_invalid_ids}")


part_1_script()
part_2_script()