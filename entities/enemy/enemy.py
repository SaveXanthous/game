import pygame

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("entities/enemy/enemy.png")
        self.rect = self.image.get_rect(midbottom = (400, 200))

    def update(self):
        pass