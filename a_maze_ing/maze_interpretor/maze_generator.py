"""Generate mazes, find paths, and write maze output files."""

from collections import deque
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
        """Create a generator using the supplied maze configuration."""
        self._config = config
        self._42_cells: set[tuple[int, int]] = set()
        self.init_grid()

    def get_config(self) -> Config:
        """Return the configuration used to generate the maze."""
        return self._config

    def get_grid(self) -> List[List[Cell]]:
        """Return the current maze grid."""
        return self._grid

    def remove_walls(self, cell1: Cell, cell2: Cell, direction: int) -> None:
        """Remove walls between two adjacent cells in the specified
        direction.
        """
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
        """Return unpassed neighbors and their direction."""
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
        self._dead_ends: list[Cell] = []
        self._42_cells = self._get_42_cells()
        if self._config.exit in self._42_cells:
            raise ValueError(
                f"EXIT coordinates {self._config.exit} "
                "cannot be inside the 42 pattern."
            )
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

        is_advancing = True

        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)

            if neighbors:
                next_cell, direction = random.choice(neighbors)
                self.remove_walls(current, next_cell, direction)
                next_cell.passed = True
                stack.append(next_cell)
                is_advancing = True
            else:
                if is_advancing:
                    self._dead_ends.append(current)
                    is_advancing = False
                stack.pop()
        if (
            start_cell.walls in {7, 11, 13, 14}
            and start_cell not in self._dead_ends
        ):
            self._dead_ends.append(start_cell)

        if not self._config.perfect:
            self.remove_dead_ends()

    def _get_42_cells(self) -> set[tuple[int, int]]:
        """Return the centered cells that form the closed-cell 42 pattern."""
        pattern = (
            "X...XXX",
            "X.....X",
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

    def remove_dead_ends(self) -> None:
        """Connect dead ends to valid neighboring cells."""
        dead_end_masks = {7, 11, 13, 14}

        for cell in self._dead_ends:
            if cell.walls not in dead_end_masks:
                continue

            directions = [NORTH, SOUTH, EAST, WEST]
            random.shuffle(directions)

            for d in directions:
                if self.has_wall(cell, d):
                    dx, dy = DELTA[d]
                    nx, ny = cell.x + dx, cell.y + dy
                    if (
                        0 <= nx < self._config.width
                        and 0 <= ny < self._config.height
                        and (nx, ny) not in self._42_cells
                    ):
                        neighbor = self._grid[ny][nx]
                        self.remove_walls(cell, neighbor, d)
                        break

    def get_shortest_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Find the shortest path between two cells in the generated maze."""
        height = len(self._grid)
        width = len(self._grid[0]) if self._grid else 0
        for x, y in (start, goal):
            if not (0 <= x < width and 0 <= y < height):
                raise ValueError("Path endpoints must be inside the maze.")

        queue = deque([start])
        parents: dict[
            tuple[int, int], tuple[int, int] | None
        ] = {start: None}

        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break

            cell = self._grid[y][x]
            for direction in (NORTH, EAST, SOUTH, WEST):
                dx, dy = DELTA[direction]
                next_x, next_y = x + dx, y + dy
                if not (0 <= next_x < width and 0 <= next_y < height):
                    continue
                if self.has_wall(cell, direction):
                    continue

                neighbor_cell = self._grid[next_y][next_x]
                if self.has_wall(neighbor_cell, OPPOSITE[direction]):
                    continue

                neighbor = (next_x, next_y)
                if neighbor not in parents:
                    parents[neighbor] = (x, y)
                    queue.append(neighbor)

        if goal not in parents:
            return []

        path: list[tuple[int, int]] = []
        current: tuple[int, int] | None = goal
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path

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
            for row in self._grid
        ]
        direction_symbols = {
            (0, -1): "N",
            (1, 0): "E",
            (0, 1): "S",
            (-1, 0): "W",
        }
        directions = "".join(
            direction_symbols[
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
