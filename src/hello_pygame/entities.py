import pygame


class LivingSprite(pygame.sprite.Sprite):
    def __init__(self, init_HP: int, MAX_HP=0):
        super().__init__()
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
