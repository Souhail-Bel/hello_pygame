from collections.abc import Generator
import pygame
from pygame.math import Vector2
from hello_pygame.entities import AnimatedSprite, LivingSprite
from hello_pygame.danmaku import *
from hello_pygame.settings import IMG_DICT, SCREEN_HEIGHT, SCREEN_WIDTH


class Enemy(LivingSprite, AnimatedSprite):
    def __init__(
        self,
        ene_type: str,
        init_pos: tuple,
        script: list,
        bullet_group: pygame.sprite.Group,
    ):

        img = "enemy_b"
        init_HP = 20

        if ene_type == "red":
            img = "enemy_r"
            init_HP = 30
        elif ene_type == "green":
            img = "enemy_g"
            init_HP = 50
        elif "boss":
            img = "mokou"
            init_HP = 120

        LivingSprite.__init__(self, init_HP=init_HP)
        AnimatedSprite.__init__(self, sequence=IMG_DICT[img], animation_speed=12)

        self.__DEATH_MARGIN = 20

        self.pos = Vector2(init_pos)
        self.rect.center = round(self.pos)

        self.bullet_group = bullet_group
        # TODO change per type
        self.bullet_img = IMG_DICT["bullet_ene"]
        self.bullet_hell = None

        # script shenanigans
        self.instructs = self.parse_script(script)
        self.__SCRIPT_LENGTH = len(self.instructs)
        self.instruct_pointer = 0
        self.busy = False
        self.timer = 0.0
        self.move_pos = None
        self.move_speed = 0

    def parse_script(self, script) -> list:
        ret = []
        for instruct in script:
            tok = instruct.split()
            cmd = tok[0]
            args = tok[1:]
            ret.append((cmd, args))
        return ret

    def update(self, dt: float, player_pos: Vector2):
        # self.pos += self.vel * dt
        #
        # if (
        #     self.pos.y > SCREEN_HEIGHT + self.__DEATH_MARGIN
        #     or self.pos.x < self.__DEATH_MARGIN
        #     or self.pos.x > SCREEN_WIDTH + self.__DEATH_MARGIN
        # ):
        #     self.kill()

        if not self.busy and self.instruct_pointer < self.__SCRIPT_LENGTH:
            cmd, args = self.instructs[self.instruct_pointer]

            if cmd == "move":
                self.move_pos = Vector2(float(args[0]), float(args[1]))
                self.move_speed = float(args[2])
                self.busy = True

        if self.busy:
            if self.move_pos:
                move_dir = self.move_pos - self.pos
                self.pos += move_dir * self.move_speed * dt

        self.rect.center = round(self.pos)
        self.animate(dt)

        if self.bullet_hell and self.bullet_hell.canShoot(dt):
            self.bullet_hell.shoot(self.pos, player_pos, self.bullet_img)

    def draw(self) -> Generator[tuple, None, None]:
        yield (self.image, self.rect)

    def on_death(self):
        self.kill()
