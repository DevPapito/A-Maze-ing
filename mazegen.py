"""mazegen - a reusable maze generation module.

This module is standalone (no third-party dependencies) so it can be
installed with pip and imported by any future project:

    pip install mazegen-1.0.0-py3-none-any.whl

Quick start:

    from mazegen import MazeGenerator

    # Create and generate a perfect 20x15 maze, reproducible via seed.
    maze = MazeGenerator(width=20, height=15, seed=42, perfect=True)
    maze.generate()

    # Access the generated structure: grid[y][x] is a Cell whose
    # `walls` bitmask encodes the closed walls (North=1, East=2,
    # South=4, West=8). Example: walls == 3 (binary 0011) means the
    # cell is open to the south and west.
    grid = maze.get_grid()

    # Access a solution (shortest path between any two cells):
    path = maze.get_shortest_path((0, 0), (19, 14))

The generator accepts custom parameters: size (width/height), seed
(reproducibility), perfect (spanning tree vs. looped board), and
reserved_cells (coordinates that are never carved and stay fully
closed, e.g. to embed a pattern such as the "42" logo).
"""

import random
from dataclasses import dataclass
from typing import List, Set, Tuple

Coordinate = Tuple[int, int]


@dataclass
class Cell:
    """A single cell of the maze grid.

    Attributes:
        x: Horizontal position of the cell (column).
        y: Vertical position of the cell (row).
        walls: Bitmask of the closed walls: North=1, East=2, South=4,
            West=8. Example: 3 (binary 0011) means open to the south
            and west; A (binary 1010) means east and west are closed.
        passed: Internal flag used while carving the maze.
    """

    x: int
    y: int
    walls: int = 15
    passed: bool = False


NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

ALL_WALLS = 0xF

OPPOSITE = {NORTH: SOUTH, EAST: WEST, SOUTH: NORTH, WEST: EAST}

DELTA = {NORTH: (0, -1), SOUTH: (0, 1), EAST: (1, 0), WEST: (-1, 0)}

# Wall masks of a cell with exactly one open side (a dead end).
DEAD_END_WALLS = {7, 11, 13, 14}


class MazeGenerator:
    """Generate reproducible mazes with an iterative DFS backtracker.

    The generator is standalone: it only needs the maze dimensions.
    Its own random source is used, so reproducibility is driven by the
    seed without touching the global random state of the caller.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
        perfect: bool = True,
        reserved_cells: Set[Coordinate] | None = None,
    ) -> None:
        """Create a generator for a width x height maze.

        Args:
            width: Maze width in cells (must be positive).
            height: Maze height in cells (must be positive).
            seed: Optional seed for reproducible generation.
            perfect: True generates a spanning tree (exactly one path
                between any two cells). False opens dead ends to create
                loops (a playable board).
            reserved_cells: Optional cells that must never be carved;
                they stay fully closed (e.g. to embed a pattern).
        """
        if width < 1 or height < 1:
            raise ValueError("width and height must be positive integers")
        self._width = width
        self._height = height
        self._perfect = perfect
        self._rng = random.Random(seed)
        self._reserved: Set[Coordinate] = set()
        if reserved_cells:
            self._reserved = set(reserved_cells)
        self._dead_ends: List[Cell] = []
        self.init_grid()

    @property
    def width(self) -> int:
        """Return the maze width in cells."""
        return self._width

    @property
    def height(self) -> int:
        """Return the maze height in cells."""
        return self._height

    def init_grid(self) -> None:
        """Initialize the grid of fully closed cells.

        All walls are closed by default (value 15 / 0xF). Dimensions
        are given by width (columns) and height (rows).
        """
        self._grid: List[List[Cell]] = [
            [Cell(x=x, y=y, walls=ALL_WALLS, passed=False)
             for x in range(self._width)]
            for y in range(self._height)
        ]

    def get_grid(self) -> List[List[Cell]]:
        """Return the current maze grid, indexed as grid[y][x]."""
        return self._grid

    def remove_walls(
        self, cell1: Cell, cell2: Cell, direction: int
    ) -> None:
        """Remove the walls between two adjacent cells."""
        cell1.walls &= ~direction
        cell2.walls &= ~OPPOSITE[direction]

    def has_wall(self, cell: Cell, direction: int) -> bool:
        """Check if a cell has a closed wall in the given direction."""
        return (cell.walls & direction) != 0

    def get_unvisited_neighbors(
        self, cell: Cell
    ) -> list[tuple[Cell, int]]:
        """Return the not-yet-carved neighbors and their direction."""
        neighbors: list[tuple[Cell, int]] = []

        for direction, (dx, dy) in DELTA.items():
            nx, ny = cell.x + dx, cell.y + dy

            if (0 <= nx < self._width and 0 <= ny < self._height):
                neighbor = self._grid[ny][nx]
                if not neighbor.passed:
                    neighbors.append((neighbor, direction))

        return neighbors

    def generate(self) -> None:
        """Carve the maze using an iterative depth-first search.

        A previously generated maze is discarded. When the maze is not
        perfect, dead ends are opened afterward to create loops.
        """
        self.init_grid()
        self._dead_ends = []

        for x, y in self._reserved:
            self._grid[y][x].passed = True

        start = self._grid[0][0]
        if start.passed:
            raise ValueError(
                "Cannot generate the maze: cell (0, 0) is reserved."
            )
        start.passed = True
        stack: List[Cell] = [start]
        is_advancing = True

        while stack:
            current = stack[-1]
            neighbors = self.get_unvisited_neighbors(current)

            if neighbors:
                next_cell, direction = self._rng.choice(neighbors)
                self.remove_walls(current, next_cell, direction)
                next_cell.passed = True
                stack.append(next_cell)
                is_advancing = True
            else:
                if is_advancing:
                    self._dead_ends.append(current)
                    is_advancing = False
                stack.pop()

        if start.walls in DEAD_END_WALLS and start not in self._dead_ends:
            self._dead_ends.append(start)

        if not self._perfect:
            self._open_dead_ends()

    def _open_dead_ends(self) -> None:
        """Open one wall of each dead end to create loops."""
        for cell in self._dead_ends:
            if cell.walls not in DEAD_END_WALLS:
                continue

            directions = [NORTH, SOUTH, EAST, WEST]
            self._rng.shuffle(directions)

            for direction in directions:
                if self.has_wall(cell, direction):
                    dx, dy = DELTA[direction]
                    nx, ny = cell.x + dx, cell.y + dy
                    if (
                        0 <= nx < self._width
                        and 0 <= ny < self._height
                        and (nx, ny) not in self._reserved
                    ):
                        neighbor = self._grid[ny][nx]
                        self.remove_walls(cell, neighbor, direction)
                        break

    def get_shortest_path(
        self,
        start: Coordinate,
        goal: Coordinate,
    ) -> List[Coordinate]:
        """Find the shortest path between two cells (breadth-first).

        Args:
            start: (x, y) coordinates of the start cell.
            goal: (x, y) coordinates of the goal cell.

        Returns:
            The list of coordinates from start to goal, or an empty
            list when no path exists. Raises ValueError when an
            endpoint lies outside the maze.
        """
        for x, y in (start, goal):
            if not (0 <= x < self._width and 0 <= y < self._height):
                raise ValueError(
                    "Path endpoints must be inside the maze."
                )

        queue = [start]
        head = 0
        parents: dict[Coordinate, Coordinate | None] = {start: None}

        while head < len(queue):
            x, y = queue[head]
            head += 1
            if (x, y) == goal:
                break

            cell = self._grid[y][x]
            for direction in (NORTH, EAST, SOUTH, WEST):
                dx, dy = DELTA[direction]
                next_x, next_y = x + dx, y + dy
                if not (
                    0 <= next_x < self._width
                    and 0 <= next_y < self._height
                ):
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

        path: List[Coordinate] = []
        current: Coordinate | None = goal
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path
