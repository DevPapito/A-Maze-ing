import sys
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional, Tuple

from maze_interpretor.maze_generator import Cell
from parse.parser import Config
from .tui import Ansi, Theme


NORTH = 0x1
EAST = 0x2
SOUTH = 0x4
WEST = 0x8

DIRECTIONS: Tuple[Tuple[int, int, int, int], ...] = (
    (0, -1, NORTH, SOUTH),
    (1, 0, EAST, WEST),
    (0, 1, SOUTH, NORTH),
    (-1, 0, WEST, EAST),
)


class Window:

    @dataclass
    class Setting:
        pass

    def __init__(self, config: Config) -> None:
        self._ansi = Ansi()
        self._setting = self.Setting
        self._config = config

    def _coordinates(self, value: float) -> Tuple[int, int]:
        """Return x and y using the configuration's existing float encoding."""
        parts = str(value).split(".")
        return int(parts[0]), int(parts[1])

    def _paint_tile(self, y: int, x: int, color: int) -> None:
        """Paint one two-character tile at visual-grid coordinates."""
        self._ansi.print(self._ansi.move_cursor(y, x))
        self._ansi.print(self._ansi.paint(self._ansi.BACKGROUND, color))
        self._ansi.print("  ")

    def _shortest_path(
        self,
        grid: List[List[Cell]],
        start: Tuple[int, int],
        goal: Tuple[int, int],
    ) -> List[Tuple[int, int]]:
        """Find a shortest route through passages encoded in the cell walls."""
        queue: Deque[Tuple[int, int]] = deque([start])
        parents: Dict[
            Tuple[int, int], Optional[Tuple[int, int]]
        ] = {start: None}
        height = len(grid)
        width = len(grid[0])

        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break

            for dx, dy, wall, opposite_wall in DIRECTIONS:
                next_x = x + dx
                next_y = y + dy
                if not (0 <= next_x < width and 0 <= next_y < height):
                    continue
                if grid[y][x].walls & wall:
                    continue
                if grid[next_y][next_x].walls & opposite_wall:
                    continue

                neighbor = (next_x, next_y)
                if neighbor not in parents:
                    parents[neighbor] = (x, y)
                    queue.append(neighbor)

        if goal not in parents:
            return []

        path: List[Tuple[int, int]] = []
        current: Optional[Tuple[int, int]] = goal
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path

    def _draw_open_passages(
        self, grid: List[List[Cell]], theme: Theme
    ) -> None:
        """Draw cell interiors and passages with open neighboring walls."""
        height = len(grid)
        width = len(grid[0])

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                center_y = (2 * y) + 1
                center_x = (2 * x) + 1
                self._paint_tile(center_y, center_x, theme.open_wall)

                for dx, dy, wall, opposite_wall in DIRECTIONS:
                    if wall not in (EAST, SOUTH):
                        continue
                    next_x = x + dx
                    next_y = y + dy
                    if not (0 <= next_x < width and 0 <= next_y < height):
                        continue
                    if cell.walls & wall:
                        continue
                    if grid[next_y][next_x].walls & opposite_wall:
                        continue

                    self._paint_tile(
                        center_y + dy,
                        center_x + dx,
                        theme.open_wall,
                    )

    def _draw_path(
        self, path: List[Tuple[int, int]], theme: Theme
    ) -> None:
        """Overlay the route while leaving ENTRY and EXIT markers visible."""
        if not path:
            return

        start = path[0]
        goal = path[-1]
        for x, y in path:
            if (x, y) not in (start, goal):
                self._paint_tile(
                    (2 * y) + 1,
                    (2 * x) + 1,
                    theme.path_wall,
                )

        for current, following in zip(path, path[1:]):
            x = current[0] + following[0] + 1
            y = current[1] + following[1] + 1
            self._paint_tile(y, x, theme.path_wall)

    def drawer(self, grid: List[List[Cell]], theme: Theme) -> None:
        """Draw the maze, endpoints, and shortest route in the terminal."""
        if len(grid) != self._config.height or any(
            len(row) != self._config.width for row in grid
        ):
            raise ValueError("Grid dimensions do not match the configuration")

        entry = self._coordinates(self._config.entry)
        exit_coord = self._coordinates(self._config.exit)
        for name, (x, y) in (("ENTRY", entry), ("EXIT", exit_coord)):
            in_bounds = (
                0 <= x < self._config.width
                and 0 <= y < self._config.height
            )
            if not in_bounds:
                raise ValueError(f"{name} coordinates are outside the grid")

        path = self._shortest_path(grid, entry, exit_coord)
        visual_height = (2 * self._config.height) + 1
        visual_width = (2 * self._config.width) + 1

        self._ansi.clear_terminal()
        self._ansi.print(self._ansi.HIDE_CURSOR)
        try:
            # 1. Fill the visual grid with closed-wall color.
            for y in range(visual_height):
                for x in range(visual_width):
                    self._paint_tile(y, x, theme.close_wall)

            # 2. Open cell interiors and passages.
            self._draw_open_passages(grid, theme)

            # 3. Mark ENTRY and EXIT.
            self._paint_tile(
                (2 * entry[1]) + 1,
                (2 * entry[0]) + 1,
                theme.entry_wall,
            )
            self._paint_tile(
                (2 * exit_coord[1]) + 1,
                (2 * exit_coord[0]) + 1,
                theme.exit_wall,
            )

            # 4. Overlay the shortest route without covering the endpoints.
            self._draw_path(path, theme)
            self._ansi.print(self._ansi.move_cursor(visual_height, 0))
        finally:
            self._ansi.print(self._ansi.RESET)
            self._ansi.print(self._ansi.SHOW_CURSOR)

        if not path:
            sys.stderr.write("No path exists between ENTRY and EXIT.\n")

    def clear(self) -> None:
        pass
