import random
from random import randint

import pygame

from entities.player.player import Player
from pygame.math import Vector2

class Enemy(pygame.sprite.Sprite):

    def __init__(self, player: Player):
        super().__init__()
        self.image = pygame.image.load("data/sprites/enemy.png")
        self.rect = self.image.get_rect(midbottom = (randint(0, 1280), randint(0, 720)))
        self.type = "enemy"
        self.player = player

        self.pos = Vector2(self.rect.x, self.rect.y)
        self.velocity = Vector2(0, 0)
        self.speed = 0.5
        self.friction = 0.15

    def player_direction(self):
        acceleration = Vector2(0, 0)
        if self.rect.y < self.player.rect.y: acceleration.y = 1
        if self.rect.y > self.player.rect.y: acceleration.y = -1
        if self.rect.x < self.player.rect.x: acceleration.x = 1
        if self.rect.x > self.player.rect.x: acceleration.x = -1

        if self.rect.x == self.player.rect.x and self.rect.y == self.player.rect.y:
            acceleration = Vector2(0, 0)

        if acceleration.length() > 0:
            acceleration.normalize()

        self.velocity += acceleration

    def move(self):
        self.velocity *= (1 - self.friction)

        if self.velocity.length() < 0.1: self.velocity = Vector2(0, 0)

        self.pos += self.velocity * self.speed  # нужно потом добавить time_delta

        self.rect = self.pos

    def type(self):
        return self.type

    def update(self):
        self.player_direction()
        self.move()