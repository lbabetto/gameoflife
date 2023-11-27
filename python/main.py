import pygame
import numpy as np
from itertools import product

from typing import Tuple

WIDTH, HEIGHT = 300, 200
PIXEL_SIZE = 5

# defining colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

# Initializing grid with random 1s and 0s
fraction_alive = 0.1
GRID = np.random.choice([1, 0], size=(WIDTH, HEIGHT), p=[fraction_alive, 1 - fraction_alive])


def draw_pixel(coords: Tuple[int, int], color: Tuple[int, int, int], hollow: bool = False):
    """Draw a pixel at position (x,y) of a given color, optionally hollow/filled

    Parameters
    ----------
    coords : Tuple[int, int]
        (x,y) coords on grid
    color : Tuple[int, int, int]
        RGB code of the wanted color
    hollow : bool, optional
        toggles hollow (False) or filled (True) pixel, by default False
    """
    x, y = coords

    rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
    pygame.draw.rect(SCREEN, color, rect, 1 if hollow else 0)


def draw_grid() -> None:
    """Draw a grey grid"""
    for x, y in product(range(WIDTH), range(HEIGHT)):
        draw_pixel((x, y), GREY, True)


def count_neighbours(coords: Tuple[int, int]) -> int:
    """Count the number of neighbouring alive cells

    Parameters
    ----------
    coords : Tuple[int, int]
        (x,y) coords on grid

    Return
    ------
    int
        number of neighbouring live cells
    """
    x, y = coords
    neighbours = 0

    for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
        if dx == 0 and dy == 0:
            continue
        neighbours += GRID[(x + dx) % WIDTH][(y + dy) % HEIGHT]

    return int(neighbours)


def next_step(coords: Tuple[int, int]):
    """Calculate alive/dead cells for the next step

    Parameters
    ----------
    coords : Tuple[int, int]
        (x,y) coords on grid


    Return
    NDArray[float64]
        grid at the next step
    ------
    """
    x, y = coords

    neighbours = count_neighbours(coords)

    if GRID[x][y] == 1:
        if neighbours in [2, 3]:
            NEWGRID[x][y] = 1
    else:
        if neighbours == 3:
            NEWGRID[x][y] = 1


pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("consolas.ttf", 24)
SCREEN = pygame.display.set_mode((WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Game of Life")
SCREEN.fill(BLACK)

pygame.display.flip()


def main():
    global GRID
    time = 0

    while True:
        # drawing cells
        for x, y in product(range(WIDTH), range(HEIGHT)):
            rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
            pygame.draw.rect(SCREEN, WHITE if GRID[x][y] == 1 else BLACK, rect)

        # setting up next step
        global NEWGRID
        NEWGRID = np.zeros((WIDTH, HEIGHT))
        for x, y in product(range(WIDTH), range(HEIGHT)):
            next_step((x, y))
        GRID = NEWGRID

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # drawing background grid
        draw_grid()

        TEXT = FONT.render(f"Time: {time}", True, (0, 255, 0))
        SCREEN.blit(TEXT, (0, 0))
        pygame.display.update()
        CLOCK.tick(100)
        time += 1


if __name__ == "__main__":
    main()
