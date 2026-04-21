import pygame

from entities.player.player import Player


class Enemy(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load("data/sprites/enemy.png")
        self.rect = self.image.get_rect(midbottom = (400, 200))
        self.type = "enemy"
        self.player = player

    def move_to_player(self):
        if self.rect.centery < self.player.rect.centery:
            self.rect.y += 5
        if self.rect.centery > self.player.rect.centery:
            self.rect.y -= 5
        if self.rect.centerx < self.player.rect.centerx:
            self.rect.x += 5
        if self.rect.centerx > self.player.rect.centerx:
            self.rect.x -= 5

    def type(self):
        return self.type

    def update(self):
        self.move_to_player()