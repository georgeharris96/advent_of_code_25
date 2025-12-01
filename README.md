## 🎄 Advent of Code 2025 Solutions

This repository contains my personal solutions for the [Advent of Code 2025](https://adventofcode.com/2025) challenges. The solutions are implemented in **Python**, with **Poetry** used for environment and dependency management.

---

## ✨ Getting Started

### Prerequisites

You need **Python 3.13+** and **Poetry** installed to run these solutions.

1.  **Install Poetry:** Follow the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).
2.  **Install Dependencies:** Navigate to the root of this repository and run:
    ```bash
    poetry install
    ```

### Structure

The code is organized using a **flat file structure**, where each day's solution is a single Python file.

* `day_01.py` - Solution for Day 1
* `day_02.py` - Solution for Day 2
* ...
* `day_25.py` - Solution for Day 25
* `pyproject.toml` - Poetry configuration file

**Important Note on Inputs:**
The input files (`input_day_01.txt`, etc.) are not committed to this repository. You must download your personal input for each day from the Advent of Code website and place them in the root directory for the corresponding script to run successfully.

### Running a Solution

Use `poetry run python` followed by the filename:

```bash
# Example for running Day 5's solution
poetry run python day_05.py
