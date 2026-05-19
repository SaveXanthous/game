import pygame

from core.events.base_events import BaseEvents

class PlayerControlsEvents(BaseEvents):
    def __init__(self, game_manager, scene, ability_manager):
        super().__init__(game_manager, scene)
        self.ability_manager = ability_manager

    def process(self, event):
        if getattr(self.scene, 'is_paused', False):
            if hasattr(self.scene, 'upgrade_menu') and self.scene.upgrade_menu.active:
                self.scene.upgrade_menu.handle_event(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.ability_manager.use_abilities("arrow")

