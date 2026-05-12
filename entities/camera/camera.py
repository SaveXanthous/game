import pygame

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        self.offset = pygame.math.Vector2()
        self.smoothing = 0.05
        self.target = None

    def set_target_camera(self, target):
        self.target = target
        if target:
            self.offset.x = self.target.rect.centerx - self.half_width
            self.offset.y = self.target.rect.centery - self.half_height

    def center_target_camera(self):
        if self.target:
            target_x = self.target.rect.centerx - self.half_width
            target_y = self.target.rect.centery - self.half_height

            self.offset.x += (target_x - self.offset.x) * self.smoothing
            self.offset.y += (target_y - self.offset.y) * self.smoothing

    def draw(self, sprite):
        self.center_target_camera()

        for sprite in sprite:
            offset_pos = (
                int(sprite.rect.left - self.offset.x),
                int(sprite.rect.top - self.offset.y)
            )
            self.display_surface.blit(sprite.image, offset_pos)