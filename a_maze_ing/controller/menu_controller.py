from visualizer.window import Window
from visualizer.tui import Theme, Ansi
from maze_interpretor.maze_generator import MazeGenerator

import readchar

class Controller():
    def __init__(self, maze_gen: MazeGenerator, window: Window, themes: list) -> None:
        self._window = window
        self._themes = themes
        self._maze_gen = maze_gen
        self._position = 0
        self._run = True
        self._show_path = False
        if hasattr(self._maze_gen, 'generate'):
            self._maze_gen.generate()

    def _switch(self, user_input: int) -> None:
        if (user_input == 1):
            if hasattr(self._maze_gen, 'generate'):
                self._maze_gen.generate()
            elif hasattr(self._maze_gen, 'init_grid'):
                self._maze_gen.init_grid()
            # Vai regerar o mapa
        elif (user_input == 2):
            if not self._show_path:
                self._show_path = True
            else:
                self._show_path = False
        elif (user_input == 3):
            if (len(self._themes) - 1 == self._position):
                self._position = 0
            else:
                self._position += 1
        elif (user_input == 4):
            self._run = False

    def menu(self) -> None:
        ansi = Ansi()
        while (self._run):
            self._window.drawer(self._maze_gen.get_grid(), self._themes[self._position], self._show_path)
            ansi.print(ansi.paint(ansi.FOREGROUND, self._themes[self._position].exit_wall))
            print(f"Debug show path: {self._show_path}")
            print("=== A-Maze-ing ===")
            ansi.print(ansi.paint(ansi.FOREGROUND, 252))
            print(f"Theme name: {self._themes[self._position].name}")
            print("1. Re-generate a new maze")
            print("2. Show / Hide the shortest path")
            print("3. Rotate the wall colours")
            print("4. Quit")
            #ansi.print(ansi.RESET)
            try:
                #keyboard = readchar.readchar()
                #print(type(keyboard))
                user_input = int(input("Choice (1-4): "))  # temp
                self._switch(user_input)
            except Exception:
                pass
            finally:
               ansi.print(ansi.RESET)
