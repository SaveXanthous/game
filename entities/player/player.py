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

    def _setup_physics(self):
        super()._setup_physics()
        self.pos = Vector2(self.rect.x, self.rect.y)
        self.speed = 0.8

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


    def player_input(self):
        keys = pygame.key.get_pressed()
        acceleration = Vector2(0, 0)
        if keys[pygame.K_LEFT]: acceleration.x = -1
        if keys[pygame.K_RIGHT]: acceleration.x = 1
        if keys[pygame.K_UP]: acceleration.y = -1
        if keys[pygame.K_DOWN]: acceleration.y = 1

        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            acceleration.x = 0

        if keys[pygame.K_UP] and keys[pygame.K_DOWN]:
            acceleration.y = 0

        if acceleration.length() != 0:
            acceleration.normalize()

        self.velocity += acceleration

    def pick_coin(self):
        coins_group = ExperienceCoin.get_group()

        for coin in coins_group:
            if self.hitbox.colliderect(coin.hitbox):
                # self.gain_xp(coin.xp_value)
                coin.kill()

    def update(self):
        self.player_input()
        super().move()
        self.animate()

        self.pick_coin()

        if self.hp <= 0:
            self.kill()