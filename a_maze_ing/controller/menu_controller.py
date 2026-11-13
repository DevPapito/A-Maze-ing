from visualizer.window import Window
from visualizer.tui import Theme
from maze_interpretor.maze_generator import MazeGenerator
import os

class Controller():
   def __init__(self, maze_gen, window, themes): # Futuramente implementar o generate para window
        self._window = window
        self._themes = themes
        self._maze_gen = maze_gen
        self._position = 0
        self._run = True
        self._show_path = False

   def _switch(self, user_input):
       if (user_input == 1):
          # self._maze_gen.generate # new maze_generate
          # Vai regerar o mapa
          pass
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

   def menu(self):
      # self._window.drawer(self._maze_gen.get_grid(), self._themes[self._position], False)
       while (self._run):
            self._window.drawer(self._maze_gen.get_grid(), self._themes[self._position], self._show_path)
            print(f"Debug show path: {self._show_path}")
            print("=== A-Maze-ing ===")
            print(f"Theme name: {self._themes[self._position].name}")
            print("1. Re-generate a new maze")
            print("2. Show / Hide the shortest path")
            print("3. Rotate the wall colours")
            print("4. Quit")
            try:
               user_input = int(input("Choice2 (1-4): ")) # temp
               self._switch(user_input)
            except Exception:
                 pass

