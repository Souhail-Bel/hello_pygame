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
        init_HP = 40

        if ene_type == "red":
            img = "enemy_r"
            init_HP = 60
        elif ene_type == "green":
            img = "enemy_g"
            init_HP = 100
        elif ene_type == "boss":
            img = "mokou"
            init_HP = 600

        LivingSprite.__init__(self, init_HP=init_HP)
        AnimatedSprite.__init__(self, sequence=IMG_DICT[img], animation_speed=12)

        self.__DEATH_MARGIN = 20

        self.pos = Vector2(init_pos)
        self.rect.center = round(self.pos)

        self.bullet_group = bullet_group
        # TODO change per type
        self.bullet_img = IMG_DICT["bullet_ene"]

        # None stands for not firing, calma UwU
        self.bullet_hell = None

        # script shenanigans
        self.instructs = self.parse_script(script)
        self.__SCRIPT_LENGTH = len(self.instructs)
        self.instruct_pointer = 0
        self.busy = False
        self.timer = 0.0

        self.move_pos = None
        self.move_start_pos = Vector2(self.pos)
        self.move_duration = 0.0
        self.move_timer = 0.0

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
                move_speed = float(args[2])

                self.move_start_pos = Vector2(self.pos)
                distance = self.pos.distance_to(self.move_pos)
                self.move_duration = distance / move_speed if move_speed > 0 else 0

                self.move_timer = 0.0
                self.busy = True

            elif cmd == "wait":
                self.timer = float(args[0])
                self.busy = True

            elif cmd == "pattern":
                pattern_name = args[0]
                pattern_args = args[1:]

                new_pattern = PATTERN_REG.get(pattern_name, None)
                if new_pattern:
                    self.bullet_hell = new_pattern(self.bullet_group, pattern_args)
                else:
                    self.bullet_hell = None

                self.instruct_pointer += 1

            elif cmd == "die":
                self.kill()  # X_X

        if self.busy:

            # Note that python is kinda mid
            # so don't expect yourself to compare floating-based vectors and get accurate results
            # so, have a "margin for reaching a target" thing
            if self.move_pos:
                self.move_timer += dt

                if self.move_duration > 0:
                    t = self.move_timer / self.move_duration
                else:
                    t = 1.0

                if t >= 1.0:
                    self.pos = self.move_pos
                    self.move_pos = None
                    self.busy = False
                    self.instruct_pointer += 1
                else:
                    interp_t = t * t * (3 - 2 * t)
                    self.pos = self.move_start_pos.lerp(self.move_pos, interp_t)

            # if we're not busy moving, we're busy waitin :P
            elif self.timer > 0:
                self.timer -= dt
                if self.timer <= 0:
                    self.busy = False
                    self.instruct_pointer += 1

        self.rect.center = round(self.pos)
        self.animate(dt)

        if self.bullet_hell and self.bullet_hell.canShoot(dt):
            self.bullet_hell.shoot(self.pos, player_pos, self.bullet_img)

    def draw(self) -> Generator[tuple, None, None]:
        yield (self.image, self.rect)

    def on_death(self):
        self.kill()
