from collections.abc import Generator
import pygame
from pygame.locals import *
from pygame.math import Vector2
from hello_pygame.entities import LivingSprite
from hello_pygame.settings import RES_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class InputManager:
    def __init__(self, rect: pygame.Rect, SPEED):
        self.rect = rect
        self.pos = Vector2(SCREEN_WIDTH / 2.0, 500.0)
        self.rect.center = round(self.pos.x), round(self.pos.y)
        self.SPEED = SPEED

    def handle_input(self, dt):

        pressed_keys = pygame.key.get_pressed()

        delta_pos = self.SPEED * dt

        # assert self.rect is not None
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.pos.x -= delta_pos

        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.pos.x += delta_pos

        if self.rect.bottom < SCREEN_HEIGHT and pressed_keys[K_DOWN]:
            self.pos.y += delta_pos

        if self.rect.top > 0 and pressed_keys[K_UP]:
            self.pos.y -= delta_pos

        self.rect.center = round(self.pos.x), round(self.pos.y)


class Player(LivingSprite, InputManager):
    def __init__(self):
        super().__init__(init_HP=3)

        self.sprites = []
        self.sprites.append(pygame.image.load(RES_DIR / "reimu_1.png"))
        self.sprites.append(pygame.image.load(RES_DIR / "reimu_2.png"))

        self.current_sprite = 0
        # 5 FPS
        self.ANIMATION_SPEED = 5

        self.image = self.sprites[self.current_sprite]
        # Type hinting is used cuz Python is gonna complain about it being None
        self.rect: pygame.Rect = self.image.get_rect()

        # speed in pixels/sec
        self.im: InputManager = InputManager(rect=self.rect, SPEED=300)

    def animate(self, dt):
        # incrementing by 1 will change  every single frame, too fast
        # Reimu's animation is 5 FPS, which takes 12 game loops (of the 60 FPS)
        # this means we have 0.083333, or 0.08 for short, for each frame
        # Note that it is frame-dependent
        # another possible solution is via delta time,
        # but that would impact update function as well
        self.current_sprite += self.ANIMATION_SPEED * dt
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def update(self, dt: float):
        if not self.is_alive:
            return

        self.animate(dt)
        self.im.handle_input(dt)

    def draw(self) -> Generator[tuple, None, None]:
        yield (self.image, self.rect)

    def on_damage(self):
        print("Ouchie")

    def on_death(self):
        self.rect.move_ip(0, 0)
        self.kill()
