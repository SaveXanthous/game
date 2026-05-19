import pygame

from ui.elements.interfaces.easing_movable import EasingMovable
from ui.elements.interfaces.scalable import Scalable
from ui.elements.interfaces.positionable import Positionable
from ui.utils.three_slice_image import ThreeSliceImage
from ui.decorator.register_ui_element import register_ui_element

@register_ui_element
class Label(Scalable, Positionable, EasingMovable):
    def __init__(self, id, x, y, w, h, text, font_size=36, font_color=(255, 255, 255), font_name='monospace',
                 show_bg=False, bg_image_path=None, bg_color_index=0):

        self.font_color = font_color
        self.text = text
        self.image = None
        self.rect = None

        self.show_bg = show_bg
        self.bg_image_path = bg_image_path
        self.bg_color_index = bg_color_index

        self.w = self.scaled_width(w)
        self.h = self.scaled_height(h)

        font_size = int(self.scaled_size_front(font_size))
        self.font = pygame.font.SysFont(font_name, font_size)

        self.update_text()

        self.x = x
        self.y = y

        self.rect.topleft = (self._x, self._y) if hasattr(self, '_x') else (self.x, self.y)

    def update_text(self):
        text_surface = self.font.render(self.text, True, self.font_color)

        if self.show_bg and self.bg_image_path:
            self.image = ThreeSliceImage(self.bg_image_path, self.bg_color_index).generate_surface(self.w, self.h)

            text_rect = text_surface.get_rect()
            text_rect.center = (self.w // 2, self.h // 2)
            self.image.blit(text_surface, text_rect)
        else:
            self.image = text_surface

        current_topleft = self.rect.topleft if self.rect else (0, 0)
        self.rect = self.image.get_rect()
        self.rect.topleft = current_topleft

    def set_text(self, new_text):
        if self.text != str(new_text):
            self.text = str(new_text)
            self.update_text()
            if hasattr(self, '_x') and hasattr(self, '_y'):
                self.rect.topleft = (self._x, self._y)
            elif hasattr(self, 'x') and hasattr(self, 'y'):
                self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        if hasattr(self, '_x') and hasattr(self, '_y'):
            self.rect.topleft = (self._x, self._y)
        surface.blit(self.image, self.rect.topleft)
