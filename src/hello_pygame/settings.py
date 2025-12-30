from pathlib import Path

# hideous and is NOT to be kept on release, but eh
ROOT_DIR = Path(__file__).parent.parent.parent
RES_DIR = ROOT_DIR / "res"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0xC0, 0xC0, 0xC0)
FPS = 60
