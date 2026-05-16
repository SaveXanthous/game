import pygame
from pygame import Vector2

from entities.base.base_entity import BaseEntity
from utils.animation import Animation


class ExperienceCoin(BaseEntity):
    def __init__(self, pos, player):
        super().__init__()

        self.player = player

        coin_sheet = pygame.image.load('data/sprites/coin.png')

        self.animations = {
            "coin" : Animation(coin_sheet, 16, 16, scale=1.4, duration=100, loop=True)
        }

        self.flip = False

        self._type = "coin"

        self.current_state = "coin"
        self.image = self.animations[self.current_state].get_current_frame()

        self.pos = pos
        self.rect.center = self.pos

        self.hitbox = self.rect

        self.xp_value = 1

    def animate(self):
        current_animation = self.animations[self.current_state]
        current_animation.update()
        raw_image = current_animation.get_current_frame()
        self.image = pygame.transform.flip(raw_image, self.flip, False)

    def set_state(self, new_state):
        pass

    def update(self):
        self.animate()