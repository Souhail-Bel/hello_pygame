import itertools
import pygame, sys
from pygame.locals import *
from pygame.math import Vector2
from pygame.typing import ColorLike
from hello_pygame.enemy import Enemy
from hello_pygame.entities import Handle_Collisions
from hello_pygame.gfx import Background, stream_group
from hello_pygame.danmaku import Bullet, CirclePattern, ConvergePattern
from hello_pygame.level_data import LEVEL_1
from hello_pygame.player import Player
from hello_pygame.settings import *


# imma state till i machine


def new_game_state():
    """
    player, player bullets
    enemy group, enemy bullets,
    stage_timer, co,
    game_state
    """
    P_bullets = pygame.sprite.Group()
    P = Player(P_bullets)

    E_bullets = pygame.sprite.Group()
    E_group = pygame.sprite.Group()

    return P, P_bullets, E_group, E_bullets, 0.0, 0, "RUNNING"


def load_ui(font: pygame.font.Font):
    def render_center(text, color: ColorLike):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        return surf, rect

    return {
        "PAUSE": render_center("GAME PAUSED", (120, 200, 0)),
        "OVER": render_center("Ouchie :P ~ Press R", (220, 80, 80)),
        "WIN": render_center("Congrats ~ Press R", (180, 210, 50)),
    }


def main():

    pygame.init()
    pygame.font.init()

    UI_FONT = pygame.font.SysFont("Monospace", 64, bold=True, italic=True)
    UIs = load_ui(UI_FONT)

    pyClock = pygame.time.Clock()

    DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Very cool game")

    load_res()

    print("Enjoy UwU")

    BG = Background()

    P1, Player_Bullets, Enemy_Group, Enemy_Bullets, STAGE_TIMER, CO, GAME_STATE = (
        new_game_state()
    )

    Player_Position: Vector2 = P1.pos

    bg_buffer = BG.draw_sky()

    while True:
        dt = pyClock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    if GAME_STATE == "RUNNING":
                        GAME_STATE = "PAUSE"
                    elif GAME_STATE == "PAUSE":
                        GAME_STATE = "RUNNING"

                elif event.key == pygame.K_r:
                    if GAME_STATE in ("OVER", "WIN"):
                        (
                            P1,
                            Player_Bullets,
                            Enemy_Group,
                            Enemy_Bullets,
                            STAGE_TIMER,
                            CO,
                            GAME_STATE,
                        ) = new_game_state()
        if GAME_STATE == "RUNNING":
            while CO < len(LEVEL_1):
                eve = LEVEL_1[CO]

                if STAGE_TIMER >= eve["time"]:
                    enemy = Enemy(
                        ene_type=eve["type"],
                        init_pos=eve["pos"],
                        script=eve["script"],
                        bullet_group=Enemy_Bullets,
                    )

                    Enemy_Group.add(enemy)

                    CO += 1

                else:
                    break

            P1.update(dt)
            Player_Position = P1.pos

            for enemy in Enemy_Group:
                enemy.update(dt, Player_Position)
            Player_Bullets.update(dt)
            Enemy_Bullets.update(dt)

            Handle_Collisions(P1, Enemy_Group, Player_Bullets, Enemy_Bullets)

            STAGE_TIMER += dt

            if not P1.is_alive:
                GAME_STATE = "OVER"

            elif CO == len(LEVEL_1) and len(Enemy_Group) == 0:
                GAME_STATE = "WIN"

        display_buffer = itertools.chain(
            BG.draw_landscape(),
            BG.draw_tower(),
            stream_group(Player_Bullets),
            P1.draw(),
            stream_group(Enemy_Bullets),
            stream_group(Enemy_Group),
        )

        DISPLAY_SURFACE.fblits(bg_buffer)
        DISPLAY_SURFACE.fblits(display_buffer)

        if GAME_STATE in UIs:
            surf, rect = UIs[GAME_STATE]
            DISPLAY_SURFACE.blit(surf, rect)

        pygame.display.update()


if __name__ == "__main__":
    main()


# honestly, i learned what python truly is through this project
# and i regret NOTHING
