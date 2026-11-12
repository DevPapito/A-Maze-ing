from typing import List
from dataclasses import dataclass
from maze_interpretor.maze_generator import Cell
from parse.parser import Config
from .tui import Ansi, Theme


class Window():

    @dataclass
    class Setting:
        pass

    def __init__(self, config: Config) -> None:
        self._ansi = Ansi()
        self._setting = self.Setting
        self._config = config

    def drawer(self, grid: List[List[Cell]], theme) -> None:
        # Estrutura real da mostragem do primeiro passo da tela
        self._ansi.clear_terminal()
        self._ansi.print(self._ansi.HIDE_CURSOR)
        self._ansi.print(self._ansi.MOVE_CURSOR_HOME)
        for i in range(self._config.height):
            for j in range(self._config.width):
                self._ansi.move_cursor(i, j)
                self._ansi.print(self._ansi.paint(self._ansi.BACKGROUND, theme.close_wall))
                self._ansi.print("  ")
            self._ansi.print('\n')

        self._ansi.print(self._ansi.MOVE_CURSOR_HOME)
        # Estrutura da mostragem dos caminhos
        for i in range(self._config.height):
            for j in range(self._config.width):
                if (i % 2 != 0):
                   self._ansi.move_cursor(i, j)
                   self._ansi.print(self._ansi.paint(self._ansi.BACKGROUND, theme.path_wall))
                   self._ansi.print("  ")
            self._ansi.print('\n')

        # Estrutura real da mostragem dos pontos de entrada como de saida
        self._ansi.print(self._ansi.MOVE_CURSOR_HOME)
        entry = str(self._config.entry).split('.')
        self._ansi.print(self._ansi.move_cursor(int(entry[1]), int(entry[0])))
        self._ansi.print(self._ansi.paint(self._ansi.BACKGROUND, theme.entry_wall))
        self._ansi.print("  ")

        self._ansi.print(self._ansi.MOVE_CURSOR_HOME)
        exit = str(self._config.exit).split('.')
        self._ansi.print(self._ansi.move_cursor(int(exit[1]), int(exit[0])))
        self._ansi.print(self._ansi.paint(self._ansi.BACKGROUND, theme.exit_wall))
        self._ansi.print("  ")
        self._ansi.print(self._ansi.move_cursor(self._config.height, 0)) # para mover o cursor de maneira segura ao fim do codigo

        self._ansi.print(self._ansi.RESET)
        self._ansi.print(self._ansi.SHOW_CURSOR)

        # Restando a mostragem do caminho mais curto entre os pontos ENTRY e EXIT

    def clear(self) -> None:
        pass
