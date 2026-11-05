<div align="center">

# A-Maze-ing

This project has been created as part of the 42 curriculum by jzampier, pezio

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Style: flake8](https://img.shields.io/badge/code%20style-flake8-green.svg)](https://flake8.pyflake.org/)
[![Typing: mypy](https://img.shields.io/badge/typing-mypy-orange.svg)](https://mypy-lang.org/)
[![Curriculum](https://img.shields.io/badge/42-Project-black.svg)](https://42.fr)

</div>

---

## About

**A-Maze-ing** is a robust maze generator and solver developed as part of the 42 curriculum. The project combines computer science, graph theory, and algorithmic design to generate customized, randomized mazes from configuration files, solve them, and output both machine-readable hexadecimal representations and visual ASCII/graphical renders.

Whether you're creating a **perfect maze** (spanning trees with a unique path between any two points) or a **Pac-Man style board** (featuring multiple loops, open centers, ghost corners, and the iconic `42` pattern), A-Maze-ing brings structure out of chaos.

---

## Features

- **Configurable Generation**: Fully customized dimensions, entry/exit points, and generation modes via simple configuration files.
- **Dual Maze Modes**:
  - **Perfect Mazes (`PERFECT=True`)**: Exactly one unique path between entry and exit (no loops).
  - **Pac-Man Style (`PERFECT=False`)**: Fully reachable corridors, multiple loops, open 2x2/3x2 zones, ghost/super-pellet corners, and minimal dead ends.
- **Hexadecimal Wall Encoding**: Encodes cardinal walls (North, East, South, West) into compact hex digits per cell.
- **Shortest Path Solver**: Computes and exports the optimal shortest route (`N`, `E`, `S`, `W`) from entry to exit.
- **Visual Rendering**: Clear terminal/ASCII visualization showing walls, start, end, and solution path.
- **Production-Grade Quality**: Strict adherence to Python type hints (`mypy` compliant) and PEP 8 style guidelines (`flake8`).

---

## Project Structure

```text
.
├── a_maze_ing/
│   ├── __init__.py
│   └── a_maze_ing.py        # Main execution script
├── Makefile                 # Automation rules (install, run, lint, clean)
├── README.md                # Project documentation
├── requirements.txt         # Project dependencies
├── en.subject.pdf           # Official project subject (English)
├── pt.subject.md            # Official project subject (Portuguese Markdown)
└── pt.subject.pdf           # Official project subject (Portuguese PDF)
```

---

## Getting Started

### Prerequisites

- **Python 3.10** or higher
- `make` utility

### Installation

Clone the repository and set up the environment using the provided `Makefile`:

```bash
# 1. Create virtual environment and install development tools (flake8, mypy)
make

# 2. Install project dependencies from requirements.txt
make install
```

---

## Usage

Run the main program with a configuration file:

```bash
python3 a_maze_ing/a_maze_ing.py config.txt
```

Alternatively, use the Makefile shortcut:
```bash
make run
```

To run with interactive debugging (`pdb`):
```bash
make debug
```

---

## Configuration Format (`config.txt`)

Configuration files use simple `KEY=VALUE` pairs. Lines starting with `#` are treated as comments.

| Key | Description | Example |
| :--- | :--- | :--- |
| `WIDTH` | Maze width (number of columns) | `WIDTH=20` |
| `HEIGHT` | Maze height (number of rows) | `HEIGHT=15` |
| `ENTRY` | Entry coordinates `(x,y)` | `ENTRY=0,0` |
| `EXIT` | Exit coordinates `(x,y)` | `EXIT=19,14` |
| `OUTPUT_FILE` | Target output file path | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Generate a perfect maze (True/False) | `PERFECT=True` |

---

## Output Format (`maze.txt`)

The generated output file encodes each cell's walls as a single hexadecimal digit (0–F) based on a 4-bit bitmask:

| Bit | Direction | Binary Value |
| :---: | :---: | :---: |
| 0 (LSB) | North | `0001` (1) |
| 1 | East | `0010` (2) |
| 2 | South | `0100` (4) |
| 3 (MSB) | West | `1000` (8) |

*(Example: `3` means South and West walls are closed; `A` means East and West walls are closed).*

Following the grid lines and a blank line, the file outputs:
1. Entry coordinates
2. Exit coordinates
3. Shortest path sequence using directions (`N`, `E`, `S`, `W`)

---

## Code Quality & Linting

To ensure codebase integrity and type safety, run the strict verification checks:

```bash
# Run standard linting (flake8 + mypy)
make lint

# Run strict type checking
make lint-strict
```

To clean up build artifacts, caches, and virtual environments:
```bash
make clean
```
