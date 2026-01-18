from collections.abc import Generator
import pygame
from pygame.locals import *
from pygame.math import Vector2
from hello_pygame.entities import AnimatedSprite, LivingSprite
from hello_pygame.danmaku import Bullet
from hello_pygame.settings import IMG_DICT, SCREEN_HEIGHT, SCREEN_WIDTH, SFX


class UI:
    def __init__(self, start_HP, max_HP=None):
        self.current_HP: float = start_HP
        if max_HP is None:
            max_HP = self.current_HP
        self.max_HP: float = max_HP

        self.HP_Width = 128
        self.HP_Height = 32
        self.HP_padding = 5
        self.HP_opacity = 0.8
        self.HP_alpha = 255 * self.HP_opacity

        self.HP_Color_Normal = (50, 222, 50, self.HP_alpha)
        self.HP_Color_Critical = (222, 50, 50, self.HP_alpha)

        self.HP_Surface = pygame.Surface((self.HP_Width, self.HP_Height), SRCALPHA)
        self.HP_Rect = self.HP_Surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))

    def update(self, new_HP):
        self.current_HP = new_HP

        HP_color = (
            self.HP_Color_Normal
            if self.current_HP > self.max_HP / 2
            else self.HP_Color_Critical
        )
        HP_relative_width = int((self.current_HP / self.max_HP) * self.HP_Width)

        self.HP_Surface.fill((0, 0, 0, 0))

        pygame.draw.rect(
            self.HP_Surface,
            (0, 0, 0, self.HP_alpha),
            Rect((0, 0), (self.HP_Width, self.HP_Height)),
            border_radius=5,
        )

        pygame.draw.rect(
            self.HP_Surface,
            HP_color,
            Rect(
                (self.HP_Width - self.HP_padding, self.HP_padding),
                (
                    -HP_relative_width + self.HP_padding * 2,
                    self.HP_Height - self.HP_padding * 2,
                ),
            ),
            border_radius=5,
        )

    def draw(self):
        yield (self.HP_Surface, self.HP_Rect)


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
        LivingSprite.__init__(self, init_HP=10)

        AnimatedSprite.__init__(self, sequence=IMG_DICT["reimu"], animation_speed=5)

        # MOVEMENT
        self.SPEED = 400  # pixels/sec
        self.pos = Vector2(SCREEN_WIDTH / 2, 500)
        self.rect.center = round(self.pos)
        self._SPEED_NORMAL = self.SPEED
        self._SPEED_FOCUSED = self.SPEED / 2
        self.is_focused = False

        # BULLETS
        bullet_rate = 25  # bullets / sec
        self._inv_bullet_rate = 1.0 / bullet_rate
        self.bullet_timer = 0.0
        self.bullet_group = bullet_group

        # ORBS
        self.orbs = [
            Orb(side=1, bullet_group=self.bullet_group),
            Orb(side=-1, bullet_group=self.bullet_group),
        ]

        # INVINCIBILITY
        self.invincibility_timer = 0.0
        self._invincibility_duration = 2
        self.is_visible = True

        # HITBOX
        self.hitbox_surface = pygame.Surface((8, 8), SRCALPHA)
        pygame.draw.circle(self.hitbox_surface, "red", (4, 4), 4)
        pygame.draw.circle(self.hitbox_surface, "white", (4, 4), 3)

        # UI
        self.ui = UI(self.HP)
        self.ui.update(self.HP)

    def shoot(self):
        for orb in self.orbs:
            orb.shoot()

    def handle_input(self, dt):

        pressed_keys = pygame.key.get_pressed()

        self.is_focused = pressed_keys[K_RSHIFT] or pressed_keys[K_LSHIFT]
        self.SPEED = self._SPEED_FOCUSED if self.is_focused else self._SPEED_NORMAL

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

        if pressed_keys[K_x] and self.bullet_timer <= 0:
            self.bullet_timer = self._inv_bullet_rate
            self.shoot()

    def update(self, dt: float):

        if not self.is_alive:
            return

        self.bullet_timer -= dt

        self.animate(dt)

        for orb in self.orbs:
            orb.update(dt, self.pos, self.is_focused)

        self.handle_input(dt)

        self.is_visible = True
        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt

            if (self.invincibility_timer % 0.02) > 0.01:
                self.is_visible = False

    def draw(self) -> Generator[tuple, None, None]:
        if not self.is_alive:
            return

        if self.is_visible:
            yield (self.image, self.rect)

        for orb in self.orbs:
            yield from orb.draw()

        if self.is_focused:
            yield (
                self.hitbox_surface,
                self.hitbox_surface.get_rect(center=self.rect.center),
            )

        yield from self.ui.draw()

    def damage(self, amount=1):
        if self.invincibility_timer > 0:
            return

        self.HP -= 1

        self.invincibility_timer = self._invincibility_duration

        self.on_damage()

    def on_damage(self):
        SFX["player_hit"].play()
        self.ui.update(self.HP)
        # print("Ouchie")

    def on_death(self):
        # print("I has death")
        self.pos = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2)
        self.rect.center = round(self.pos)
