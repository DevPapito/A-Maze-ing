from parse import parser
from maze_interpretor import MazeGenerator


def main() -> None:
    config = parser()
    maze = MazeGenerator(config)
    print(maze.get_grid())


if __name__ == '__main__':
    main()
