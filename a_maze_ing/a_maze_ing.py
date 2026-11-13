from parse import parser
from maze_interpretor import MazeGenerator
from visualizer import Window, Theme
from controller import Controller
from visualizer.mock_grid import build_mock_grid # temp


def main() -> None:
    """Main entry point for A-Maze-ing."""
    themes = [
        Theme("dark", 232, 235, 238, 28, 124),
        Theme("matrix", 22, 46, 2, 10, 118),
        Theme("neon", 53, 201, 198, 226, 213),
        Theme("ocean", 17, 27, 33, 45, 51),
        Theme("sunset", 52, 166, 208, 214, 220),
    ]

    config = parser()
    maze = MazeGenerator(config)
    grid = build_mock_grid(config.width, config.height) # temp
    window = Window(config)
    # window.drawer(grid, sunset, True) just to test
    menu_controller = Controller(maze, window, themes)
    menu_controller.menu()

if __name__ == '__main__':
    main()
