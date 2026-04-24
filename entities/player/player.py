import pygame
from pygame.math import Vector2

from entities.base.base_entity import BaseEntity


class Player(BaseEntity):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("data/sprites/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (640, 360))
        self.type = "player"

        self.pos = Vector2(self.rect.x, self.rect.y)
        self.velocity = Vector2(0, 0)
        self.speed = 1
        self.friction = 0.1

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

        if acceleration.length() > 0:
            acceleration.normalize()

        self.velocity += acceleration

    def move(self):
        self.velocity *= (1 - self.friction)

        if self.velocity.length() < 0.1: self.velocity = Vector2(0, 0)

        self.pos += self.velocity * self.speed # нужно потом добавить time_delta

        self.rect = self.pos

    def type(self):
        return self.type

    def update(self):
        self.player_input()
        self.move()
