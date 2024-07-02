import pygame
import numpy as np
from common import draw_pixel, pygame_setup, next_step
from common import ARGS
from common import WIDTH, HEIGHT
from common import BLACK, WHITE, GREY, GREEN


# setting up pygame objects
SCREEN, CLOCK, FONT = pygame_setup()


def main():
    time = 0
    fraction_alive = float(ARGS.ratio)

    # Initializing grid with random 1s and 0s
    GRID = np.array(
        np.random.choice([1, 0], size=(WIDTH * HEIGHT), p=[fraction_alive, 1 - fraction_alive]),
        dtype=np.ushort,
    )

    while True:
        # Initialize grid for next step
        NEWGRID = np.zeros(WIDTH * HEIGHT, dtype=np.ushort)

        for i in range(WIDTH * HEIGHT):
            draw_pixel(SCREEN, i, WHITE if GRID[i] == 1 else BLACK, False)  # draw cell
            draw_pixel(SCREEN, i, GREY, True)  # draw background
            next_step(i, GRID, NEWGRID)  # calculate grid for next step

        GRID = NEWGRID

        # checking for exit condition and displaying clock
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
