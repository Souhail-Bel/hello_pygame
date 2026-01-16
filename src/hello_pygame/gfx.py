from typing import Generator
import pygame
from hello_pygame.settings import IMG_DICT, SCREEN_HEIGHT, SCREEN_WIDTH


def stream_group(group: pygame.sprite.Group):
    for sprite in group:
        yield from sprite.draw()


class Background:
    def __init__(self):
        self.BG_ECLIPSE = IMG_DICT["eclipse"]
        self.BG_LANDSCAPE = IMG_DICT["bg"]
        self.BG_SKY = IMG_DICT["sky"]
        self.BG_TOWER = IMG_DICT["tower"]
        self.tower_height = self.BG_TOWER.get_height()

        self.landscape_offset = 0
        self.landscape_speed = 0.02

        self.tower_offset = self.tower_height
        self.tower_speed = 0.2

    def draw_sky(self) -> list:
        return [(self.BG_SKY, (0, 0)), (self.BG_ECLIPSE, (SCREEN_WIDTH - 200, 50))]

    def draw_landscape(self) -> Generator[tuple, None, None]:
        if self.landscape_offset >= SCREEN_HEIGHT:
            return
        self.landscape_offset += self.landscape_speed
        yield (self.BG_LANDSCAPE, (0, self.landscape_offset))

    def draw_tower(self) -> Generator[tuple, None, None]:
        self.tower_offset += self.tower_speed

        if self.tower_offset >= self.tower_height * 2:
            self.tower_offset = self.tower_height

        for y in range(3):
            yield (self.BG_TOWER, (0, -y * self.tower_height + self.tower_offset))
