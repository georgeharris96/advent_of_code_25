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


def calculate_area(tile_1, tile_2):
    return np.prod(np.abs(tile_1-tile_2)+1)


def generate_tile_pairs(tile_layout):
    tile_combinations = np.array([(i, j) for i, j in combinations(range(len(tile_layout)), 2)])
    return np.c_[tile_combinations, -np.ones(len(tile_combinations), dtype=tile_combinations.dtype)]


def is_inside_polygon(point, polygon):
    px, py = point
    is_in = False
    n = len(polygon)

    for i in range(n):
        a = polygon[i]
        b = polygon[(i+1) % n]

        if ((a[1] > py) != (b[1] > py)):
            intersect_x = a[0] + (py - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if px < intersect_x:
                is_in = not is_in
    return is_in


def is_on_boundary(point, polygon, tolerance=1e-9):
    n = len(polygon)

    for i in range(n):
        a = polygon[i]
        b = polygon[(i+1) % n]

        cross_product = (point[1] - a[1]) * (b[0] - a[0]) - (point[0] - a[0]) * (b[1] - a[1])

        if abs(cross_product) <= tolerance:
            if (min(a[0], b[0]) - tolerance <= point[0] <= max(a[0], b[0]) + tolerance) and \
               (min(a[1], b[1]) - tolerance <= point[1] <= max(a[1], b[1]) + tolerance):
                return True
    return False


def part_1_script():
    tile_layout = np.array(
        get_tile_layout(
            path="puzzle_inputs/day_9.txt",
            test=False,
        ),
        dtype=np.int64
    )

    tile_combinations = generate_tile_pairs(tile_layout)

    for combination in tile_combinations:
        tile_1, tile_2 = tile_layout[combination[0]], tile_layout[combination[1]]
        combination[2] = calculate_area(tile_1, tile_2)

    tile_combinations = tile_combinations[np.argsort(tile_combinations[:, 2])][::-1]

    largest_area = tile_combinations[0]

    print(f"The largest area between two red tile locations is {largest_area[2]}")


def part_2_script():
    red_tile_layout = np.array(
        get_tile_layout(
            path="puzzle_inputs/day_9.txt",
            test=False,
        ),
        dtype=np.int64
    )

    red_tile_pairs = generate_tile_pairs(red_tile_layout)

    for tile_pair in red_tile_pairs:
        point_a, point_b = red_tile_layout[tile_pair[0]], red_tile_layout[tile_pair[1]]
        
        # Get bounds for the candidate rectangle
        x_min, x_max = sorted([point_a[0], point_b[0]])
        y_min, y_max = sorted([point_a[1], point_b[1]])

        # 1. Corner Check (Your existing logic)
        point_x, point_y = np.array([point_b[0], point_a[1]]), np.array([point_a[0], point_b[1]])
        all_corners = [point_a, point_b, point_x, point_y]
        
        is_valid_area = True
        for point in all_corners:
            if not (is_inside_polygon(point, red_tile_layout) or is_on_boundary(point, red_tile_layout)):
                is_valid_area = False
                break
        
        if not is_valid_area:
            continue

        # 2. Midpoint Check: Prevents bridging over external gaps
        mid_point = np.array([(x_min + x_max) / 2, (y_min + y_max) / 2])
        if not is_inside_polygon(mid_point, red_tile_layout):
            is_valid_area = False
            continue

        # 3. Edge Intersection Check: Ensure no polygon boundary cuts through the rectangle
        # Since the polygon is made of rectangles, we only check vertical/horizontal segments
        n = len(red_tile_layout)
        for i in range(n):
            p1 = red_tile_layout[i]
            p2 = red_tile_layout[(i + 1) % n]
            
            # Check if a vertical polygon edge passes through the rectangle's horizontal span
            if p1[0] == p2[0]: # Vertical edge
                if x_min < p1[0] < x_max:
                    if max(p1[1], p2[1]) > y_min and min(p1[1], p2[1]) < y_max:
                        is_valid_area = False
                        break
            # Check if a horizontal polygon edge passes through the rectangle's vertical span
            else: # Horizontal edge
                if y_min < p1[1] < y_max:
                    if max(p1[0], p2[0]) > x_min and min(p1[0], p2[0]) < x_max:
                        is_valid_area = False
                        break
        
        if is_valid_area:
            tile_pair[2] = calculate_area(point_a, point_b)

    # Filter and sort
    red_tile_pairs = red_tile_pairs[red_tile_pairs[:, 2] != -1]
    red_tile_pairs = red_tile_pairs[np.argsort(red_tile_pairs[:, 2])][::-1]
    
    print(f"The largest area made up of red and green tiles is {red_tile_pairs[0, 2]}")


part_1_script()
part_2_script()

