from collections.abc import Generator
import pygame
from pygame.locals import *
from pygame.math import Vector2
from hello_pygame.entities import LivingSprite
from hello_pygame.items import Bullet
from hello_pygame.settings import IMG_DICT, SCREEN_HEIGHT, SCREEN_WIDTH


class Player(LivingSprite):
    def __init__(self, bullet_group):
        super().__init__(init_HP=3)

        # ANIMATION
        self.sprites = IMG_DICT["reimu"]
        self.current_sprite = 0
        self.ANIMATION_SPEED = 5  # FPS
        self.image = self.sprites[self.current_sprite]
        # Type hinting is used cuz Python is gonna complain about it being None
        self.rect: pygame.Rect = self.image.get_rect(center=(SCREEN_WIDTH / 2.0, 500.0))

        # MOVEMENT
        self.SPEED = 300  # pixels/sec
        self.pos = Vector2(self.rect.center)

        # BULLETS
        self.bullet_group = bullet_group
        self.bullet_img = IMG_DICT["bullet"]
        self.bullet_rate = 25  # bullets / sec
        self.bullet_timer = 0.0

    def shoot(self):
        b = Bullet(self.pos, (0, -1), self.bullet_img, speed=500)
        self.bullet_group.add(b)

    def handle_input(self, dt):

        pressed_keys = pygame.key.get_pressed()

        move_dir = Vector2(0, 0)

        if pressed_keys[K_LEFT]:
            move_dir.x -= 1
        if pressed_keys[K_RIGHT]:
            move_dir.x += 1
        if pressed_keys[K_UP]:
            move_dir.y -= 1
        if pressed_keys[K_DOWN]:
            move_dir.y += 1

        if move_dir != Vector2(0, 0):
            self.pos += move_dir.normalize() * self.SPEED * dt

            self.pos.x = max(0, min(SCREEN_WIDTH, self.pos.x))
            self.pos.y = max(0, min(SCREEN_HEIGHT, self.pos.y))

            self.rect.center = round(self.pos.x), round(self.pos.y)

        if pressed_keys[K_x] and self.bullet_timer <= 0:
            self.bullet_timer = 1.0 / self.bullet_rate
            self.shoot()

    def animate(self, dt):
        self.current_sprite += self.ANIMATION_SPEED * dt
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

    def update(self, dt: float):
        if not self.is_alive:
            return
        self.bullet_timer -= dt
        self.animate(dt)
        self.handle_input(dt)

    def draw(self) -> Generator[tuple, None, None]:
        yield (self.image, self.rect)

    def on_damage(self):
        print("Ouchie")

    def on_death(self):
        self.rect.move_ip(0, 0)
