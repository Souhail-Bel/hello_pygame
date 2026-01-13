import pygame, sys
from pygame.locals import *
from hello_pygame.gfx import Background
from hello_pygame.player import Player
from hello_pygame.settings import *


def main():

    pygame.init()

    pyClock = pygame.time.Clock()

    DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Very cool game")

    print("Enjoy :3")

    P1 = Player()
    BG = Background()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        P1.update()

        # DISPLAY_SURFACE.fill(BG_COLOR)

        BG.draw_sky(DISPLAY_SURFACE)
        BG.draw_landscape(DISPLAY_SURFACE)
        BG.draw_tower(DISPLAY_SURFACE)

        P1.draw(DISPLAY_SURFACE)

        pygame.display.update()
        pyClock.tick(FPS)


if __name__ == "__main__":
    main()
