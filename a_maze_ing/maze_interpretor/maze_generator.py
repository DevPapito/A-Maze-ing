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

        if self._config.seed is not None:
            random.seed(self._config.seed)

        stack: list[Cell] = []
        start_cell = self._grid[0][0]
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

    def add_loops(self, chance: float = 0.2) -> None:
        for y, row in enumerate(self._grid):
            for x, cell in enumerate(row):
                if x + 1 < self._config.width:
                    neighbor = self._grid[y][x + 1]
                    if self.has_wall(cell, EAST) and random.random() < chance:
                        self.remove_walls(cell, neighbor, EAST)

                if y + 1 < self._config.height:
                    neighbor = self._grid[y + 1][x]
                    if self.has_wall(cell, SOUTH) and random.random() < chance:
                        self.remove_walls(cell, neighbor, SOUTH)
