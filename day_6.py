######## Day 6 #########
from typing import List
import numpy as np

# Get homework
def get_sample_homework() -> List[str]:
    sample_homework = [
    "123 328  51  64\n",
    " 45 64  387  23\n",
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


part_1_script()