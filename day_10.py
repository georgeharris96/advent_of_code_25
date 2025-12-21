######## Day 10 #########
from scipy.optimize import milp, LinearConstraint, Bounds
import numpy as np
import itertools

def get_sample_input():
    puzzle_input = [
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}\n",
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}\n",
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}\n",
    ]
    return puzzle_input


def get_manual_information(path:str, test=False):
    if test:
        manual_info = get_sample_input()
    else:
        with open(path, "r") as file:
            manual_info = file.readlines()

    manual_info = [line.strip("\n").split(" ") for line in manual_info]
    
    indicator_lights = []
    button_wiring_schematics = []
    joltage_requirements = []
    for line in manual_info:
        button_wiring_schematic = []
        for item in line:
            if item.startswith("["):
                fixed_item = item.strip("[").strip("]")
                indicator_lights.append(fixed_item)
            if item.startswith("("):
                fixed_item = item.strip("(").strip(")").split(",")
                button_wiring_schematic.append([int(x) for x in fixed_item])
            if item.startswith("{"):
                joltage_requirements.append(item)
        button_wiring_schematics.append(button_wiring_schematic)
    return indicator_lights, button_wiring_schematics, joltage_requirements


def create_light_array(lights:str):
    light_array = np.zeros(shape=(len(lights)))
    for idx, light in enumerate(lights):
        if light == "#":
            light_array[idx] = 1
        else:
            light_array[idx] = 0
    return light_array


def create_schematic_grid(schematic:list, target:np.ndarray):
    grid_schematic = np.c_[np.zeros((len(target), len(schematic)), dtype=int), target.T.astype(int)]
    for i, item in enumerate(schematic):
        for light in item:
            grid_schematic[int(light), i] = 1
    return grid_schematic


def create_counter(joltage_requirement:str):
    joltage_requirement = joltage_requirement.strip("{").strip("}")
    return np.array([int(joltage) for joltage in joltage_requirement.split(",")])


def gaussian_elimination(grid_schematic:np.ndarray):
    rows, cols = grid_schematic.shape
    pivot_row = 0
    pivot_cols = []
    result = np.zeros(shape=grid_schematic.shape[1])

    for col in range(cols -1):
        if pivot_row >= rows:
            break

        column_segment = grid_schematic[pivot_row:, col]
        if np.max(column_segment) == 0:
            continue

        found_row_index = pivot_row + np.argmax(column_segment)

        grid_schematic[[pivot_row, found_row_index]] = grid_schematic[[found_row_index, pivot_row]]

        for r in range(rows):
            if r != pivot_row and grid_schematic[r, col] == 1:
                grid_schematic[r] ^= grid_schematic[pivot_row]
        
        pivot_cols.append(col)
        pivot_row += 1
    return grid_schematic, pivot_cols


def gaussian_elimination_real(grid_schematic: np.ndarray):
    grid_schematic = grid_schematic.astype(float)
    
    rows, cols = grid_schematic.shape
    pivot_row = 0
    pivot_cols = []

    for col in range(cols - 1):
        if pivot_row >= rows:
            break

        column_segment = grid_schematic[pivot_row:, col]
        if np.all(np.isclose(column_segment, 0)):
            continue

        found_row_index = pivot_row + np.argmax(np.abs(column_segment))
        grid_schematic[[pivot_row, found_row_index]] = grid_schematic[[found_row_index, pivot_row]]

        pivot_val = grid_schematic[pivot_row, col]
        grid_schematic[pivot_row] /= pivot_val

        for r in range(rows):
            if r != pivot_row:
                factor = grid_schematic[r, col]
                if not np.isclose(factor, 0):
                    grid_schematic[r] -= factor * grid_schematic[pivot_row]

        pivot_cols.append(col)
        pivot_row += 1
        
    return grid_schematic, pivot_cols


def solve_from_reduced_grid(grid, pivot_cols):
    rows, total_cols = grid.shape
    num_buttons = total_cols - 1

    free_cols = [c for c in range(num_buttons) if c not in pivot_cols]
    
    min_presses = float('inf')
    
    for free_vals in itertools.product([0, 1], repeat=len(free_cols)):
        presses = np.zeros(num_buttons, dtype=int)
        
        for i, col_idx in enumerate(free_cols):
            presses[col_idx] = free_vals[i]
            
        possible = True
        
        for r in range(rows):
            target_val = grid[r, -1]
            
            current_row_impact = np.sum(grid[r, :num_buttons] * presses) % 2

            pivot_c = -1
            for c in range(num_buttons):
                if grid[r, c] == 1 and c in pivot_cols:
                    pivot_c = c
                    break
            
            if pivot_c != -1:
                required_val = (target_val + current_row_impact) % 2

                if presses[pivot_c] == 0: 
                     presses[pivot_c] = required_val
                elif presses[pivot_c] != required_val:
                    possible = False
                    break
            else:
                if current_row_impact != target_val:
                    possible = False
                    break
        
        if possible:
            total_presses = np.sum(presses)
            if total_presses < min_presses:
                min_presses = total_presses

    if min_presses == float('inf'):
        return 0
    return min_presses


def solve_part2(grid, pivot_cols):
    rows, cols = grid.shape
    num_buttons = cols - 1 # Last col is target
    
    free_cols = [c for c in range(num_buttons) if c not in pivot_cols]
    
    min_presses = float('inf')
    
    search_range = range(100) 
    
    for free_vals in itertools.product(search_range, repeat=len(free_cols)):
        presses = np.zeros(num_buttons, dtype=int)
        
        for i, f_col in enumerate(free_cols):
            presses[f_col] = free_vals[i]
            
        valid = True
        
        for r in range(len(pivot_cols)):
            p_col = pivot_cols[r]
            
            rhs = grid[r, -1]
        
            lhs_free = np.dot(grid[r, free_cols], presses[free_cols])
            
            required_val = rhs - lhs_free

            if required_val < -1e-5 or not np.isclose(required_val, np.round(required_val)):
                valid = False
                break
            
            presses[p_col] = int(np.round(required_val))
            
        if valid:
            for r in range(len(pivot_cols), rows):
                lhs = np.dot(grid[r, :num_buttons], presses)
                if not np.isclose(lhs, grid[r, -1]):
                    valid = False
                    break
        
        if valid:
            total = np.sum(presses)
            if total < min_presses:
                min_presses = total
                
    return min_presses if min_presses != float('inf') else 0

def solve_with_milp(grid_schematic):
    A = grid_schematic[:, :-1]
    b = grid_schematic[:, -1]
    
    num_vars = A.shape[1]
    
    c = np.ones(num_vars)
    
    constraints = LinearConstraint(A, b, b)
    integrality = np.ones(num_vars)
    
    bounds = Bounds(lb=0, ub=np.inf)
    
    res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)
    
    if res.success:
        presses = np.round(res.x).astype(int)
        if np.all(A @ presses == b):
            return int(np.sum(presses))

    return 0


def part_1_script():
    indictator_lights, button_wiring_schematics, _ = get_manual_information(
        path="puzzle_inputs/day_10.txt",
        test=False,
    )

    button_presses = 0
    for lights, schematic in zip(indictator_lights, button_wiring_schematics):
        light_array = create_light_array(lights)
        grid_schematic = create_schematic_grid(schematic, light_array)
        grid_schematic, pivot_cols = gaussian_elimination(grid_schematic)

        answer = solve_from_reduced_grid(grid_schematic, pivot_cols)
        button_presses += answer

    print(f"The fewest number of indicator lights is {button_presses} ")


def part_2_script():
    _, button_wiring_schematics, joltage_requirements = get_manual_information(
        path="puzzle_inputs/day_10.txt",
        test=False
    )
    
    total_presses_all_machines = 0
    for joltages, schematic in zip(joltage_requirements, button_wiring_schematics):
        joltages = create_counter(joltages)
        # Create the grid as before
        grid_schematic = create_schematic_grid(schematic, joltages)
        
        # OLD WAY:
        # grid_schematic, pivot_cols = gaussian_elimination_real(grid_schematic)
        # machine_total = solve_part2(grid_schematic, pivot_cols)
        
        # NEW WAY:
        machine_total = solve_with_milp(grid_schematic)
        
        if machine_total > 0:
            total_presses_all_machines += machine_total

    print(f"Final Answer: {total_presses_all_machines}")

part_1_script()
part_2_script()


