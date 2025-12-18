######## Day 6 #########
from typing import List
import numpy as np

# Get homework
def get_sample_homework() -> List[str]:
    sample_homework = [
    "123 328  51 64 \n",
    " 45 64  387 23 \n",
    "  6 98  215 314\n",
    "*   +   *   +\n",
    ]
    return sample_homework


def get_homework(path:str, test:bool = False) -> List[str]:
    if test:
        homework = get_sample_homework()
    else:
        with open(path, "r") as file:
            homework = file.readlines()
    
    homework = [line.strip("\n") for line in homework]
    return homework

def reformat_homework_numbers(homework_numbers:List[str]): # type: ignore
    homework_numbers:List[List[str]] = [line.split() for line in homework_numbers]
    reformed_homework_numbers:List[List[int]] = []
    for row in homework_numbers:
        reformed_homework_numbers.append([int(element) for element in row])
    return reformed_homework_numbers


# Part 1 script
def part_1_script():
    homework = get_homework(
        path="puzzle_inputs/day_6.txt",
        test=False,
    )
    homework_numbers, homework_operands = homework[:-1], homework[-1]
    
    homework_numbers = np.array(reformat_homework_numbers(homework_numbers))
    homework_operands = homework_operands.split()

    columns = homework_numbers.shape[1]

    answers:List[int] = []
    for i in range(columns):
        if homework_operands[i] == "+":
            answers.append(int(np.sum(homework_numbers[:,i])))
        if homework_operands[i] == "*":
            answers.append(int(np.prod(homework_numbers[:,i])))
    
    print(f"The grand total of all the answers is {sum(answers)}")

def part_2_script():
    homework = get_homework(
        path="puzzle_inputs/day_6.txt",
        test=False, # Set to True to verify against the example
    )
    
    number_lines = homework[:-1]
    operator_line = homework[-1]

    max_width = max(len(line) for line in number_lines)
    max_width = max(max_width, len(operator_line))
    
    padded_numbers = [line.ljust(max_width) for line in number_lines]
    padded_operator_line = operator_line.ljust(max_width)
    
    blocks = []
    in_block = False
    block_start = 0
    
    all_lines = padded_numbers + [padded_operator_line]
    
    for col in range(max_width):
        is_empty = all(line[col] == " " for line in all_lines)
        
        if not is_empty:
            if not in_block:
                in_block = True
                block_start = col
        else:
            if in_block:
                in_block = False
                blocks.append((block_start, col))
    
    if in_block:
        blocks.append((block_start, max_width))

    grand_total = 0
    
    for start, end in blocks:
        op_segment = padded_operator_line[start:end].strip()
        operator = op_segment
        
        current_block_numbers = []
        
        for col in range(end - 1, start - 1, -1):
            col_str = ""
            for row in padded_numbers:
                col_str += row[col]
            
            clean_str = col_str.replace(" ", "")
            
            if clean_str:
                current_block_numbers.append(int(clean_str))
        
        if not current_block_numbers:
            continue
            
        block_answer = current_block_numbers[0]
        for num in current_block_numbers[1:]:
            if operator == "+":
                block_answer += num
            elif operator == "*":
                block_answer *= num
        
        grand_total += block_answer

    print(f"Part 2 Grand Total: {grand_total}")


part_1_script()
part_2_script()

