import pygame


class EasingMovable:
    DEFAULT_SPEED = 0.12
    EPSILON = 0.5

    def move_by_easing(self, x=None, y=None, on_finished=None):
        base_x = getattr(self, '_target_x', self.x)
        base_y = getattr(self, '_target_y', self.y)

        self._target_x = base_x + x if x is not None else base_x
        self._target_y = base_y + y if y is not None else base_y

        self._on_finished_callback = on_finished
        self.is_moving = True

    @property
    def is_finished(self):
        return not getattr(self, 'is_moving', False)

    def update_easing(self):
        if not getattr(self, 'is_moving', False):
            return

        dx = self._target_x - self.x
        dy = self._target_y - self.y

        if abs(dx) > self.EPSILON:
            self.x += dx * self.DEFAULT_SPEED
        else:
            self.x = self._target_x

        if abs(dy) > self.EPSILON:
            self.y += dy * self.DEFAULT_SPEED
        else:
            self.y = self._target_y

        if self.x == self._target_x and self.y == self._target_y:
            self.is_moving = False

            if hasattr(self, '_on_finished_callback') and self._on_finished_callback:
                self._on_finished_callback()