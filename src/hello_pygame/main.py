import itertools
import pygame, sys
from pygame.locals import *
from pygame.math import Vector2
from hello_pygame.enemy import Enemy
from hello_pygame.gfx import Background, stream_group
from hello_pygame.danmaku import Bullet
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
    E = Enemy(Enemy_Bullets)

    BG = Background()

    bg_buffer = BG.draw_sky()

    while True:
        # since there'll be bullet logic and moving parts...
        # I don't want my game to run differently on 144Hz or sth
        dt = pyClock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    P1.damage()

        P1.update(dt)
        Player_Position = P1.pos

        E.update(dt, Player_Position)
        P1.bullet_group.update(dt)
        E.bullet_group.update(dt)

        display_buffer = itertools.chain(
            BG.draw_landscape(),
            BG.draw_tower(),
            stream_group(Player_Bullets),
            P1.draw(),
            stream_group(Enemy_Bullets),
            E.draw(),
        )

        DISPLAY_SURFACE.fblits(bg_buffer)
        DISPLAY_SURFACE.fblits(display_buffer)

        pygame.display.update()


if __name__ == "__main__":
    main()
