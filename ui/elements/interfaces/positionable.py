import pygame


class Positionable:
    @property
    def x(self):
        return self._x if hasattr(self, '_x') else 0

    @property
    def y(self):
        return self._y if hasattr(self, '_y') else 0

    @x.setter
    def x(self, value):
        if hasattr(self, '_x'):
            self._x = value
            if hasattr(self, 'rect') and self.rect:
                self.rect.x = int(self._x)
            return

        surf = self.surface if hasattr(self, 'surface') and self.surface else pygame.display.get_surface()
        surf_w = surf.get_size()[0] if surf else 800
        w = self.rect.width if hasattr(self, 'rect') and self.rect else 0

        final_x = (surf_w // 2) - (w // 2) - value
        self._x = self.scaled_x(final_x) if hasattr(self, 'scaled_x') else final_x

    @y.setter
    def y(self, value):
        if hasattr(self, '_y'):
            self._y = value
            if hasattr(self, 'rect') and self.rect:
                self.rect.y = int(self._y)
            return

        surf = self.surface if hasattr(self, 'surface') and self.surface else pygame.display.get_surface()
        surf_h = surf.get_size()[1] if surf else 600
        h = self.rect.height if hasattr(self, 'rect') and self.rect else 0

        final_y = (surf_h // 2) - (h // 2) - value
        self._y = self.scaled_y(final_y) if hasattr(self, 'scaled_y') else final_y