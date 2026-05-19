import pygame

from ui.elements.interfaces.easing_movable import EasingMovable
from ui.elements.interfaces.scalable import Scalable
from ui.elements.interfaces.positionable import Positionable
from ui.utils.nine_slice_image import NineSliceImage
from ui.decorator.register_ui_element import register_ui_element


@register_ui_element
class Panel(Scalable, Positionable, EasingMovable):
    def __init__(self, id, x, y, w, h, image_path, style="nine_slice"):
        """
        id, x, y, w, h, image_path - стандартные параметры.
        style - может быть:
            "nine_slice" -> стандартная 9-slice панель.
            "stretch"    -> обычное изображение, растянутое под w, h.
            "tile_screen"-> заполняет весь экран повторяющимся паттерном (тайлом).
        """
        w = self.scaled_width(w)
        h = self.scaled_height(h)

        if style == "tile_screen":
            self.image = self._generate_tile_screen(image_path)
            self.rect = self.image.get_rect()
            self.x, self.y = 0, 0
        else:
            if style == "nine_slice":
                self.image = NineSliceImage(image_path).generate_surface(w, h)
            elif style == "stretch":
                raw_image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(raw_image, (w, h))

            self.rect = self.image.get_rect()
            self.x = x
            self.y = y

        if hasattr(self, '_x') and hasattr(self, '_y'):
            self.rect.topleft = (self._x, self._y)
        else:
            self.rect.topleft = (self.x, self.y)

    def _generate_tile_screen(self, image_path) -> pygame.Surface:
        display_surface = pygame.display.get_surface()
        screen_w, screen_h = display_surface.get_size()

        tiled_surface = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)

        tile = pygame.image.load(image_path).convert_alpha()
        tile_w, tile_h = tile.get_size()

        for x in range(0, screen_w, tile_w):
            for y in range(0, screen_h, tile_h):
                tiled_surface.blit(tile, (x, y))

        return tiled_surface

    def draw(self, surface):
        if hasattr(self, '_x') and hasattr(self, '_y'):
            self.rect.topleft = (self._x, self._y)

        if surface:
            surface.blit(self.image, self.rect.topleft)