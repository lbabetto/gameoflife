import pygame
import numpy as np
from common import draw_pixel, pygame_setup, count_neighbours, next_step
from common import ARGS
from common import WIDTH, HEIGHT
from common import BLACK, WHITE, GREEN, GREY
from mpi4py import MPI


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

# setting up pygame objects
if rank == 0:
    SCREEN, CLOCK, FONT = pygame_setup()


def main():
    # Initializing grid with random 1s and 0s
    if rank == 0:
        time = 0
        fraction_alive = float(ARGS.ratio)
        GRID = np.array(
            np.random.choice([1, 0], size=(WIDTH * HEIGHT), p=[fraction_alive, 1 - fraction_alive]),
            dtype=np.ushort,
        )
    else:
        GRID = np.empty((WIDTH * HEIGHT), dtype=np.ushort)
    comm.Bcast(GRID, root=0)

    while True:
        if rank == 0:
            for i in range(WIDTH * HEIGHT):
                draw_pixel(SCREEN, start + i, WHITE if GRID[i] == 1 else BLACK, hollow=False)  # draw cell
                draw_pixel(SCREEN, start + i, GREY, hollow=True)  # draw background

        # Initialize grid for next step (split by process rank)
        NEWGRID = np.zeros(nitems, dtype=np.ushort)

        # calculate neighbours for each cell in process rank
        for i in range(nitems):
            next_step(i, GRID, NEWGRID)

        comm.Allgatherv(NEWGRID, GRID)

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
