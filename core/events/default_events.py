import pygame

from core.events.base_events import BaseEvents

class DefaultEvents(BaseEvents):
    def process(self, event):
        if event.type == pygame.QUIT:
            self._game_manager.stop()