import itertools
import pygame, sys
from pygame.locals import *
from hello_pygame.gfx import Background
from hello_pygame.player import Player
from hello_pygame.settings import *


def main():

    pygame.init()

    pyClock = pygame.time.Clock()

    DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    display_buffer = []
    pygame.display.set_caption("Very cool game")

    print("Enjoy :3")

    P1 = Player()
    BG = Background()

    bg_buffer = BG.draw_sky()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    P1.damage()

        P1.update()

        # display_buffer = [BG.draw_landscape(), *BG.draw_tower(), P1.draw()]
        display_buffer = itertools.chain(
            BG.draw_landscape(), BG.draw_tower(), P1.draw()
        )

        DISPLAY_SURFACE.fblits(bg_buffer)
        DISPLAY_SURFACE.fblits(display_buffer)

        pygame.display.update()
        pyClock.tick(FPS)


if __name__ == "__main__":
    main()
