from parse import parser
from maze_interpretor import MazeGenerator
from visualizer import Ansi


def main() -> None:
    """Main entry point for A-Maze-ing."""
    config = parser()
    _maze = MazeGenerator(config)
    # print(_maze.get_grid())
    ansi = Ansi()
    ansi.print(ansi.CLEAR_SCREEN)
    ansi.print(ansi.HIDE_CURSOR)
    try:
        ansi.print(ansi.move_cursor(5, 10))
        ansi.print("Ola mundo!, esse e o buffer alternativo\n")
    except Exception:
        pass
    finally:
        ansi.print(ansi.SHOW_CURSOR)


if __name__ == '__main__':
    main()
