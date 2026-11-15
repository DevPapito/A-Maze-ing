"""Application maze generator: "42" pattern and output file writing.

Thin application layer over the reusable `mazegen` module: it computes
the centered closed-cell "42" pattern required by the subject, hands it
to the generator as reserved cells, and writes the generated maze to
the output file configured by the user.
"""

from typing import Dict, List, Set, Tuple

from mazegen import Cell, Coordinate
from mazegen import MazeGenerator as BaseMazeGenerator

from a_maze_ing.parse.parser import Config


# Rows of the centered "42" pattern drawn with fully closed cells.
FORTY_TWO_PATTERN = (
    "X...XXX",
    "X.....X",
    "XXX.XXX",
    "..X.X..",
    "..X.XXX",
)

DIRECTION_SYMBOLS: Dict[Tuple[int, int], str] = {
    (0, -1): "N",
    (1, 0): "E",
    (0, 1): "S",
    (-1, 0): "W",
}


def get_42_cells(width: int, height: int) -> Set[Coordinate]:
    """Return the centered cells forming the closed-cell "42" pattern.

    Prints an error message and returns an empty set when the maze is
    too small to hold the pattern.
    """
    pattern_width = len(FORTY_TWO_PATTERN[0])
    pattern_height = len(FORTY_TWO_PATTERN)

    if width < pattern_width + 2 or height < pattern_height + 1:
        print(
            "Error: maze too small to display the 42 pattern; "
            "generating it without the pattern."
        )
        return set()

    left = (width - pattern_width + 1) // 2
    top = (height - pattern_height + 1) // 2
    return {
        (left + x, top + y)
        for y, row in enumerate(FORTY_TWO_PATTERN)
        for x, value in enumerate(row)
        if value == "X"
    }


class MazeGenerator:
    """Application maze generator bound to the parsed configuration."""

    def __init__(self, config: Config) -> None:
        """Create the generator, reserving the "42" pattern cells."""
        self._config = config
        pattern_cells = get_42_cells(config.width, config.height)
        if config.exit in pattern_cells:
            raise ValueError(
                f"EXIT coordinates {config.exit} "
                "cannot be inside the 42 pattern."
            )
        self._generator = BaseMazeGenerator(
            config.width,
            config.height,
            seed=config.seed,
            perfect=config.perfect,
            reserved_cells=pattern_cells,
        )

    def generate(self) -> None:
        """Generate a new maze."""
        self._generator.generate()

    def get_grid(self) -> List[List[Cell]]:
        """Return the current maze grid."""
        return self._generator.get_grid()

    def get_shortest_path(
        self,
        start: Coordinate,
        goal: Coordinate,
    ) -> List[Coordinate]:
        """Return the shortest path between two cells (BFS)."""
        return self._generator.get_shortest_path(start, goal)

    def write_output_file(self) -> None:
        """Write the maze, endpoints, and route to the configured file."""
        entry = self._config.entry
        exit_coord = self._config.exit
        if entry == exit_coord:
            raise ValueError("ENTRY and EXIT must be different.")

        path = self.get_shortest_path(entry, exit_coord)
        if not path:
            raise ValueError("No path exists between ENTRY and EXIT.")

        rows = [
            "".join(f"{cell.walls:X}" for cell in row)
            for row in self.get_grid()
        ]
        directions = "".join(
            DIRECTION_SYMBOLS[
                (next_cell[0] - cell[0], next_cell[1] - cell[1])
            ]
            for cell, next_cell in zip(path, path[1:])
        )
        lines = rows + [
            "",
            f"{entry[0]},{entry[1]}",
            f"{exit_coord[0]},{exit_coord[1]}",
            directions,
        ]

        with open(self._config.output_file, "w", encoding="utf-8") as file:
            file.write("\n".join(lines) + "\n")
