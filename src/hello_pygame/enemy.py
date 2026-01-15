from collections.abc import Generator
import pygame
from pygame.math import Vector2
from hello_pygame.entities import AnimatedSprite, LivingSprite
from hello_pygame.danmaku import Bullet
from hello_pygame.settings import IMG_DICT, SCREEN_HEIGHT, SCREEN_WIDTH


class Enemy(LivingSprite, AnimatedSprite):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        init_pos=Vector2(SCREEN_WIDTH / 2.0, 50),
        init_vel=Vector2(0, 10),
    ):
        LivingSprite.__init__(self, init_HP=20)
        AnimatedSprite.__init__(self, sequence=IMG_DICT["enemy_b"], animation_speed=12)

        self.__DEATH_MARGIN = 10
        self.rect.center = init_pos
        self.pos = Vector2(self.rect.center)
        self.vel = init_vel

        self.bullet_group = bullet_group
        self.bullet_img = IMG_DICT["bullet_ene"]

        bullet_rate = 5
        self.inv_bullet_rate = 1.0 / bullet_rate
        self.bullet_timer: float = 0.0

    def update(self, dt: float, player_pos: Vector2):
        self.pos += self.vel * dt
        if (
            -self.__DEATH_MARGIN < self.pos.x < SCREEN_WIDTH + self.__DEATH_MARGIN
            or -self.__DEATH_MARGIN < self.pos.y < SCREEN_HEIGHT + self.__DEATH_MARGIN
        ):
            self.kill()

        self.rect.center = round(self.pos)
        self.animate(dt)

        self.bullet_timer -= dt
        if self.bullet_timer <= 0:
            self.bullet_timer = self.inv_bullet_rate
            self.shoot_player(player_pos)

    def shoot(self):
        b = Bullet(self.pos, (0, 1), self.bullet_img, 100)
        self.bullet_group.add(b)

    def shoot_player(self, player_pos: Vector2, speed=100):
        bullet_direction = (player_pos - self.pos).normalize()
        b = Bullet(self.pos, bullet_direction, self.bullet_img, speed)
        self.bullet_group.add(b)

    def draw(self) -> Generator[tuple, None, None]:
        yield (self.image, self.rect)
