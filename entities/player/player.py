from random import randint

import pygame
from pygame.math import Vector2

from entities.experience_coin.experience_coin import ExperienceCoin
from utils import scaler
from utils.animation import Animation
from entities.base.base_entity import BaseEntity


class Player(BaseEntity):
    def __init__(self):
        self._type = "player"

        super().__init__()

    def _setup_animations(self):
        idle_sheet = pygame.image.load("data/sprites/player_idle.png").convert_alpha()
        walk_sheet = pygame.image.load("data/sprites/player_walk.png").convert_alpha()

        self.animations = {
            "idle": Animation(idle_sheet, 100, 100, scale=2, duration=100, loop=True),
            "walk": Animation(walk_sheet, 100, 100, scale=2, duration=75, loop=True)
        }

        self.current_state = "idle"
        self.image = self.animations[self.current_state].get_current_frame()
        self.rect = self.image.get_rect()
        self.flip = False

    def _setup_stats(self):
        super()._setup_stats()
        self.hp = 5
        self.invincibility_duration = 1000

        self.level = 1
        self.xp = 0
        self.max_xp = 5

        self.score = 0

    def _setup_physics(self):
        super()._setup_physics()
        self.pos = Vector2(self.rect.x, self.rect.y)
        self.speed = 0.8

        self.input_acceleration = Vector2(0, 0)

    def set_state(self, new_state):
        if self.current_state != new_state:
            self.current_state = new_state
            self.animations[self.current_state].reset()

    def animate(self):
        if self.velocity.x > 0:
            self.set_state("walk")
            self.flip = False
        elif self.velocity.x < 0:
            self.set_state("walk")
            self.flip = True
        elif self.velocity.y != 0:
            self.set_state("walk")
        else:
            self.set_state("idle")
        current_animation = self.animations[self.current_state]
        current_animation.update()
        raw_image = current_animation.get_current_frame()
        self.image = pygame.transform.flip(raw_image, self.flip, False)


    def collect_coins(self):
        coins = list(ExperienceCoin.group)

        for coin in coins:
            if self.hitbox.colliderect(coin.hitbox):
                self.xp += coin.xp_value
                self.score += 10
                coin.kill()
                self.check_level_up()

    def check_level_up(self):
        if self.xp >= self.max_xp:
            self.xp -= self.max_xp
            self.level += 1
            self.score += 100

            self.max_xp = int(self.max_xp * 1.5)
            if hasattr(self, 'scene') and hasattr(self.scene, 'upgrade_menu'):
                self.scene.upgrade_menu.show()


    def update(self):
        self.velocity += self.input_acceleration
        super().move()
        self.animate()

        self.collect_coins()

        if self.hp <= 0:
            self.kill()