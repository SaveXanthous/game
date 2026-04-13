import pygame

from core.events.base_events import BaseEvents

class DefaultEvents(BaseEvents):
    @classmethod
    def process(cls, event):
        if event.type == pygame.QUIT:
            cls._GameManager.stop()