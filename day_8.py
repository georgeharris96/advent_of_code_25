######## Day 8 #########
from typing import List, Tuple 
import numpy as np
from itertools import combinations

def get_sample_input() -> List[str]:
    junction_box_coords = [
        "162,817,812\n",
        "57,618,57\n",
        "906,360,560\n",
        "592,479,940\n",
        "352,342,300\n",
        "466,668,158\n",
        "542,29,236\n",
        "431,825,988\n",
        "739,650,466\n",
        "52,470,668\n",
        "216,146,977\n",
        "819,987,18\n",
        "117,168,530\n",
        "805,96,715\n",
        "346,949,466\n",
        "970,615,88\n",
        "941,993,340\n",
        "862,61,35\n",
        "984,92,344\n",
        "425,690,689\n",
    ]
    return junction_box_coords


def get_junction_box_coords(path:str, test:bool = False) -> List[Tuple[int, int, int]]:
    if test: # Is this a test?....
        junction_box_coords = get_sample_input()
    else: # ... If not load the real sample set
        with open(path, "r") as file:
            junction_box_coords = file.readlines()
    
    # Reformat the junction box coordinates into a usable format
    junction_box_coords = [line.strip("\n").split(",") for line in junction_box_coords]

    reformated_coords = []
    for coordinate_set in junction_box_coords:
        reformated_set = []
        for coordinate in coordinate_set:
            reformated_set.append(int(coordinate))
        reformated_coords.append(tuple(reformated_set))

    return reformated_coords


def get_distances(junction_box_coords):
    distances = np.array(
        [
            (i, j, np.linalg.norm(junction_box_coords[i] - junction_box_coords[j])) for i, j in combinations(range(len(junction_box_coords)), 2)
        ],
        dtype=junction_box_coords.dtype,
    )
    distances = distances[np.argsort(distances[:, 2])]
    return distances


def limit_connections(distances, max_connections):
    return distances[:max_connections]


def create_circuits(coords, distances, max_connections):
    coords = np.c_[coords, -np.ones(len(coords), dtype=coords.dtype)]

    if max_connections:
        distances = distances[:max_connections]

    next_circuit = 0
    for i, j, distance in distances:
        box_1 = coords[i, 3]
        box_2 = coords[j, 3]
        if box_1 == box_2 == -1: # Are box 1 and box 2 assigned to a circuit yet?...
            # If not...
            coords[i, 3] = coords[j, 3] = next_circuit # ...Assign them to a circuit
            next_circuit +=1 # ...And increase the circuit indicator by 1

        elif box_2 == -1: # Is box 2 not assigned to a circuit?...
            coords[j, 3] = box_1 #... If so assign it to the same circuit as box 1

        elif box_1 == -1: # Is box 1 not assigned to a circuit?..
            coords[i, 3] = box_2 #... if so assign it to the same circuit as box 2
        
        elif box_1 != box_2: # Are box 1 and box 2 not assigned to the same circuit?
            coords[coords[:, 3] == box_2, 3] = box_1 #... if so join the two circuits

        if max_connections is None and np.unique(coords[:, 3]).size == 1:
            return coords[i, 0] * coords[j, 0]

    return np.prod(np.sort(np.unique_counts(coords[:, 3][coords[:, 3] >= 0]).counts)[-3:])


def part_1_script():
    junction_box_coords = np.array(
        get_junction_box_coords(
            path="puzzle_inputs/day_8.txt",
            test=False
        ), 
        np.int64
        )

    distances = get_distances(junction_box_coords)
    max_connections = 1000
    number_of_circuits = create_circuits(
        junction_box_coords,
        distances,
        max_connections,
    )
    print(f"There are a total of {number_of_circuits} after {max_connections} of connections")


def part_2_script():
    junction_box_coords = np.array(
        get_junction_box_coords(
            path="puzzle_inputs/day_8.txt",
            test=False
        ), 
        np.int64
        )

    distances = get_distances(junction_box_coords)
    max_connections = None
    number_of_circuits = create_circuits(
        junction_box_coords,
        distances,
        max_connections,
    )
    print(f"There are a total of {number_of_circuits} of circuits")


part_1_script()
part_2_script()

