from abc import ABC, abstractmethod
import random
from math import fabs, sin
import pygame
from pygame.math import Vector2
from hello_pygame.settings import IMG_DICT, SCREEN_HEIGHT, SCREEN_WIDTH, TAU


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        pos,
        b_dir,
        img=None,
        speed=400,
        accel=(0, 0),
        friction=1.0,
        angular_vel=0.0,
        flail=0.0,
        flail_freq=10,
        **kwargs,
    ):
        super().__init__()

        if img is None:
            self.image = IMG_DICT["bullet_ene"]
        else:
            self.image = img
        self.rect: pygame.Rect = self.image.get_rect()

        self.pos = Vector2(pos)
        self.vel = Vector2(b_dir)
        if self.vel.length() != 0.0:
            self.vel.normalize_ip()
            self.vel *= speed
        self.angular_vel = angular_vel
        self.friction = friction
        self.accel = Vector2(accel)

        self.lifetime = 0.0
        self.flail = flail
        self.flail_frequency = flail_freq

        self.__DEATH_MARGIN = 10

    def update(self, dt: float):
        self.lifetime += dt

        if self.friction != 1.0:
            self.vel *= self.friction

        self.vel += self.accel * dt

        if self.angular_vel != 0.0:
            self.vel.rotate_ip(self.angular_vel * dt)

        self.pos += self.vel * dt

        wobble = 0
        if self.flail != 0:
            wobble = self.flail * sin(self.lifetime * self.flail_frequency) * dt

        self.pos.x += wobble
        self.rect.center = round(self.pos)

        if not -self.__DEATH_MARGIN < self.pos.x < SCREEN_WIDTH + self.__DEATH_MARGIN:
            self.kill()
        if not -self.__DEATH_MARGIN < self.pos.y < SCREEN_HEIGHT + self.__DEATH_MARGIN:
            self.kill()

    def draw(self):
        yield (self.image, self.rect)


class DeployableBullet(Bullet):
    def __init__(
        self,
        start_pos,
        end_pos,
        deploy_duration: float,
        arrived_action="fall",
        target_pos=(0, 0),
        speed_final=400,
        interp=lambda x: x * (2 - x),
        **kwargs,
    ):
        super().__init__(pos=start_pos, b_dir=(0, 0), speed=0, **kwargs)

        self.start_pos = Vector2(start_pos)
        self.end_pos = Vector2(end_pos)

        self.deploy_duration = deploy_duration
        self.deploy_timer = 0.0
        self.deployed = False

        self.arrived_action = arrived_action
        self.target_pos = Vector2(target_pos)
        self.speed_final = speed_final

        # t = 1 + fabs(sin(-TAU * t)) / (-TAU * t)
        self.interp = interp

    def update(self, dt: float):
        self.deploy_timer += dt

        if self.deployed:
            return super().update(dt)

        if self.deploy_timer < self.deploy_duration:
            t = self.deploy_timer / self.deploy_duration

            # thx geogebra
            t = self.interp(t)

            self.pos = self.start_pos.lerp(self.end_pos, t)
            self.rect.center = round(self.pos)
        else:
            self.deployed = True
            self.pos = self.end_pos
            self.arrived_behaviour()

    def arrived_behaviour(self):
        if self.arrived_action == "fall":
            self.vel = Vector2(0, 1) * self.speed_final


class BulletPattern(ABC):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=400,
        bullet_rate=10,
        **kwargs,
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
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=400,
        bullet_rate=10,
        **kwargs,
    ):
        super().__init__(bullet_group, bullet_speed, bullet_rate, **kwargs)
        self.accuracy: float = kwargs.get("accuracy", 1.0)

    def shoot(self, shooter_pos, target_pos, bullet_img):

        bullet_dir = (target_pos - shooter_pos).normalize()

        if self.accuracy < 1.0:
            MAX_SPREAD_ANGLE = 180.0

            curr_spread = MAX_SPREAD_ANGLE * (1.0 - self.accuracy)
            offset = random.uniform(-curr_spread, curr_spread)
            bullet_dir.rotate_ip(offset)

        b = Bullet(shooter_pos, bullet_dir, bullet_img, self.bullet_speed)

        # b = Bullet(shooter_pos, (0, 0), bullet_img, 100, accel=(0, 10), flail=5)

        self.bullet_group.add(b)


class CirclePattern(BulletPattern):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=400,
        bullet_rate=20,
        **kwargs,
    ):
        super().__init__(bullet_group, bullet_speed, bullet_rate, **kwargs)
        self.count = kwargs.get("count", 14)
        self.angle_fraction: float = self.count / TAU

    def shoot(self, shooter_pos, target_pos, bullet_img):
        bullet_dir = Vector2(0, 1)
        for c in range(self.count):
            b = Bullet(shooter_pos, bullet_dir, bullet_img, self.bullet_speed)
            self.bullet_group.add(b)
            bullet_dir.rotate_rad_ip(self.angle_fraction)


class ConvergePattern(BulletPattern):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=400,
        bullet_rate=20,
        **kwargs,
    ):
        super().__init__(bullet_group, bullet_speed, bullet_rate, **kwargs)
        self.rows = kwargs.get("rows", 10)
        self.spread = kwargs.get("spread", 80)
        self.ang_vel_0 = kwargs.get("ang_vel_0", 30)
        self.center_rows = (self.rows - 1) / 2.0

    def shoot(self, shooter_pos, target_pos, bullet_img):
        for i in range(0, self.rows):
            offset_x = (i - self.center_rows) * self.spread
            bullet_pos = shooter_pos + Vector2(offset_x, 0)

            ang_vel = self.ang_vel_0 if offset_x > 0 else -self.ang_vel_0

            b = Bullet(
                bullet_pos,
                (0, 1),
                bullet_img,
                speed=self.bullet_speed,
                angular_vel=ang_vel,
            )
            self.bullet_group.add(b)


class RainPattern(BulletPattern):
    def shoot(self, shooter_pos, target_pos, bullet_img):
        self.inv_bullet_rate = 1.0 / 1
        row_count = 10
        row_width = 600
        spread = row_width / row_count

        for i in range(row_count):
            offset_x = (i - (row_count / 2)) * spread
            pos_to_fly_to = shooter_pos + Vector2(offset_x, 0)

            b = DeployableBullet(
                shooter_pos,
                pos_to_fly_to,
                deploy_duration=0.5,
                arrived_action="fall",
                speed_final=300,
                angular_vel=0,
            )
            self.bullet_group.add(b)
