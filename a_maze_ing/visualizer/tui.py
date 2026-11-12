import sys
import os
from dataclasses import dataclass

@dataclass
class Theme:
	name: str
	close_wall: int
	open_wall: int
	path_wall: int
	entry_wall: int
	exit_wall: int


class Ansi():

    ESC = "\x1b"
    CSI = f"{ESC}["  # Control Sequence Introducer

    # Basic styles
    INVERT_FG_BG = f"{CSI}7m"
    RESET = f"{CSI}0m"

    # Cursor

    MOVE_CURSOR_HOME = f"{CSI}H"
    CLEAR_SCREEN = f"{CSI}2J"
    CLEAR_CURSOR_LINE = f"{CSI}0J"
    HIDE_CURSOR = f"{CSI}?25l"
    SHOW_CURSOR = f"{CSI}?25h"

    # Modes

    FOREGROUND = 1
    BACKGROUND = 2

    def __init__(self) -> None:
        pass
    # art

    #def paint(self, mode: int, r: int, g: int, b: int) -> str:
    def paint(self, mode: int, id_color: int) -> str:
        if (mode == self.FOREGROUND):
            #return f"{self.CSI}38;2;{r};{g};{b}m"
            return f"{self.CSI}38;5;{id_color}m"
        return f"{self.CSI}48;5;{id_color}m"

    # Cursor

    def move_cursor(self, y: int, x: int) -> str:
        """Move cursor to grid coordinates (y, x),

        automatically applying 1-based indexing and
        2-character column width scaling.
        """
        terminal_row = y + 1
        terminal_col = (x * 2) + 1
        return f"{self.CSI}{terminal_row};{terminal_col}H"

    def print(self, string: str) -> None:
        if (string is None):
            raise Exception("str is not valid!")
        sys.stdout.write(string)
        sys.stdout.flush()

    def clear_terminal(self) -> None:
        os.system("clear")
