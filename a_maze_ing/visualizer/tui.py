"""Terminal colors, cursor movement, and display helpers."""

import sys
import os
from dataclasses import dataclass


@dataclass
class Theme:
    """Define the colors used to render maze elements."""

    name: str
    close_wall: int
    open_wall: int
    path_wall: int
    entry_wall: int
    exit_wall: int


class Ansi():
    """Write ANSI terminal control sequences and colored output."""

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

    def paint(self, mode: int, id_color: int) -> str:
        """Return the ANSI color sequence for a foreground or background."""
        if (mode == self.FOREGROUND):
            return f"{self.CSI}38;5;{id_color}m"
        return f"{self.CSI}48;5;{id_color}m"

    def move_cursor(self, y: int, x: int) -> str:
        """Move cursor to grid coordinates (y, x),

        automatically applying 1-based indexing and
        2-character column width scaling.
        """
        terminal_row = y + 1
        terminal_col = (x * 2) + 1
        return f"{self.CSI}{terminal_row};{terminal_col}H"

    def print(self, string: str) -> None:
        """Write a string to standard output and flush it."""
        if (string is None):
            raise Exception("str is not valid!")
        sys.stdout.write(string)
        sys.stdout.flush()

    def clear_terminal(self) -> None:
        """Clear the terminal display."""
        os.system("clear")
