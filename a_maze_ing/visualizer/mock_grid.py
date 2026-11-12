from typing import List

from maze_interpretor.maze_generator import Cell


MOCK_WALLS = (
    "9155553955155555393D3",
    "84553FAC3FAFFFFFC2812",
    "C1116FC56F85557F92C6A",
    "90043FFFFFAFFFFF8057A",
    "AE83E9553FAFD5552C516",
    "A92C3C396FAFFFFFA93C3",
    "C447C56C5545555546C56",
)


def build_mock_grid(width: int, height: int) -> List[List[Cell]]:
    """Build the fixed 21x7 visual fixture with a closed-cell 42 pattern."""
    if width != 21 or height != 7:
        raise ValueError("The mock maze requires WIDTH=21 and HEIGHT=7")

    return [
        [
            Cell(x=x, y=y, walls=int(walls, 16))
            for x, walls in enumerate(row)
        ]
        for y, row in enumerate(MOCK_WALLS)
    ]
