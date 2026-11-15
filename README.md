*This project has been created as part of the 42 curriculum by jzampier, pezio.*

<div align="center">

# A-Maze-ing

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Style: flake8](https://img.shields.io/badge/code%20style-flake8-green.svg)](https://flake8.pyflake.org/)
[![Typing: mypy](https://img.shields.io/badge/typing-mypy-orange.svg)](https://mypy-lang.org/)
[![Curriculum](https://img.shields.io/badge/42-Project-black.svg)](https://42.fr)

</div>

---

## Description

**A-Maze-ing** is a robust, modular maze generator, solver, and visualizer developed as part of the 42 curriculum. The project combines graph theory, algorithmic design, and software engineering best practices to generate customized, randomized mazes from configuration files, solve them using optimal pathfinding, and output both machine-readable hexadecimal representations and rich visual renders.

The primary goal of A-Maze-ing is to explore foundational graph traversal algorithms, parse structured configuration files robustly, handle custom exceptions gracefully, and provide dual operational modes:
1. **Perfect Mazes (`PERFECT=True`)**: Spanning trees featuring exactly one unique path between any two points (no loops or cycles).
2. **Pac-Man Style Mazes (`PERFECT=False`)**: Multi-path mazes featuring loops, open central zones, ghost/super-pellet corners, and minimal dead ends.

---

## Features & Advanced Features

- **Configurable Generation**: Fully customizable dimensions, entry/exit coordinates, output file paths, and generation mode via clean `config.txt` files.
- **Embedded 42 Logo Pattern**: Automatically embeds a centered, closed-cell `42` structural pattern into the maze layout when dimensions allow.
- **Hexadecimal Wall Encoding**: Encodes cardinal walls (North=1, East=2, South=4, West=8) into compact hexadecimal digits (0–F) per cell.
- **Shortest Path Solver (BFS)**: Computes and exports the optimal shortest route (`N`, `E`, `S`, `W`) from entry to exit.
- **Dual Visualizers**:
  - **Terminal User Interface (TUI)**: Interactive or static ASCII/Unicode grid rendering in the terminal.
  - **Graphical Window**: Visual window renderer for graphical inspection.
- **Production-Grade Quality**: Strict adherence to Python type hints (`mypy` strict compliant) and PEP 8 style guidelines (`flake8`).

---

## Project Structure

```text
.
├── a_maze_ing.py                   # Main execution entrypoint (python3 a_maze_ing.py config.txt)
├── mazegen.py                      # Reusable, standalone maze generation module (pip package)
├── a_maze_ing/
│   ├── __init__.py
│   ├── a_maze_ing.py              # Application main(): wiring and error handling
│   ├── controller/
│   │   ├── __init__.py
│   │   └── menu_controller.py    # Menu & interaction controller
│   ├── maze_interpretor/
│   │   ├── __init__.py
│   │   └── maze_generator.py     # Adapter: "42" pattern + output file writer
│   ├── parse/
│   │   ├── __init__.py
│   │   ├── config_interpretor.py # Configuration lexer and file interpreter
│   │   ├── exceptions_parser.py  # Custom parser and validation exceptions
│   │   └── parser.py             # Configuration validation and schema parsing
│   └── visualizer/
│       ├── __init__.py
│       ├── tui.py                # Terminal User Interface (TUI) renderer
│       └── window.py             # Graphical window renderer
├── .gitignore                    # Git ignore rules
├── config.txt                    # Default configuration file example
├── LICENSE.md                    # Project license
├── Makefile                      # Automation rules (install, run, package, lint)
├── pyproject.toml                # mazegen package build configuration
└── README.md                     # Project documentation
```

---

## Instructions

### Prerequisites

- **Python 3.10** or higher
- `make` utility

### Installation & Setup

Clone the repository and set up the development environment using the provided `Makefile`:

```bash
# 1. Initialize virtual environment and development tools
make

# 2. Install project dependencies
make install
```

### Execution

Run the main program with your configuration file:

```bash
make run config.txt
```

Alternatively, run directly via Python (as required by the subject):

```bash
python3 a_maze_ing.py config.txt
```

To run with interactive debugging (`pdb`):
```bash
make debug config.txt
```

### Build the Reusable Package

Build the `mazegen` pip package (`.whl` is copied to the repository root):

```bash
make package
```

---

## Configuration Format (`config.txt`)

Configuration files use simple `KEY=VALUE` format. Blank lines and lines starting with `#` are ignored as comments.

| Key | Description | Expected Type | Example |
| :--- | :--- | :--- | :--- |
| `WIDTH` | Maze width (number of columns) | Integer (`int`) | `WIDTH=20` |
| `HEIGHT` | Maze height (number of rows) | Integer (`int`) | `HEIGHT=15` |
| `ENTRY` | Entry coordinates `x,y` | Integer pair (`int,int`) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates `x,y` | Integer pair (`int,int`) | `EXIT=19,14` |
| `OUTPUT_FILE` | Target output file path | String (`str`) | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Generate a perfect maze (True/False) | Boolean (`bool`) | `PERFECT=False` |
| `SEED` | Optional generation seed (reproducibility) | Integer (`int`) | `SEED=42` |

---


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
1. Entry coordinates (`x,y`)
2. Exit coordinates (`x,y`)
3. Shortest path sequence using cardinal directions (`N`, `E`, `S`, `W`).

---

## Code Quality & Verification

To verify codebase integrity, type safety, and linting standards, run:

```bash
# Run linters and type checkers (flake8 + mypy)
make lint

# Run strict type checking
make lint-strict

# Clean build artifacts
make clean
```

## Algorithm Choices & Justification

A-Maze-ing relies on graph theory algorithms for both maze generation and pathfinding. Below is the technical justification for the chosen algorithms:

### 1. Maze Generation: Randomized Depth-First Search (Iterative Backtracker)
- **Algorithm**: We use an iterative DFS with a stack to generate perfect mazes as spanning trees.
- **Why we chose it**: 
  - **Single Solution Guarantee**: DFS creates long, winding corridors with relatively few dead ends, making it ideal for generating classic "perfect mazes" where every cell is reachable with exactly one unique path between any two points.
  - **Stack-Based Iteration**: Implementing DFS iteratively with an explicit stack avoids Python's recursion depth limit errors on large maze grids (e.g., 100x100 or larger).
  - **Pac-Man Extension**: For `PERFECT=False` mode, we augment the generator with a dead-end removal pass that systematically punctures walls of dead-end cells into adjacent corridors, creating loops and open spaces reminiscent of retro arcade boards.

### 2. Maze Solving: Breadth-First Search (BFS)
- **Algorithm**: We use a queue (`collections.deque`) to perform level-order graph traversal from the entry coordinate to the exit coordinate.
- **Why we chose it**:
  - **Shortest Path Optimality**: In unweighted graphs (where every corridor edge has an equal cost of 1), **Breadth-First Search guarantees the absolute shortest path** from the start node to the goal node.
  - **Completeness**: BFS is guaranteed to find a path if one exists, efficiently exploring all reachable nodes level-by-level without getting trapped in infinite depth loops.
  - **Performance**: Operating in $O(V + E)$ time complexity (where $V$ is the number of cells and $E$ is the open passages), BFS executes near-instantly even on large grids. Reconstruction of the path is efficiently handled by maintaining a parent pointer dictionary.

---

## Code Reusability

Modular design principles were strictly followed to maximize code reusability across the project:
- **`mazegen.py`**: The entire maze generation engine (and its documentation) lives in a single standalone file with no third-party dependencies. It is packaged as `mazegen-1.0.0-py3-none-any.whl` so a future project can install and reuse it (see below).
- **`Config` Parser (`parse/parser.py` & `config_interpretor.py`)**: Designed as a standalone configuration schema validator. It can be easily imported and reused by any module or future GUI/CLI interface requiring validated maze parameters.
- **Renderers (`visualizer/tui.py` & `window.py`)**: Separated into independent display adapters that consume the grid state without modifying business logic.
- **Application adapter (`maze_interpretor/maze_generator.py`)**: A thin layer that binds the reusable `mazegen` engine to this project's needs (the closed-cell "42" pattern and the output file format).

### Reusable Module Documentation (`mazegen`)

`mazegen.py` exposes a single class, `MazeGenerator`. After installing the wheel (`make package`, then `pip install mazegen-1.0.0-py3-none-any.whl`):

```python
from mazegen import MazeGenerator

# Instantiate and generate: size, seed, and mode are all custom parameters.
maze = MazeGenerator(width=20, height=15, seed=42, perfect=True)
maze.generate()

# Access the generated structure: grid[y][x] is a Cell whose `walls`
# bitmask encodes closed walls (North=1, East=2, South=4, West=8).
grid = maze.get_grid()

# Access a solution: shortest path between any two cells (BFS).
path = maze.get_shortest_path((0, 0), (19, 14))
```

Custom parameters:
- `width`, `height`: maze dimensions in cells (must be positive).
- `seed`: optional seed for reproducible generation.
- `perfect=True`: spanning tree with a unique path between any two points; `perfect=False`: dead ends are opened to create loops (a playable board).
- `reserved_cells`: optional set of `(x, y)` coordinates that are never carved and stay fully closed (e.g. to embed the "42" pattern).

The same documentation is available as the `mazegen.py` module docstring and in the class/method docstrings.

---

## Team & Project Management

### Team Roles
- **`jzampier` (Joao)**: Maze generation engine, BFS shortest path solver.
- **`pezio` (Pietro)**: Configuration parser, 42 pattern embedding, and TUI/window visualizers, exception handling framework, CLI controllers.

### Anticipated Planning & Evolution
1. **Phase 1 (Research & Design)**: Studied graph traversal algorithms (DFS vs BFS vs A*), defined the 4-bit hexadecimal bitmask standard, and drafted configuration grammar rules.
2. **Phase 2 (Core Implementation)**: Developed the configuration parser, robust exception system, and the DFS maze generation engine.
3. **Phase 3 (Solving & Advanced Features)**: Implemented the BFS shortest path solver, dead-end removal for Pac-Man mode, and the centered `42` logo integration.
4. **Phase 4 (Visualizers & Quality Assurance)**: Built the TUI and graphical visualizers, added automated tests, and ensured strict compliance with `flake8` and `mypy` strict typing.

### What Worked Well & What Could Be Improved
- **What worked well**:
  - Clear separation of concerns between parsing, generation, solving, and visualization.
  - Strict typing (`mypy`) caught potential null reference bugs early during refactoring.
  - Iterative DFS prevented recursion stack overflows on large grids.
- **What could be improved**:
  - Adding asynchronous visualization animation frames for step-by-step BFS exploration in future iterations.
  - Extending configuration options to support custom color themes in the TUI.

### Specific Tools Used
- **Language**: Python 3.10+
- **Build & Automation**: Make / Makefile
- **Type Checking**: `mypy` (strict mode)
- **Linting**: `flake8`
- **Version Control**: Git & GitHub

---

## Resources & AI Usage

### Classic References
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. *Introduction to Algorithms* (Graph Traversal, BFS, DFS).
- Red Blob Games. *Pathfinding and Maze Generation Tutorials*.
- 42 School Subject Guidelines for *A-Maze-ing*.

### AI Usage Disclosure
Artificial Intelligence (specifically Gemini) was utilized during the development of this project for specific supportive tasks:
- **Documentation & Structuring**: Assisting in structuring and refining markdown documentation (including this `README.md`) to meet the comprehensive 42 curriculum evaluation rubric.
- **Type Hinting & Docstrings**: Reviewing Python type hints and PEP 257 docstring compliance to ensure rigorous `mypy` strict compatibility.
- **Test Case Brainstorming**: Discussing edge cases for configuration parsing errors and invalid maze dimensions.
