import pygame
from pygame.locals import *
from hello_pygame.settings import RES_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.sprites = []
        self.sprites.append(pygame.image.load(RES_DIR / "reimu_1.png"))
        self.sprites.append(pygame.image.load(RES_DIR / "reimu_2.png"))

        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (399, 500)

    def animate(self):
        # incrementing by 1 will change  every single frame, too fast
        # Reimu's animation is 5 FPS, which takes 12 game loops (of the 60 FPS)
        # this means we have 0.083333, or 0.08 for short, for each frame
        # Note that it is frame-dependent
        # another possible solution is via delta time,
        # but that would impact update function as well
        self.current_sprite = (self.current_sprite + 0.08) % len(self.sprites)
        self.image = self.sprites[int(self.current_sprite)]

    def update(self):
        assert self.rect is not None
        self.animate()

        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)

        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
