from abc import ABC, abstractmethod
import pygame
from pygame.math import Vector2
from hello_pygame.settings import SCREEN_HEIGHT, SCREEN_WIDTH, TAU


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, b_dir, img, speed=400):
        super().__init__()

        self.image = img
        self.rect: pygame.Rect = self.image.get_rect()
        self.pos = Vector2(pos)
        self.vel = speed * Vector2(b_dir).normalize()
        self.__DEATH_MARGIN = 10

    def update(self, dt: float):
        self.pos += self.vel * dt
        self.rect.center = round(self.pos)

        if not -self.__DEATH_MARGIN < self.pos.x < SCREEN_WIDTH + self.__DEATH_MARGIN:
            self.kill()
        if not -self.__DEATH_MARGIN < self.pos.y < SCREEN_HEIGHT + self.__DEATH_MARGIN:
            self.kill()

    def draw(self):
        yield (self.image, self.rect)


class BulletPattern(ABC):
    def __init__(
        self, bullet_group: pygame.sprite.Group, bullet_speed=400, bullet_rate=10
    ):
        self.bullet_group = bullet_group
        self.bullet_speed = bullet_speed
        self.inv_bullet_rate = 1.0 / bullet_rate
        self.timer = 0.0

    def canShoot(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = self.inv_bullet_rate
            return True
        return False

    @abstractmethod
    def shoot(self, shooter_pos, target_pos, bullet_img):
        pass


class StreamPattern(BulletPattern):
    def shoot(self, shooter_pos, target_pos, bullet_img):
        b = Bullet(shooter_pos, (0, -1), bullet_img, self.bullet_speed)
        self.bullet_group.add(b)


class AimPattern(BulletPattern):
    def shoot(self, shooter_pos, target_pos, bullet_img):
        bullet_dir = (target_pos - shooter_pos).normalize()
        b = Bullet(shooter_pos, bullet_dir, bullet_img, self.bullet_speed)
        self.bullet_group.add(b)


class CirclePattern(BulletPattern):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=400,
        bullet_rate=20,
        count=14,
    ):
        super().__init__(bullet_group, bullet_speed, bullet_rate)
        self.count = count
        self.angle_fraction: float = self.count / TAU

    def shoot(self, shooter_pos, target_pos, bullet_img):
        bullet_dir = Vector2(0, 1)
        for c in range(self.count):
            b = Bullet(shooter_pos, bullet_dir, bullet_img, self.bullet_speed)
            self.bullet_group.add(b)
            bullet_dir.rotate_rad_ip(self.angle_fraction)
