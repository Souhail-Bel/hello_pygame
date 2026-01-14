from pathlib import Path
import pygame

# hideous and is NOT to be kept on release, but eh
ROOT_DIR = Path(__file__).parent.parent.parent
RES_DIR = ROOT_DIR / "res"

IMG_SRC = {
    "reimu": [RES_DIR / "reimu_1.png", RES_DIR / "reimu_2.png"],
    "eclipse": RES_DIR / "eclipse.png",
    "bg": RES_DIR / "bg.png",
    "sky": RES_DIR / "sky.png",
    "tower": RES_DIR / "tower.png",
    "bullet": RES_DIR / "bullet.png",
}

IMG_DICT = {}


def load_res():
    global IMG_DICT
    for k, v in IMG_SRC.items():
        if isinstance(v, list):
            IMG_DICT[k] = []
            for a in v:
                IMG_DICT[k].append(pygame.image.load(a).convert_alpha())
        else:
            IMG_DICT[k] = pygame.image.load(v).convert_alpha()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0xC0, 0xC0, 0xC0)
FPS = 60
