import pygame
from pygame.math import Vector2

from entities.animation_component.animation import Animation
from entities.base.base_entity import BaseEntity


class Player(BaseEntity):
    def __init__(self):
        super().__init__()

        idle_sheet = pygame.image.load("data/sprites/player_idle.png").convert_alpha()
        walk_sheet = pygame.image.load("data/sprites/player_walk.png").convert_alpha()


        self.animations = {
            "idle": Animation(idle_sheet, 100, 100, scale=2, duration=75, loop=True),
            "walk": Animation(walk_sheet, 100, 100, scale=2, duration=50, loop=True)
        }

        self.current_state = "idle"
        self.image = self.animations[self.current_state].get_current_frame()
        self.rect = self.image.get_rect(midbottom = (640, 360))
        self.flip = False
        self._type = "player"

        self.pos = Vector2(self.rect.x, self.rect.y)
        self.speed = 2

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

        if acceleration.length() > 0:
            acceleration.normalize()

        self.velocity += acceleration

    def move(self):
        self.velocity *= (1 - self.friction)

        if self.velocity.length() < 0.1: self.velocity = Vector2(0, 0)

        self.pos += self.velocity * self.speed # нужно потом добавить time_delta

        self.rect = self.pos

    def update(self):
        self.player_input()
        self.move()
        self.animate()