from parse import parser
from maze_interpretor import MazeGenerator
from visualizer import Window, Theme
from controller import Controller


def main() -> None:
    """Main entry point for A-Maze-ing."""
    themes = [
        Theme("dark", 232, 235, 238, 28, 124),
        Theme("matrix", 22, 46, 2, 28, 124),
        Theme("neon", 53, 201, 198, 28, 124),
        Theme("ocean", 17, 27, 33, 28, 124),
        Theme("sunset", 52, 166, 208, 28, 124),
    ]

    config = parser()
    maze = MazeGenerator(config)
    window = Window(config)
    menu_controller = Controller(maze, window, themes)
    menu_controller.menu()

if __name__ == '__main__':
    main()
