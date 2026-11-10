import sys
from typing import Optional


class Ansi():

    ESC = "\x1b"
    CSI = f"{ESC}["  # Control Sequence Introducer

    # buffer
    # CREATE_ALTER_BUFFER = f"{CSI}?1049h"
    # DESTROY_ALTER_BUFFER = f"{CSI}?1049l"

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

    def paint(self, mode: int, r: int, g: int, b: int) -> Optional[str]:
        if (mode == self.FOREGROUND):
            return f"{self.CSI}38;2;{r};{g};{b}m"
        elif (mode == self.BACKGROUND):
            return f"{self.CSI}48;2;{r};{g};{b}m"
        return None

    # Cursor

    def move_cursor(self, line: int, column: int) -> str:
        return f"{self.CSI}{line};{column}H"  # or ending with f

    def print(self, ansi_sintaxe: str) -> None:
        if (ansi_sintaxe is None):
            raise Exception("ansi_sintaxe is not valid!")
        sys.stdout.write(ansi_sintaxe)
        sys.stdout.flush()
