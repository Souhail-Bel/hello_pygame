import pygame
from pygame import Vector2
from hello_pygame.settings import IMG_DICT


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sequence, animation_speed):
        pygame.sprite.Sprite.__init__(self)

        self.sequence = sequence
        self.sequence_length = len(self.sequence)
        self.FPS = animation_speed

        self.current_frame = 0.0
        self.image = self.sequence[0]
        self.rect: pygame.Rect = self.image.get_rect()

    def animate(self, dt):
        self.current_frame += self.FPS * dt

        if self.current_frame > self.sequence_length:
            self.current_frame = 0

        self.image = self.sequence[int(self.current_frame)]


class LivingSprite:
    def __init__(self, init_HP: int, MAX_HP=0):
        self._MAX_HP = max(MAX_HP, init_HP)
        self._HP = init_HP
        self.is_alive = True

    @property
    def HP(self) -> int:
        return self._HP

    @HP.setter
    def HP(self, value):
        self._HP = value

        if self._HP <= 0:
            self._HP = 0
            self.is_alive = False
            self.on_death()

        elif self._HP > self._MAX_HP:
            self._HP = self._MAX_HP

    def damage(self, amount=1):
        self.HP -= amount
        self.on_damage()

    def heal(self, amount=1):
        self.HP += amount
        self.on_heal()

    def on_damage(self):
        pass

    def on_heal(self):
        pass

    def on_death(self):
        pass


def Handle_Collisions(
    player: LivingSprite,
    enemy_group: pygame.sprite.Group,
    player_bullets: pygame.sprite.Group,
    enemy_bullets: pygame.sprite.Group,
) -> int:
    Score_gain = 0

    # Enemies vs Player's Bullets
    # kills player bullets (dokillb = True)
    # keeps enemies alive for now :)
    Enemies_Hits = pygame.sprite.groupcollide(
        enemy_group, player_bullets, dokilla=False, dokillb=True
    )

    for enemy, bullet_list in Enemies_Hits.items():
        for bullet in bullet_list:
            enemy.damage()
            Score_gain += 1

    Player_Hit = pygame.sprite.spritecollide(
        player,
        enemy_bullets,
        dokill=True,
        collided=pygame.sprite.collide_circle_ratio(0.1),
    ) or pygame.sprite.spritecollide(
        player,
        enemy_group,
        dokill=False,
        collided=pygame.sprite.collide_circle_ratio(0.1),
    )

    if Player_Hit:
        player.damage()

    return Score_gain


class VFX(AnimatedSprite):
    def __init__(self, pos, images, parent=None):
        super().__init__(sequence=images, animation_speed=10)

        self.parent = parent
        self.pos = Vector2(pos)
        self.rect.center = round(self.pos)

    def update(self, dt):
        self.animate(dt)

        if self.parent:
            if not self.parent.is_alive:
                self.kill()

            else:
                self.pos = self.parent.pos
                self.rect.center = round(self.pos)

    def draw(self):
        return (self.image, self.rect)
