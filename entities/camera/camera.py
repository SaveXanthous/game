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

    def spawn_cinematic(self, target=None, min_radius=400, max_radius=700, mode="ease_out"):
        """
        Кинематографичный вылет.
        mode="ease_out" -> Резкий старт со скоростью, плавное замедление к концу.
        mode="ease_in"  -> Плавный ленивый старт, резкое ускорение (рывок) к концу.
        """
        min_radius = Scaler.scaled_radius(min_radius)
        max_radius = Scaler.scaled_radius(max_radius)

        self.target = target
        self.cinematic_mode = mode

        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(min_radius, max_radius)
        offset_x = radius * math.cos(angle)
        offset_y = radius * math.sin(angle)

        if target:
            ideal_x = self.target.rect.centerx - self.half_width
            ideal_y = self.target.rect.centery - self.half_height
            self.offset.x = ideal_x + offset_x
            self.offset.y = ideal_y + offset_y
        else:
            self.cinematic_destination = pygame.math.Vector2(
                self.offset.x + offset_x,
                self.offset.y + offset_y
            )

        self.is_appearing = True

        if self.cinematic_mode == "ease_in":
            self.current_smoothing = 0.005
        else:
            self.current_smoothing = 0.06

    def center_target_camera(self):
        if self.target:
            target_x = self.target.rect.centerx - self.half_width
            target_y = self.target.rect.centery - self.half_height
        elif self.is_appearing and hasattr(self, 'cinematic_destination'):
            target_x = self.cinematic_destination.x
            target_y = self.cinematic_destination.y
        else:
            return

        if self.is_appearing:
            if self.cinematic_mode == "ease_in":
                self.current_smoothing = min(0.4, self.current_smoothing * 1.09)
            elif self.cinematic_mode == "ease_out":
                self.current_smoothing = max(0.015, self.current_smoothing * 0.97)

        step_x = (target_x - self.offset.x) * self.current_smoothing
        step_y = (target_y - self.offset.y) * self.current_smoothing

        if self.is_appearing:
            step_length_sq = step_x ** 2 + step_y ** 2

            if step_length_sq < 4:
                dx = target_x - self.offset.x
                dy = target_y - self.offset.y
                dist = math.hypot(dx, dy)
                if dist > 0:
                    step_x = (dx / dist) * 2
                    step_y = (dy / dist) * 2

        self.offset.x += step_x
        self.offset.y += step_y

        if self.is_appearing:
            distance_sq = (target_x - self.offset.x) ** 2 + (target_y - self.offset.y) ** 2

            stop_threshold = 100 if self.cinematic_mode == "ease_in" else 9

            if distance_sq < stop_threshold:
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