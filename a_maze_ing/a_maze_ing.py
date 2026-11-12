from parse import parser
from maze_interpretor import MazeGenerator
from visualizer import Window, Theme


def main() -> None:
    """Main entry point for A-Maze-ing."""
    dark = Theme("dark", 232, 235, 238, 28, 124)
    matrix = Theme("matrix", 22, 46, 2, 10, 118)
    neon = Theme("neon", 53, 201, 198, 226, 213)
    ocean = Theme("ocean", 17, 27, 33, 45, 51)
    sunset = Theme("sunset", 52, 166, 208, 214, 220)

    config = parser()
    maze = MazeGenerator(config)
    window = Window(config)
    window.drawer(maze.get_grid(), sunset)


if __name__ == '__main__':
    main()
