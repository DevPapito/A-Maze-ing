from parse import parser
from maze_interpretor import MazeGenerator
from visualizer import Window, Theme


def main() -> None:
    """Main entry point for A-Maze-ing."""
    dark = Theme(232, 235, 238, 28, 124)
    matrix = Theme(22, 46, 2, 10, 118)
    neon = Theme(53, 201, 198, 226, 213)
    ocean = Theme(17, 27, 33, 45, 51)
    sunset = Theme(52, 166, 208, 214, 220)

    config = parser()
    maze = MazeGenerator(config)
    window = Window(config)
    window.drawer(maze.get_grid(), sunset)


if __name__ == '__main__':
    main()
