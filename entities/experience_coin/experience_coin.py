import pygame
from pygame import Vector2

from entities.base.base_entity import BaseEntity
from utils.animation import Animation


class ExperienceCoin(BaseEntity):
    def __init__(self, pos, player):
        self._type = "coin"
        self.player = player
        self._initial_pos = pos

        super().__init__()

    def _setup_animations(self):
        coin_sheet = pygame.image.load('data/sprites/coin.png')

        self.animations = {
            "coin": Animation(coin_sheet, 16, 16, scale=1.4, duration=100, loop=True)
        }

        self.current_state = "coin"
        self.image = self.animations[self.current_state].get_current_frame()
        self.flip = False

        self.rect = self.image.get_rect(center=(self._initial_pos.x, self._initial_pos.y))

    def _setup_physics(self):
        super()._setup_physics()
        self.pos = Vector2(self.rect.centerx, self.rect.centery)

    def _setup_stats(self):
        super()._setup_stats()
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