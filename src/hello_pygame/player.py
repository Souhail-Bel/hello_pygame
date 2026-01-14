import pygame
from pygame.locals import *
from hello_pygame.entities import LivingSprite
from hello_pygame.settings import RES_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class InputManager:
    def __init__(self, rect: pygame.Rect, SPEED):
        self.rect = rect
        self.SPEED = SPEED

    def handle_input(self):

        pressed_keys = pygame.key.get_pressed()

        # assert self.rect is not None
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-self.SPEED, 0)

        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(self.SPEED, 0)

        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, self.SPEED)

        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -self.SPEED)


class Player(LivingSprite, InputManager):
    def __init__(self):
        super().__init__(init_HP=3)

        self.sprites = []
        self.sprites.append(pygame.image.load(RES_DIR / "reimu_1.png"))
        self.sprites.append(pygame.image.load(RES_DIR / "reimu_2.png"))

        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        # Type hinting is used cuz Python is gonna complain about it being None
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 500)

        # self.SPEED = 5
        self.im: InputManager = InputManager(rect=self.rect, SPEED=5)

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
        if not self.is_alive:
            return

        self.animate()
        self.im.handle_input()

    def draw(self) -> tuple:
        return (self.image, self.rect)

    def on_damage(self):
        print("Ouchie")

    def on_death(self):
        self.rect.move_ip(0, 0)
        self.kill()
