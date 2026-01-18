import itertools
import pygame, sys
from pygame.locals import *
from pygame.math import Vector2
from hello_pygame.enemy import Enemy
from hello_pygame.entities import Handle_Collisions
from hello_pygame.gfx import Background, stream_group
from hello_pygame.danmaku import Bullet, CirclePattern, ConvergePattern
from hello_pygame.level_data import LEVEL_1
from hello_pygame.player import Player
from hello_pygame.settings import *


def main():

    pygame.init()

    pyClock = pygame.time.Clock()

    DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    display_buffer = []
    pygame.display.set_caption("Very cool game")

    load_res()

    print("Enjoy UwU")

    Player_Bullets = pygame.sprite.Group()
    P1 = Player(Player_Bullets)
    Player_Position: Vector2 = P1.pos

    Enemy_Bullets = pygame.sprite.Group()
    Enemy_Group = pygame.sprite.Group()

    BG = Background()

    bg_buffer = BG.draw_sky()

    STAGE_TIMER = 0.0
    CO = 0

    while True:
        dt = pyClock.tick(FPS) / 1000.0

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

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                # elif event.key == pygame.K_c:
                #   P1.damage()

        P1.update(dt)
        Player_Position = P1.pos

        for enemy in Enemy_Group:
            enemy.update(dt, Player_Position)
        Player_Bullets.update(dt)
        Enemy_Bullets.update(dt)

        Handle_Collisions(P1, Enemy_Group, Player_Bullets, Enemy_Bullets)

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

        pygame.display.update()

        STAGE_TIMER += dt


if __name__ == "__main__":
    main()
