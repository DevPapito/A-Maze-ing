from dataclasses import dataclass
from typing import List
from parse.parser import Config
import random

@dataclass
class Cell:
    """Represents a single cell in the maze grid."""

    x: int
    y: int
    walls: int = 15
    passed: bool = False

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

OPPOSITE = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST
}

DELTA = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0)
}

class MazeGenerator:
    """Class responsible for generating the maze based on configuration."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._42_cells: set[tuple[int, int]] = set()
        self.init_grid()

    def get_config(self) -> Config:
        return self._config

    def get_grid(self) -> List[List[Cell]]:
        return self._grid

    def remove_walls(self, cell1: Cell, cell2: Cell, direction: int) -> None:
        """ Remove walls between two adjacent cells in the specified direction."""
        cell1.walls &= ~direction
        cell2.walls &= ~OPPOSITE[direction]

    def has_wall(self, cell: Cell, direction: int) -> bool:
        """Check if a cell has a wall in the specified direction."""
        return (cell.walls & direction) != 0

    def init_grid(self) -> None:
        """Initialize the maze grid with Cell instances.

        All walls are closed by default (value 15 / 0xF).
        Dimensions are given by config.height (rows)
        and config.width (cols).
        """
        self._grid = [
            [
                Cell(x=x, y=y, walls=15, passed=False)
                for x in range(self._config.width)
            ]
            for y in range(self._config.height)
        ]

    def get_unvisited_neighbors(self, cell: Cell) -> list[tuple[Cell, int]]:
        """Returns a list of tuples (neighbor, direction) that hasn't been passed"""
        neighbors: list[tuple[Cell, int]] = []
        directions = DELTA

        for direction, (dx, dy) in directions.items():
            nx, ny = cell.x + dx, cell.y + dy

            if (0 <= nx < self._config.width and
                    0 <= ny < self._config.height):
                neighbor = self._grid[ny][nx]
                if not neighbor.passed:
                    neighbors.append((neighbor, direction))

        return neighbors

    def generate(self) -> None:
        """Generate the perfect maze using iterative DFS."""
        self.init_grid()
        self._42_cells = self._get_42_cells()
        for x, y in self._42_cells:
            self._grid[y][x].passed = True

        if self._config.seed is not None:
            random.seed(self._config.seed)

        stack: list[Cell] = []
        start_cell = self._grid[0][0]
        if start_cell.passed:
            raise ValueError("The maze is too small to place the 42 pattern.")
        start_cell.passed = True
        stack.append(start_cell)

        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)

            if neighbors:
                next_cell, direction = random.choice(neighbors)
                self.remove_walls(current, next_cell, direction)
                next_cell.passed = True
                stack.append(next_cell)
            else:
                stack.pop()

        if not self._config.perfect:
            self.add_loops()

    def _get_42_cells(self) -> set[tuple[int, int]]:
        """Return the centered cells that form the closed-cell 42 pattern."""
        pattern = (
            "X.X.XXX",
            "X.X...X",
            "XXX.XXX",
            "..X.X..",
            "..X.XXX",
        )
        pattern_width = len(pattern[0])
        pattern_height = len(pattern)

        if (self._config.width < pattern_width + 2 or
                self._config.height < pattern_height + 1):
            print(
                "Error: maze too small to display the 42 pattern; "
                "generating it without the pattern."
            )
            return set()

        left = (self._config.width - pattern_width + 1) // 2
        top = (self._config.height - pattern_height + 1) // 2
        return {
            (left + x, top + y)
            for y, row in enumerate(pattern)
            for x, value in enumerate(row)
            if value == "X"
        }

    def add_loops(self, chance: float = 0.2) -> None:
        if self._config.width > 1:
            self.remove_walls(self._grid[0][0], self._grid[0][1], EAST)

        for y in range(self._config.height):
            for x in range(self._config.width):
                cell = self._grid[y][x]
                if (x, y) in self._42_cells:
                    continue
                if cell.walls > 8 and random.random() < chance:
                    directions = [NORTH, SOUTH, EAST, WEST]
                    random.shuffle(directions)
                    for d in directions:
                        if self.has_wall(cell, d):
                            dx, dy = DELTA[d]
                            nx, ny = x + dx, y + dy
                            in_bounds = (
                                0 <= nx < self._config.width
                                and 0 <= ny < self._config.height
                            )
                            if in_bounds:
                                if (nx, ny) in self._42_cells:
                                    continue
                                neighbor = self._grid[ny][nx]
                                self.remove_walls(cell, neighbor, d)
                                break
