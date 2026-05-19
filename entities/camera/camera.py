import pygame
import random
import math
from entities.base.base_entity import BaseEntity
from utils.scaler import Scaler


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        self.offset = pygame.math.Vector2()

        self.normal_smoothing = 0.2
        self.spawn_smoothing = 0.03
        self.current_smoothing = self.normal_smoothing

        self.target = None
        self.is_appearing = False

    def set_target_camera(self, target):
        self.target = target
        if target and not self.is_appearing:
            self.offset.x = self.target.rect.centerx - self.half_width
            self.offset.y = self.target.rect.centery - self.half_height

    def spawn_cinematic(self, target, min_radius=400, max_radius=700):
        min_radius = Scaler.scaled_radius(min_radius)
        max_radius = Scaler.scaled_radius(max_radius)

        self.target = target
        if not target:
            return

        ideal_x = self.target.rect.centerx - self.half_width
        ideal_y = self.target.rect.centery - self.half_height

        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(min_radius, max_radius)

        self.offset.x = ideal_x + radius * math.cos(angle)
        self.offset.y = ideal_y + radius * math.sin(angle)

        self.is_appearing = True
        self.current_smoothing = self.spawn_smoothing

    def center_target_camera(self):
        if not self.target:
            return

        target_x = self.target.rect.centerx - self.half_width
        target_y = self.target.rect.centery - self.half_height

        self.offset.x += (target_x - self.offset.x) * self.current_smoothing
        self.offset.y += (target_y - self.offset.y) * self.current_smoothing

        if self.is_appearing:
            distance_sq = (target_x - self.offset.x) ** 2 + (target_y - self.offset.y) ** 2

            if distance_sq < 4:
                self.is_appearing = False
                self.current_smoothing = self.normal_smoothing

    def draw(self):
        self.center_target_camera()

        for sprite in BaseEntity.container:
            offset_pos = (
                int(sprite.rect.left - self.offset.x),
                int(sprite.rect.top - self.offset.y)
            )
            self.display_surface.blit(sprite.image, offset_pos)

    @property
    def is_cinematic_finished(self) -> bool:
        return not self.is_appearing

    @property
    def position(self):
        return (self.offset.x, self.offset.y)

    @property
    def view_rect(self):
        size = self.display_surface.get_size()
        return pygame.Rect(self.offset.x, self.offset.y, size[0], size[1])