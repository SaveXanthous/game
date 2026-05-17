import pygame

from core.events.base_events import BaseEvents
from entities.ability.ability import Ability

class PlayerControlsEvents(BaseEvents):
    def __init__(self, game_manager, scene, ability_manager):
        super().__init__(game_manager, scene)
        self.ability_manager = ability_manager

    def process(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                print("Активация способности через EventsManager!")
                self.ability_manager.use_abilities("ability")

