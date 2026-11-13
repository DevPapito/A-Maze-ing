from dataclasses import dataclass
from typing import List
from parse.parser import Config


@dataclass
class Cell:
    """Represents a single cell in the maze grid."""

    x: int
    y: int
    walls: int = 15
    passed: bool = False


class MazeGenerator:
    """Class responsible for generating the maze based on configuration."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._grid: List[List[Cell]] = []
        self.init_grid()

    def get_config(self) -> Config:
        return self._config

    def get_grid(self) -> List[List[Cell]]:
        return self._grid

    def init_grid(self) -> None:
        """Initialize the maze grid with Cell instances.

        All walls are closed by default (value 15 / 0xF).
        Dimensions are given by config.height (rows)
        and config.width (cols).
        """
        try:
            from visualizer.mock_grid import build_mock_grid
            self._grid = build_mock_grid(self._config.width, self._config.height)
        except Exception:
            self._grid = [
                [
                    Cell(x=x, y=y, walls=15, passed=False)
                    for x in range(self._config.width)
                ]
                for y in range(self._config.height)
            ]

    def generate(self) -> None:
        """Temporary generate method using mock grid while maze generator is unfinished."""
        self.init_grid()
