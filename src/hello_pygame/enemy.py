from collections.abc import Generator
import pygame
from pygame.math import Vector2
from hello_pygame.entities import AnimatedSprite, LivingSprite
from hello_pygame.danmaku import *
from hello_pygame.settings import IMG_DICT, SCREEN_HEIGHT, SCREEN_WIDTH


class Enemy(LivingSprite, AnimatedSprite):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        init_HP=30,
        init_pos=None,
        init_vel=None,
        init_bullet_pattern=None,
    ):
        LivingSprite.__init__(self, init_HP=init_HP)
        AnimatedSprite.__init__(self, sequence=IMG_DICT["enemy_b"], animation_speed=12)

        self.__DEATH_MARGIN = 20

        if init_pos is None:
            init_pos = Vector2(SCREEN_WIDTH / 2, 50)

        if init_vel is None:
            init_vel = Vector2(0, 10)

        self.pos = Vector2(init_pos)
        self.vel = Vector2(init_vel)
        self.rect.center = round(self.pos)

        self.bullet_group = bullet_group
        self.bullet_img = IMG_DICT["bullet_ene"]

        if init_bullet_pattern is None:
            init_bullet_pattern = AimPattern(
                self.bullet_group, bullet_rate=5, accuracy=0.8
            )

        self.bullet_hell = init_bullet_pattern

    def update(self, dt: float, player_pos: Vector2):
        self.pos += self.vel * dt

        if (
            self.pos.y > SCREEN_HEIGHT + self.__DEATH_MARGIN
            or self.pos.x < self.__DEATH_MARGIN
            or self.pos.x > SCREEN_WIDTH + self.__DEATH_MARGIN
        ):
            self.kill()

        self.rect.center = round(self.pos)
        self.animate(dt)

        if self.bullet_hell.canShoot(dt):
            self.bullet_hell.shoot(self.pos, player_pos, self.bullet_img)

    def draw(self) -> Generator[tuple, None, None]:
        yield (self.image, self.rect)

    def on_death(self):
        self.kill()
