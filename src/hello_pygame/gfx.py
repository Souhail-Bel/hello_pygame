import pygame
from hello_pygame.settings import RES_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class Background:
    def __init__(self):
        self.BG_ECLIPSE = pygame.image.load(RES_DIR / "eclipse.png")
        self.BG_LANDSCAPE = pygame.image.load(RES_DIR / "bg.png")
        self.BG_SKY = pygame.image.load(RES_DIR / "sky.png")
        self.BG_TOWER = pygame.image.load(RES_DIR / "tower.png")
        self.tower_height = self.BG_TOWER.get_height()

        self.landscape_offset = 0
        self.landscape_speed = 0.02

        self.tower_offset = self.tower_height
        self.tower_speed = 0.2

    def draw_sky(self) -> list:
        return [(self.BG_SKY, (0, 0)), (self.BG_ECLIPSE, (SCREEN_WIDTH - 200, 50))]

    def draw_landscape(self) -> tuple:
        self.landscape_offset += self.landscape_speed
        return (self.BG_LANDSCAPE, (0, self.landscape_offset))

    def draw_tower(self) -> list:
        self.tower_offset += self.tower_speed

        if self.tower_offset >= self.tower_height * 2:
            self.tower_offset = self.tower_height

        titanic_tower = []
        for y in range(3):
            titanic_tower.append(
                (self.BG_TOWER, (0, -y * self.tower_height + self.tower_offset))
            )
        return titanic_tower
