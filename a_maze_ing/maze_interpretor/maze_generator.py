from dataclasses import dataclass
from typing import List
from parse.parser import Config
from random import seed as random_seed

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
        self._grid: List[List[Cell]] = []

        if self._config.seed is not None:
            random_seed(self._config.seed)

        print(f"Generating maze with seed: {self._config.seed}")

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
