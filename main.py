import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 60
pyClock = pygame.time.Clock()

BG_COLOR = (0xC0, 0xC0, 0xC0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_SURFACE.fill(BG_COLOR)
pygame.display.set_caption("Very cool game")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("res/reimu.png")
        self.rect = self.image.get_rect()
        self.rect.center = (400, 500)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def GameLoop():
    P1 = Player()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY_SURFACE.fill(BG_COLOR)
        P1.draw(DISPLAY_SURFACE)

        pygame.display.update()
        pyClock.tick(FPS)


if __name__ == "__main__":
    print("Enjoy :3")
    GameLoop()
