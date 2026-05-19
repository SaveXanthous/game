import pygame

from ui.elements.interfaces.easing_movable import EasingMovable
from ui.elements.interfaces.scalable import Scalable
from ui.elements.interfaces.positionable import Positionable
from ui.utils.three_slice_image import ThreeSliceImage
from ui.decorator.register_ui_element import register_ui_element


@register_ui_element
class ProgressBar(Scalable, Positionable, EasingMovable):
    def __init__(self, id, x, y, w, h, base_image_path, fill_image_path,
                 text="", font_size=36, font_color=(255, 255, 255), font_name='monospace',
                 base_color_index=0, fill_color_index=0, progress=1.0, crop_fill=True,
                 offset_x=0, offset_y=0, offset_w=0, offset_h=0):

        self.text = str(text)
        self.font_color = font_color
        self.progress = max(0.0, min(1.0, progress))

        self.crop_fill = crop_fill
        self.fill_image_path = fill_image_path
        self.fill_color_index = fill_color_index

        self.w = self.scaled_width(w)
        self.h = self.scaled_height(h)

        self.offset_x = self.scaled_width(offset_x)
        self.offset_y = self.scaled_height(offset_y)
        self.offset_w = self.scaled_width(offset_w)
        self.offset_h = self.scaled_height(offset_h)

        self.max_fill_w = max(0, self.w - (self.offset_x * 2) - self.offset_w)
        self.fill_h = max(0, self.h - (self.offset_y * 2) - self.offset_h)

        font_size = int(self.scaled_size_front(font_size))
        self.font = pygame.font.SysFont(font_name, font_size)

        self.base_surface = ThreeSliceImage(base_image_path, base_color_index).generate_surface(self.w, self.h)

        if self.crop_fill:
            self.fill_surface_full = ThreeSliceImage(fill_image_path, fill_color_index).generate_surface(
                self.max_fill_w, self.fill_h)
        else:
            self.fill_generator = ThreeSliceImage(fill_image_path, fill_color_index)

        self.x = x
        self.y = y

        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self._x, self._y) if hasattr(self, '_x') else (self.x, self.y)

        self.update_view()

    def set_progress(self, value):
        new_progress = max(0.0, min(1.0, value))
        if self.progress != new_progress:
            self.progress = new_progress
            self.update_view()

    def set_text(self, new_text):
        if self.text != str(new_text):
            self.text = str(new_text)
            self.update_view()

    def update_view(self):
        self.image.fill((0, 0, 0, 0))

        self.image.blit(self.base_surface, (0, 0))

        current_fill_w = int(self.max_fill_w * self.progress)

        if current_fill_w > 0 and self.fill_h > 0:
            if self.crop_fill:
                crop_rect = pygame.Rect(0, 0, current_fill_w, self.fill_h)
                self.image.blit(self.fill_surface_full, (self.offset_x, self.offset_y), area=crop_rect)
            else:
                current_fill = self.fill_generator.generate_surface(current_fill_w, self.fill_h)
                self.image.blit(current_fill, (self.offset_x, self.offset_y))

        if self.text:
            text_surface = self.font.render(self.text, True, self.font_color)
            text_rect = text_surface.get_rect()
            text_rect.center = (self.w // 2, self.h // 2)
            self.image.blit(text_surface, text_rect)

    def draw(self, surface):
        if hasattr(self, '_x') and hasattr(self, '_y'):
            self.rect.topleft = (self._x, self._y)
        surface.blit(self.image, self.rect.topleft)