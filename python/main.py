import pygame
import numpy as np

WIDTH, HEIGHT = 100, 100
PIXEL_SIZE = 10

# defining colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

# Initializing grid with random 1s and 0s
GRID = np.random.choice([0, 1], size=(WIDTH, HEIGHT), p=[0.7, 0.3])


def draw_grid():
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
            pygame.draw.rect(SCREEN, GREY, rect, 1)


def count_neighbours(x, y):
    neighbours = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbours += GRID[(x + dx) % WIDTH][(y + dy) % HEIGHT]

    print(f"x: {x}, y: {y}, state: {GRID[x][y]}, neighbours: {int(neighbours)}")
    return int(neighbours)


pygame.init()
SCREEN = pygame.display.set_mode((WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Game of Life")
SCREEN.fill(BLACK)

pygame.display.flip()


def main():
    global GRID
    time = 0

    while True:
        NEWGRID = np.zeros((WIDTH, HEIGHT))

        for x in range(WIDTH):
            for y in range(HEIGHT):
                # drawing cells
                rect = pygame.Rect(x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
                pygame.draw.rect(SCREEN, WHITE if GRID[x][y] == 1 else BLACK, rect)

                neighbours = count_neighbours(x, y)

                # setting up grid for next timestep
                if GRID[x][y] == 1:
                    if neighbours in [2, 3]:
                        NEWGRID[x][y] = 1
                    else:
                        NEWGRID[x][y] = 0
                else:
                    if neighbours == 3:
                        NEWGRID[x][y] = 1
                    else:
                        NEWGRID[x][y] = 0

        GRID = NEWGRID

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        draw_grid()

        pygame.display.update()
        CLOCK.tick(5)
        time += 1


if __name__ == "__main__":
    main()
