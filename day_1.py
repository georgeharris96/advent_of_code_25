######### Part 1 #########
# Set up dial
class Dial:
    def __init__(self):
        self.current = 50
        self.high = 99
        self.low = 0
        self.times_touched_zero = 0

    def move_right(self):
        self.current += 1
        if self.current > self.high:
            self.current = 0
    
    def move_left(self):
        self.current -= 1
        if self.current < self.low:
            self.current = 99

# Import puzzle input
def import_puzzle_input(filepath: str):
    with open(filepath) as f:
        input = f.readlines()
        input = [x.strip("\n") for x in input]
    return input


# Process instruction
def process_instruction(instruction: str):
    direction = instruction[0]
    places = int(instruction[1:])
    return direction, places


# Check if dial has touched zero
def check_dial(dial: Dial):
    if dial.current == 0:
        dial.times_touched_zero +=1
    else:
        pass


# Move the dial
def move_dial(dial: Dial, direction: str, places: int):
    if direction == "L":
        for _ in range(places):
            dial.move_left()
            check_dial(dial)
    
    else:
        for _ in range(places):
            dial.move_right()
            check_dial(dial)


def part_1_script():
    puzzle_input = import_puzzle_input("puzzle_inputs/day_1.txt")
    # puzzle_input = [
    #     "L68", "L30", "R48", 
    #     "L5", "R60", "L55", 
    #     "L1", "L99", "R14", 
    #     "L82"
    #     ]
    dial = Dial()
    times_at_zero = 0

    for instruction in puzzle_input:
        direction, places = process_instruction(instruction)
        move_dial(dial, direction, places)

        if dial.current == 0:
            times_at_zero += 1
        
    print(times_at_zero)

def part_2_script():
    puzzle_input = import_puzzle_input("puzzle_inputs/day_1.txt")
    dial = Dial()

    for instruction in puzzle_input:
        direction, places = process_instruction(instruction)
        move_dial(dial, direction, places)

    print(dial.times_touched_zero)

part_1_script()
part_2_script()

