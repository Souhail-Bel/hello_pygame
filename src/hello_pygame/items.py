import pygame
from pygame.math import Vector2
from hello_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, dir, img, speed=400):
        super().__init__()

        self.image = img
        self.rect: pygame.Rect = self.image.get_rect()
        self.pos = Vector2(pos)
        self.vel = speed * Vector2(dir).normalize()
        # if it goes 10 pixels out of the screen (either X or Y), it dies
        self.__DEATH_MARGIN = 50

    def update(self, dt: float):
        self.pos += self.vel * dt
        self.rect.center = round(self.pos.x), round(self.pos.y)

        if not 0 < self.pos.x + self.__DEATH_MARGIN < SCREEN_WIDTH:
            self.kill()
        if not 0 < self.pos.y + self.__DEATH_MARGIN < SCREEN_HEIGHT:
            self.kill()

    def draw(self):
        yield (self.image, tuple(self.pos))
