######### Day 3 #########
from typing import List
import numpy as np

# Get floor layout
def get_sample_input() -> List[str]:
    """Returns the sample from the problem statement in the same form as the regular input"""
    sample_floor_layout = [
        "..@@.@@@@.\n",
        "@@@.@.@.@@\n",
        "@@@@@.@.@@\n",
        "@.@@@@..@.\n",
        "@@.@@@@.@@\n",
        ".@@@@@@@.@\n",
        ".@.@.@.@@@\n",
        "@.@@@.@@@@\n",
        ".@@@@@@@@.\n",
        "@.@.@@@.@.\n",
    ]
    return sample_floor_layout



def get_floor_layout(path:str, test:bool = False) -> List[str]:
    """Retrieves either the sample or real floor layout"""
    if test: # Is it a test?..
        floor_layout = get_sample_input()
    else: # ..or not?
        with open(path) as f:
            floor_layout = f.readlines()
    return [row.strip("\n") for row in floor_layout]


# Create grid
def process_grid(floor_layout:List[str]) -> List[List[int]]:
    """Converts the array of text into a matrix of ints"""
    processed_floor_layout: List[List[int]] = []
    for row in floor_layout:
        processed_row: List[int] = []
        for column in [col for col in row]:
            if column == "@":
                processed_row.append(1)
            else:
                processed_row.append(0)
        processed_floor_layout.append(processed_row)
    return processed_floor_layout


def create_grid(floor_layout:List[str]) -> np.ndarray:
    """Converts a list of strings into a np.ndarray which represents the floor layout
    
    The area is padded by 1 to allow for indexing.
    """
    return np.pad(np.array(process_grid(floor_layout)), pad_width=1, constant_values=0, mode="constant")


# Find rolls which can be accessed
def number_of_rolls_in_grid(grid:np.ndarray):
    """Finds the number of rolls inside of a grid"""
    return np.sum(grid)

def find_accessible_rolls(floor_layout:np.ndarray) -> int:
    """defines the search space and then retrives the number of rolls which are accessable"""
    n_accessable_rolls = 0
    search_space = (
        list(range(1, floor_layout.shape[0]-1)),
        list(range(1, floor_layout.shape[1]-1)),
    )
    for i in search_space[0]:
        for j in search_space[1]:
            if floor_layout[i, j] == 1:
                if number_of_rolls_in_grid(floor_layout[i-1:i+2,j-1:j+2]) < 5:
                    n_accessable_rolls += 1
    return n_accessable_rolls


# Part 1 script
def part_1_script():
    """My solution to day 4 part 1"""
    floor_layout = get_floor_layout(
        path="puzzle_inputs/day_4.txt",
        test=False
    )
    floor_layout = create_grid(floor_layout)

    print(f"The Number of accessable rolls is {find_accessible_rolls(floor_layout)}")


part_1_script()

