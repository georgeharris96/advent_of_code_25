######### Day 1 #########
# Set up dial
class Dial:
    def __init__(self):
        self.current = 50
        self.high = 99
        self.low = 0
        self.times_touched_zero = 0

    def move_right(self):
        """Moves the dial to the right
        
        This moves the dial to the right and checks if it is over the maximum of the dial. If it is then it reverts back to the start
        """
        self.current += 1
        if self.current > self.high:
            self.current = 0
    
    def move_left(self):
        """Moves the dial to the left
        
        This moves the dial to the left and checks if it is below the minimum of the dial. If it is then it reverts back to the end
        """
        self.current -= 1
        if self.current < self.low:
            self.current = 99


# Import puzzle input
def import_puzzle_input(filepath: str):
    """Function which loads the puzzle input and removes other junk"""
    with open(filepath) as f:
        input = f.readlines()
        input = [x.strip("\n") for x in input]
    return input


# Process instruction
def process_instruction(instruction: str):
    """Takes a instruction from the puzzle input and extracts the direction and number of places the dial has to move"""
    direction = instruction[0]
    places = int(instruction[1:])
    return direction, places


# Check if dial has touched zero
def check_dial(dial: Dial):
    """Checks if the dial is currently at zero and if so move the tracker up one place"""
    if dial.current == 0:
        dial.times_touched_zero +=1
    else:
        pass


# Move the dial
def move_dial(dial: Dial, direction: str, places: int):
    """Depending on the direction it moves the dial a certain number of places"""
    if direction == "L":
        for _ in range(places):
            dial.move_left()
            check_dial(dial)
    
    else:
        for _ in range(places):
            dial.move_right()
            check_dial(dial)


def part_1_script():
    """The script which will output the number of times the dial stops on the zero mark"""
    puzzle_input = import_puzzle_input("puzzle_inputs/day_1.txt")
    dial = Dial()
    times_at_zero = 0

    for instruction in puzzle_input:
        direction, places = process_instruction(instruction)
        move_dial(dial, direction, places)

        if dial.current == 0:
            times_at_zero += 1
        
    print(f"The dial stopped at zero {times_at_zero} times")

def part_2_script():
    """The script which will output the number of times the dial passes the zero mark"""
    puzzle_input = import_puzzle_input("puzzle_inputs/day_1.txt")
    dial = Dial()

    for instruction in puzzle_input:
        direction, places = process_instruction(instruction)
        move_dial(dial, direction, places)

    print(f"The dial passed the zero mark {dial.times_touched_zero} times")

part_1_script()
part_2_script()

