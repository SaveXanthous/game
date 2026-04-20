import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("entities/player/player.PNG").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (640, 360))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
        if keys[pygame.K_UP]:
            self.rect.y -= 10
        if keys[pygame.K_DOWN]:
            self.rect.y += 10

    def update(self):
        self.player_input()
