import pygame
import numpy as np

WIDTH, HEIGHT = 100, 100
PIXEL_SIZE = 10

# defining colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

# Initializing grid with random 1s and 0s
fraction_alive = 0.1
GRID = np.random.choice([1, 0], size=(WIDTH, HEIGHT), p=[fraction_alive, 1 - fraction_alive])


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

    return int(neighbours)


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

        TEXT = FONT.render(f"Time: {time}", True, (0, 255, 0))
        SCREEN.blit(TEXT, (0, 0))
        pygame.display.update()
        CLOCK.tick(100)
        time += 1


if __name__ == "__main__":
    main()
