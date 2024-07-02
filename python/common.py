from typing import Tuple
from argparse import ArgumentParser
import pygame
import numpy as np

parser = ArgumentParser(
    prog="Game Of Life",
    description="Conway's Game of Life, Python version.",
    epilog="For MPI runs, launch with `mpirun -n <nproc> main.py <width> <height>`",
)

parser.add_argument("width", help="grid width")
parser.add_argument("height", help="grid height")
parser.add_argument("-r", "--ratio", help="fraction of 'live' cells at startup", default=0.2)

ARGS = parser.parse_args()

#################
# Display setup #
#################
WIDTH, HEIGHT = int(ARGS.width), int(ARGS.height)
PIXEL_SIZE = 5

# defining colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


def pygame_setup() -> Tuple[
    pygame.Surface,
    pygame.time.Clock,
    pygame.font.Font,
]:
    """Initialize Pygame objects such as screen, clock and font

    Returns
    -------
    pygame.Surface
        Surface on which to display the cells
    pygame.time.Clock
        Clock for in-game timing
    pygame.font.Font
        Font for displaying messages
    """

    pygame.init()
    pygame.font.init()

    FONT = pygame.font.SysFont("consolas.ttf", 24)
    SCREEN = pygame.display.set_mode((WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("Game of Life")

    SCREEN.fill(BLACK)
    pygame.display.flip()

    return SCREEN, CLOCK, FONT


def draw_pixel(
    screen: pygame.Surface,
    position: int,
    color: Tuple[int, int, int],
    hollow: bool = False,
) -> None:
    """Draw a cell at a certain position, of a given color, optionally hollow/filled

    x, y coordinates are calculate as:
    x = position % WIDTH
    y = position // WIDTH

    Parameters
    ----------
    screen : pygame.Surface
        pygame Surface on which to draw the pixel
    position : int
        position of the cell on the grid
    color : Tuple[int, int, int]
        RGB code of the wanted color
    hollow : bool, optional
        toggles hollow (False) or filled (True) pixel, by default False
    """
    x, y = position % WIDTH, position // WIDTH
    rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
    pygame.draw.rect(screen, color, rect, 1 if hollow else 0)


def count_neighbours(grid: np.ndarray, position: int) -> int:
    """Count neighbours for cell in a certain position

    Parameters
    ----------
    grid : np.ndarray
        grid used for fetching neighbours
    position : int
        position of the cell for which to calculate the number of neighbours

    Returns
    -------
    int
        number of neighbours for the cell
    """

    neighbours = 0

    for step in [
        -1,  # left
        # 0, self, avoid counting
        +1,  # right
        WIDTH - 1,  # up-left
        WIDTH,  # up
        WIDTH + 1,  # up-right
        -WIDTH - 1,  # down-left
        -WIDTH,  # down
        -WIDTH + 1,  # down-right
    ]:
        neighbours += grid[
            (position + step + WIDTH * HEIGHT) % (WIDTH * HEIGHT)
        ]  # WIDTH * HEIGHT needed for periodicity

    return neighbours


def next_step(position: int, grid: np.ndarray) -> bool:
    """Update cells for the next timestep based on game rules:

    1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    2. Any live cell with two or three live neighbours lives on to the next generation.
    3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

    Parameters
    ----------
    position : int
        position of the cell to be evaluated
    grid : np.ndarray
        grid on which the game is played

    Returns
    -------
    bool
        whether that cell is dead (0) or alive (1)
    """
    neighbours = count_neighbours(grid, position)

    if grid[position] == 1:
        if neighbours in [2, 3]:
            return 1
    else:
        if neighbours == 3:
            return 1

    return 0
