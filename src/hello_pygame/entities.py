import pygame


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
