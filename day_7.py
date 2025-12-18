######## Day 6 #########
from typing import List, Tuple
import itertools
import collections

def get_sample_manifold() -> List[str]:
    """Returns the sample manifold in the same format as the real input"""
    manifold = [
        ".......S.......\n",
        "...............\n",
        ".......^.......\n",
        "...............\n",
        "......^.^......\n",
        "...............\n",
        ".....^.^.^.....\n",
        "...............\n",
        "....^.^...^....\n",
        "...............\n",
        "...^.^...^.^...\n",
        "...............\n",
        "..^...^.....^..\n",
        "...............\n",
        ".^.^.^.^.^...^.\n",
        "...............\n",
    ]
    return manifold

def get_manifold(path:str, test:bool) -> List[str]:
    """Returns either the sample or real manifold"""
    if test:
        manifold = get_sample_manifold()
    else:
        with open(path, "r") as file:
            manifold = file.readlines()
    
    manifold = [layer.strip("\n") for layer in manifold]
    return manifold


def turn_on_classical_beams(manifold:List[str]) -> Tuple[List[str], int]:
    """Takes a manifold and turns on a classical tachyon beam"""
    source_loc = manifold[0].index("S")
    edited_manifold = [manifold[0]]
    beam_locs = [source_loc]
    number_of_splits = 0

    for layer in manifold[1:]:
        edited_layer = list(layer)
        locs_to_remove = []
        for loc in beam_locs:
            if edited_layer[loc] == ".":
                edited_layer[loc] = "|"
            
            if edited_layer[loc] == "^":
                edited_layer[loc-1], edited_layer[loc+1] = "|", "|"

                if loc-1 not in beam_locs:
                    beam_locs.append(loc-1)
                if loc+1 not in beam_locs:
                    beam_locs.append(loc+1)

                number_of_splits += 1
                locs_to_remove.append(loc)

        for loc in locs_to_remove:
            beam_locs.remove(loc)

        edited_manifold.append("".join(edited_layer))
    return edited_manifold, number_of_splits

def turn_on_quantum_beams(manifold:List[str]) -> Tuple[List[str], int]:
    """Takes a manifold and turns on the a quantum tachyon beam"""
    tachyons = collections.defaultdict(int)
    tachyons[manifold[0].find("S")] += 1

    for layer in manifold:
        for i, symbol in enumerate(layer):

            if symbol == "^" and i in tachyons.keys():
                tachyons[i-1] += tachyons[i]
                tachyons[i+1] += tachyons[i]
                tachyons[i] = 0
    return tachyons

# Part 1 script
def part_1_script():
    """My solution to part 1"""
    manifold = get_manifold(
        path="puzzle_inputs/day_7.txt",
        test=False
    )

    manifold, n_splits = turn_on_classical_beams(manifold)

    print(f"The tachyon beam is split a total of {n_splits} times")


def part_2_script():
    """My solution to part 2"""
    manifold = get_manifold(
        path="puzzle_inputs/day_7.txt",
        test=False
    )

    possible_beam_locations = turn_on_quantum_beams(manifold)
    print(f"The number of possible paths is {sum(possible_beam_locations.values())}")


part_1_script()
part_2_script()