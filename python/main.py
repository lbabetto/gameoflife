import pygame
import numpy as np
from typing import Tuple
from mpi4py import MPI

#################
# Display setup #
#################
WIDTH, HEIGHT = 200, 150
PIXEL_SIZE = 5

# defining colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#############
# MPI setup #
#############
comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank = comm.Get_rank()

# dividing cells among processes
N = WIDTH * HEIGHT
rem = N % nprocs
nitems = (N - rem) // nprocs
if rank < rem:
    nitems += 1

# calculating starting index
start = rank * nitems
if rank >= rem:
    start += rem

################
# Pygame setup #
################
if rank == 0:
    pygame.init()
    pygame.font.init()

    FONT = pygame.font.SysFont("consolas.ttf", 24)
    SCREEN = pygame.display.set_mode((WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE))
    CLOCK = pygame.time.Clock()
    pygame.display.set_caption("Game of Life")

    SCREEN.fill(BLACK)
    pygame.display.flip()


def draw_pixel(position: int, color: Tuple[int, int, int], hollow: bool = False) -> None:
    """Draw a cell at a certain position, of a given color, optionally hollow/filled

    x, y coordinates are calculate as:
    x = position % WIDTH
    y = position // WIDTH

    Parameters
    ----------
    position : int
        position of the cell on the grid
    color : Tuple[int, int, int]
        RGB code of the wanted color
    hollow : bool, optional
        toggles hollow (False) or filled (True) pixel, by default False
    """
    x, y = position % WIDTH, position // WIDTH
    rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
    pygame.draw.rect(SCREEN, color, rect, 1 if hollow else 0)


def main():
    # Initializing grid with random 1s and 0s
    if rank == 0:
        time = 0
        fraction_alive = 0.2
        GRID = np.array(
            np.random.choice([1, 0], size=(WIDTH * HEIGHT), p=[fraction_alive, 1 - fraction_alive]),
            dtype=np.ushort,
        )
    else:
        GRID = np.empty((WIDTH * HEIGHT), dtype=np.ushort)
    comm.Bcast(GRID, root=0)

    while True:
        # render cells
        if rank == 0:
            for i in range(WIDTH * HEIGHT):
                draw_pixel(start + i, WHITE if GRID[i] == 1 else BLACK, hollow=False)

        # Initialize grid for next step (split by process rank)
        NEWGRID = np.zeros(nitems, dtype=np.ushort)

        # calculate neighbours for each cell in process rank and store data in new grid
        for i in range(nitems):
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
                neighbours += GRID[
                    (start + i + step + WIDTH * HEIGHT) % (WIDTH * HEIGHT)
                ]  # WIDTH * HEIGHT needed for periodicity

            # NEWGRID[i] = 0
            if GRID[start + i] == 1:
                if neighbours in [2, 3]:
                    NEWGRID[i] = 1

            else:
                if neighbours == 3:
                    NEWGRID[i] = 1

        comm.Allgatherv(NEWGRID, GRID)

        # drawing background grid
        if rank == 0:
            for i in range(WIDTH * HEIGHT):
                draw_pixel(start + i, GREY, hollow=True)

        # checking for exit condition and displaying clock
        if rank == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            TEXT = FONT.render(f"Time: {time}", True, GREEN)
            SCREEN.blit(TEXT, (0, 0))
            pygame.display.update()
            CLOCK.tick(30)  # FPS

            time += 1


if __name__ == "__main__":
    main()
