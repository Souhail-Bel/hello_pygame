import pygame
from hello_pygame.settings import RES_DIR


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(RES_DIR / "reimu.png")
        self.rect = self.image.get_rect()
        self.rect.center = (399, 500)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
