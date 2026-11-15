"""Launch the A-Maze-ing terminal application."""

import sys
from parse import parser
from maze_interpretor import MazeGenerator
from visualizer import Window, Theme
from controller import Controller


def main() -> None:
    """Main entry point for A-Maze-ing."""
    themes = [
        Theme("Dark", 233, 252, 243, 1, 2),
        Theme("Flash", 252, 233, 240, 1, 2),
        Theme("Vice city", 234, 201, 123, 1, 2),
        Theme("Wood art", 95, 238, 137, 1, 2),
        Theme("Sandstorm", 52, 223, 202, 1, 2),
    ]

    try:
        config = parser()
        maze = MazeGenerator(config)
        window = Window(config)
        menu_controller = Controller(maze, window, themes)
        menu_controller.menu()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
