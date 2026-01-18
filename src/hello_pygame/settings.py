from pathlib import Path
import pygame

# hideous and is NOT to be kept on release, but eh
ROOT_DIR = Path(__file__).parent.parent.parent
RES_DIR = ROOT_DIR / "res"

IMG_SRC = {
    "reimu": [f"reimu_{i}.png" for i in [1, 2]],
    "eclipse": "eclipse.png",
    "bg": "bg.png",
    "sky": "sky.png",
    "tower": "tower.png",
    "bullet": "bullet.png",
    "orb": [f"orb{i}.png" for i in range(1, 5)],
    "enemy_r": [f"enemy_r{i}.png" for i in [1, 2]],
    "enemy_g": [f"enemy_g{i}.png" for i in [1, 2]],
    "enemy_b": [f"enemy_b{i}.png" for i in [1, 2]],
    "mokou": [f"boss{i}.png" for i in range(1, 4)],
    "bullet_pell": "bullet_pell.png",
    "bullet_ene": "bullet_ene.png",
    "aura": [f"boss_aura{i}.png" for i in range(1, 9)],
}

IMG_DICT = {}


def load_res():
    global IMG_DICT
    for k, v in IMG_SRC.items():
        if isinstance(v, list):
            IMG_DICT[k] = []
            for a in v:
                IMG_DICT[k].append(pygame.image.load(RES_DIR / a).convert_alpha())
        else:
            IMG_DICT[k] = pygame.image.load(RES_DIR / v).convert_alpha()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0xC0, 0xC0, 0xC0)
FPS = 60
TAU = 6.283185307
