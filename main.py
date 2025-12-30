import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 60
pyClock = pygame.time.Clock()

RED = (0xFF, 0, 0)
GREEN = (0, 0xFF, 0)
BLUE = (0, 0, 0xFF)
BLACK = (0, 0, 0)
WHITE = (0xFF, 0xFF, 0xFF)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_SURFACE.fill(WHITE)
pygame.display.set_caption("Very cool game")


def GameLoop():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        DISPLAY_SURFACE.fill(WHITE)
        pygame.display.update()
        pyClock.tick(FPS)


if __name__ == "__main__":
    print("Enjoy :3")
    GameLoop()
