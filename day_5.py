######## Day 5 #########
from typing import List

# Get id ranges and inventory
def get_sample_input() -> List[str]:
    """Returns the sample from the problem statement in the same form as the regular input"""
    sample_inventory_and_ids = [
        "3-5",
        "10-14",
        "16-20",
        "12-18",
        "",
        "1",
        "5",
        "8",
        "11",
        "17",
        "32",
    ]
    return sample_inventory_and_ids


def get_inventory_and_ids(path:str, test:bool = False):
    """Retrieves either the sample or real input"""
    if test: # Is it a test?..
        inventory_and_ids = get_sample_input()
    else: # ..or not?
        with open(path) as f:
            inventory_and_ids = f.readlines()
    inventory_and_ids = [line.strip("\n") for line in inventory_and_ids]
    return [line for line in inventory_and_ids if "-" in line], [line for line in inventory_and_ids if "-" not in line][1:]


# Unpack Id range
def unpack_id_range(id_range: str) -> List[int]:
    """Takes an id range and outputs a tuple of the high and low values"""
    split_id_range = [int(x) for x in id_range.split("-")]
    return [split_id_range[0], split_id_range[1]]


# Check if item is fresh
def is_fresh(item:int, id_ranges:List[List[int]]):
    """Checks if an item is contained in any of the fresh item ranges"""
    fresh_status = False
    for id_range in id_ranges:
        if item >= id_range[0] and item <= id_range[1]:
            fresh_status = True
    return fresh_status


# Find number of fresh ingredients
def find_number_of_fresh_ingredients(id_ranges:List[List[int]]):
    values:List[int] = []
    for id_range in id_ranges:
        values += id_range
    values = sorted(set(values))
    func = lambda x: any(r0 <= x <= r1 for r0, r1 in id_ranges)
    
    counter = 0
    for i in range(len(values)-1):
        inter_val = (values[i+1] + values[i]) // 2
        n_between = values[i+1] - values[i]-1
        counter += func(inter_val)*n_between
    return counter+len(values)


# Part 1 script
def part_1_script():
    """My solution to day 5 part 1"""
    fresh_ingredient_ranges, inventory = get_inventory_and_ids(
        path="puzzle_inputs/day_5.txt",
        test=False
    )

    unpacked_fresh_ingredient_ranges:List[List[int]] = [unpack_id_range(x) for x in fresh_ingredient_ranges]

    number_of_fresh_items = 0
    for item in inventory:
        if is_fresh(int(item), unpacked_fresh_ingredient_ranges):
            number_of_fresh_items += 1

    print(f"The number of fresh items is {number_of_fresh_items}")


# Part 2 script
def part_2_script():
    """My solution to day 5 part 2"""
    fresh_ingredient_ranges, _ = get_inventory_and_ids(
        path="puzzle_inputs/day_5.txt",
        test=False
    )
    fresh_ingredient_ranges = [unpack_id_range(x) for x in fresh_ingredient_ranges]

    total_number_of_fresh_ingredients = find_number_of_fresh_ingredients(fresh_ingredient_ranges)
    print(f"The total number of fresh ingredients is {total_number_of_fresh_ingredients}")

part_1_script()
part_2_script()
