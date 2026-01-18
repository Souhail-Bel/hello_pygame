from abc import ABC, abstractmethod
import random
from math import fabs, sin
import pygame
from pygame.math import Vector2
from hello_pygame.settings import IMG_DICT, SCREEN_HEIGHT, SCREEN_WIDTH, TAU


# Normal vs Deployable:
#     normal spawn instantly, while deployable follow a lerping function to arrive at their positions before starting some action
#
# Format:
#     PatternClassName: description
#         "name_in_script"
#         [argument_1, argument_2, ...]
#
# Example of pattern action in script:
# "pattern aim 0.8"
# this means start the AimPattern at 80% accuracy
#
#
# Normal patterns:
#     StreamPattern: streams down bullets
#         "stream"
#         []
#     AimPattern: aims at player given an accuracy
#         "aim"
#         [accuracy]
#     CirclePattern: extending circle given bullets count
#         "circle"
#         [count]
#     ConvergePattern: spawns spread out rows of bullets that close on each other
#         "converge"
#         [rows, spread, ang_vel_0]
#
# Deployable patterns:
#     RainPattern: similar to ConvergePattern, but with flailing
#         "rain"
#         [row_count, rain_width]
#     FishingPattern: try and catch the player like a fishing net of radius and around the circle count
#         "fish"
#         [radius, count]
#     BlossomPattern: galaxy like pattern extending from enemy
#         "blossom"
#         [radius, count]
#     CircleConvergePattern: a combination of the circle and converge patterns :P
#         "cc"
#         [radius, count]

# TODO add check for when value goes out of bounds for given pattern

PATTERN_REG = {
    # Normal
    "stream": lambda g, args: StreamPattern(g),
    "aim": lambda g, args: AimPattern(g, accuracy=float(args[0]) if args else 1.0),
    "circle": lambda g, args: CirclePattern(g, count=int(args[0]) if args else 14),
    "converge": lambda g, args: ConvergePattern(
        g,
        rows=int(args[0]) if len(args) > 0 else 10,
        spread=int(args[1]) if len(args) > 1 else 80,
        ang_vel_0=int(args[2]) if len(args) > 2 else 30,
    ),
    # Deployable
    "rain": lambda g, args: RainPattern(
        g,
        row_count=int(args[0]) if len(args) > 0 else 12,
        rain_width=int(args[1]) if len(args) > 1 else 750,
    ),
    "fish": lambda g, args: FishingPattern(
        g,
        radius=int(args[0]) if len(args) > 0 else 100,
        count=int(args[1]) if len(args) > 1 else 16,
    ),
    "blossom": lambda g, args: BlossomPattern(
        g,
        radius=int(args[0]) if len(args) > 0 else 100,
        count=int(args[1]) if len(args) > 1 else 32,
    ),
    "cc": lambda g, args: CircleConvergePattern(
        g,
        radius=int(args[0]) if len(args) > 0 else 100,
        count=int(args[1]) if len(args) > 1 else 32,
    ),
}


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
        angular_drag=1.0,
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
        self.angular_drag = angular_drag
        self.friction = friction
        self.accel = Vector2(accel)

        self.lifetime = 0.0
        self.flail = flail
        self.flail_frequency = flail_freq

        self.__DEATH_MARGIN = 50

        self.on_spawn()

    def update(self, dt: float):
        self.lifetime += dt

        if self.friction != 1.0:
            self.vel *= self.friction

        self.vel += self.accel * dt

        if self.angular_vel != 0.0:
            self.vel.rotate_ip(self.angular_vel * dt)

            self.angular_vel *= self.angular_drag

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

    def on_spawn(self):
        # for playing sound effect later
        pass


class DeployableBullet(Bullet):
    def __init__(
        self,
        start_pos,
        end_pos,
        deploy_duration: float,
        wait_duration=0.0,
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
        # self.wait_duraion = wait_duration
        self.wake_moment = wait_duration + deploy_duration

        self.timer = 0.0
        self.deployed = False

        self.arrived_action = arrived_action
        self.target_pos = Vector2(target_pos)
        self.speed_final = speed_final

        # t = 1 + fabs(sin(-TAU * t)) / (-TAU * t)
        self.interp = interp

    def update(self, dt: float):
        self.timer += dt

        if self.deployed:
            return super().update(dt)

        if self.timer < self.deploy_duration:
            t = self.timer / self.deploy_duration

            # thx geogebra
            t = self.interp(t)

            self.pos = self.start_pos.lerp(self.end_pos, t)
            self.rect.center = round(self.pos)
        elif self.timer < self.wake_moment:
            pass

        else:
            self.deployed = True
            self.pos = self.end_pos
            self.on_deploy()

    def on_deploy(self):
        if self.arrived_action == "fall":
            self.vel = Vector2(0, 1) * self.speed_final
        elif self.arrived_action == "aim":
            self.vel = (self.target_pos - self.end_pos).normalize() * self.speed_final


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
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=200,
        bullet_rate=4,
        **kwargs,
    ):
        super().__init__(bullet_group, bullet_speed, bullet_rate, **kwargs)

    def shoot(self, shooter_pos, target_pos, bullet_img):
        b = Bullet(shooter_pos, (0, 1), bullet_img, self.bullet_speed)
        self.bullet_group.add(b)


class AimPattern(BulletPattern):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=200,
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

        self.bullet_group.add(b)


class CirclePattern(BulletPattern):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=100,
        bullet_rate=2,
        **kwargs,
    ):
        super().__init__(bullet_group, bullet_speed, bullet_rate, **kwargs)
        self.count = kwargs.get("count", 14)
        self.angle_fraction: float = TAU / self.count

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
        bullet_speed=200,
        bullet_rate=2,
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
                angular_drag=0.99,
            )
            self.bullet_group.add(b)


class RainPattern(BulletPattern):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=100,
        bullet_rate=1,
        **kwargs,
    ):
        super().__init__(bullet_group, bullet_speed, bullet_rate, **kwargs)
        self.row_count = kwargs.get("row_count", 12)
        self.rain_width = kwargs.get("rain_width", 750)
        self.center_rows = self.row_count / 2
        self.spread = self.rain_width / self.row_count

    def shoot(self, shooter_pos, target_pos, bullet_img):

        for i in range(self.row_count):
            offset_x = (i - self.center_rows) * self.spread
            pos_to_fly_to = shooter_pos + Vector2(offset_x, 0)

            b = DeployableBullet(
                shooter_pos,
                pos_to_fly_to,
                deploy_duration=1.5,
                wait_duration=0.5,
                arrived_action="fall",
                speed_final=self.bullet_speed,
                flail=100,
                flail_freq=5,
                angular_vel=0,
            )
            self.bullet_group.add(b)


class FishingPattern(BulletPattern):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=100,
        bullet_rate=1,
        **kwargs,
    ):
        super().__init__(bullet_group, bullet_speed, bullet_rate, **kwargs)
        self.radius = kwargs.get("radius", 100)
        self.count = kwargs.get("count", 16)
        self.angle_fraction = 360 / self.count

    def shoot(self, shooter_pos, target_pos, bullet_img):

        for i in range(self.count):
            angle = i * self.angle_fraction
            deploy_pos = target_pos + Vector2(self.radius, 0).rotate(angle)

            b = DeployableBullet(
                shooter_pos,
                deploy_pos,
                deploy_duration=2.5,
                wait_duration=1.0,
                arrived_action="aim",
                speed_final=self.bullet_speed,
                target_pos=target_pos,
            )

            self.bullet_group.add(b)


class BlossomPattern(BulletPattern):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=100,
        bullet_rate=2,
        **kwargs,
    ):
        super().__init__(bullet_group, bullet_speed, bullet_rate, **kwargs)
        self.radius = kwargs.get("radius", 100)
        self.count = kwargs.get("count", 32)
        self.angle_fraction = 360 / self.count

    def shoot(self, shooter_pos, target_pos, bullet_img):

        for i in range(self.count):
            angle = i * self.angle_fraction
            deploy_pos = shooter_pos + Vector2(self.radius, 0).rotate(angle)

            b = DeployableBullet(
                shooter_pos,
                deploy_pos,
                deploy_duration=0.5,
                wait_duration=0.5,
                arrived_action="aim",
                speed_final=self.bullet_speed,
                target_pos=shooter_pos,
                angular_vel=150,
                angular_drag=0.99,
            )

            self.bullet_group.add(b)


class CircleConvergePattern(BulletPattern):
    def __init__(
        self,
        bullet_group: pygame.sprite.Group,
        bullet_speed=100,
        bullet_rate=2,
        **kwargs,
    ):
        super().__init__(bullet_group, bullet_speed, bullet_rate, **kwargs)
        self.radius = kwargs.get("radius", 100)
        self.count = kwargs.get("count", 32)
        self.angle_fraction = 360 / self.count

    def shoot(self, shooter_pos, target_pos, bullet_img):

        for i in range(self.count):
            angle = i * self.angle_fraction
            deploy_pos = shooter_pos + Vector2(self.radius, 0).rotate(angle)

            ang_vel = 150 if i & 1 else -150

            b = DeployableBullet(
                shooter_pos,
                deploy_pos,
                deploy_duration=0.5,
                wait_duration=0.5,
                arrived_action="aim",
                speed_final=self.bullet_speed,
                target_pos=shooter_pos,
                angular_vel=ang_vel,
                angular_drag=0.99,
            )

            self.bullet_group.add(b)
