######## Day 9 #########
import numpy as np
from itertools import combinations


def get_sample_layout():
    tile_layout = [
        "7,1\n",
        "11,1\n",
        "11,7\n",
        "9,7\n",
        "9,5\n",
        "2,5\n",
        "2,3\n",
        "7,3\n",
    ]
    return tile_layout


def get_tile_layout(path:str, test:bool=False):
    if test:
        tile_layout = get_sample_layout()
    else:
        with open(path, "r") as file:
            tile_layout = file.readlines()
    
    tile_layout = [line.strip("\n").split(",") for line in tile_layout]

    reformated_layout = []
    for tile in tile_layout:
        reformated_tile = []
        for coord in tile:
            reformated_tile.append(int(coord))
        reformated_layout.append(tuple(reformated_tile))
    return reformated_layout


def calculate_areas(tile_layout):
    tile_combinations = np.array(
        [(i, j) for i, j in combinations(range(len(tile_layout)), 2)]
    )
    tile_combinations = np.c_[tile_combinations, -np.ones(len(tile_combinations), dtype=tile_combinations.dtype)]

    for combination in tile_combinations:
        tile_1, tile_2 = tile_layout[combination[0]], tile_layout[combination[1]]
        combination[2] = np.prod(np.abs(tile_1-tile_2)+1)
    return tile_combinations


def part_1_script():
    tile_layout = np.array(
        get_tile_layout(
            path="puzzle_inputs/day_9.txt",
            test=False,
        ),
        dtype=np.int64
    )

    tile_areas = calculate_areas(tile_layout)
    tile_areas = tile_areas[np.argsort(tile_areas[:, 2])][::-1]

    largest_area = tile_areas[0]

    print(f"The Largest area is {largest_area[2]}")
part_1_script()




        