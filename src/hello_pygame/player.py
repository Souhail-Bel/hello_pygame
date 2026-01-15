from collections.abc import Generator
import pygame
from pygame.locals import *
from pygame.math import Vector2
from hello_pygame.entities import AnimatedSprite, LivingSprite
from hello_pygame.danmaku import Bullet
from hello_pygame.settings import IMG_DICT, SCREEN_HEIGHT, SCREEN_WIDTH


class Orb(AnimatedSprite):
    def __init__(self, side: int, bullet_group):
        super().__init__(sequence=IMG_DICT["orb"], animation_speed=4)
        self.side = side
        self.bullet_img = IMG_DICT["bullet"]
        self.bullet_group = bullet_group
        self.target_offset = Vector2(24.0 * self.side, -32.0)
        self.curr_offset = self.target_offset.copy()

    def update(self, dt: float, target: Vector2, is_focused: bool):
        self.animate(dt)
        self.curr_offset += (self.target_offset - self.curr_offset) * 7 * dt
        if is_focused:
            self.curr_offset.x = self.target_offset.x / 2
        self.rect.center = target + self.curr_offset

    def draw(self):
        yield (self.image, self.rect)

    def shoot(self):
        b = Bullet(self.rect.center, (0, -1), self.bullet_img, speed=600)
        self.bullet_group.add(b)


class Player(LivingSprite, AnimatedSprite):
    def __init__(self, bullet_group: pygame.sprite.Group):
        LivingSprite.__init__(self, init_HP=3)

        AnimatedSprite.__init__(self, sequence=IMG_DICT["reimu"], animation_speed=5)

        # MOVEMENT
        self.SPEED = 300  # pixels/sec
        self.pos = Vector2(SCREEN_WIDTH / 2, 500)
        self.rect.center = round(self.pos)
        self.is_focused = False

        # BULLETS
        bullet_rate = 25  # bullets / sec
        self.inv_bullet_rate = 1.0 / bullet_rate
        self.bullet_timer = 0.0
        self.bullet_group = bullet_group

        # ORBS
        self.orbs = [
            Orb(side=1, bullet_group=self.bullet_group),
            Orb(side=-1, bullet_group=self.bullet_group),
        ]

    def shoot(self):
        for orb in self.orbs:
            orb.shoot()

    def handle_input(self, dt):
        self.is_focused = False

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

            self.rect.center = round(self.pos)

        if pressed_keys[K_RSHIFT] or pressed_keys[K_LSHIFT]:
            self.is_focused = True

        if pressed_keys[K_x] and self.bullet_timer <= 0:
            self.bullet_timer = self.inv_bullet_rate
            self.shoot()

    def update(self, dt: float):
        if not self.is_alive:
            return
        self.bullet_timer -= dt
        self.animate(dt)
        for orb in self.orbs:
            orb.update(dt, self.pos, self.is_focused)
        self.handle_input(dt)

    def draw(self) -> Generator[tuple, None, None]:
        yield (self.image, self.rect)

        for orb in self.orbs:
            yield from orb.draw()

    def on_damage(self):
        print("Ouchie")

    def on_death(self):
        self.rect.move_ip(0, 0)
