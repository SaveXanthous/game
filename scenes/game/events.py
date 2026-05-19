import pygame
from pygame.math import Vector2

from core.events.base_events import BaseEvents
from entities.ability.ability import Ability

class PlayerControlsEvents(BaseEvents):
    def __init__(self, game_manager, scene, ability_manager):
        super().__init__(game_manager, scene)
        self.ability_manager = ability_manager

        self.movement_keys = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False
        }

    def process(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if getattr(self.scene, 'is_paused', False):
                if self.scene.upgrade_menu.handle_click(event.pos):
                    self._resync_keys()
                    return

        if getattr(self.scene, 'is_paused', False):
            if event.type == pygame.KEYUP and event.key in self.movement_keys:
                self.movement_keys[event.key] = False
                self._update_player_acceleration()
            return

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            is_pressed = (event.type == pygame.KEYDOWN)

            if is_pressed and event.key == pygame.K_z:
                self.ability_manager.use_abilities("arrow")

            if event.key in self.movement_keys:
                self.movement_keys[event.key] = is_pressed
                self._update_player_acceleration()

    def _resync_keys(self):
        keys = pygame.key.get_pressed()

        for key in self.movement_keys:
            self.movement_keys[key] = keys[key]

            self._update_player_acceleration()

    def _update_player_acceleration(self):
        acceleration = Vector2(0, 0)

        if self.movement_keys[pygame.K_LEFT]: acceleration.x = -1
        if self.movement_keys[pygame.K_RIGHT]: acceleration.x = 1
        if self.movement_keys[pygame.K_UP]: acceleration.y = -1
        if self.movement_keys[pygame.K_DOWN]: acceleration.y = 1

        if self.movement_keys[pygame.K_LEFT] and self.movement_keys[pygame.K_RIGHT]:
            acceleration.x = 0
        if self.movement_keys[pygame.K_UP] and self.movement_keys[pygame.K_DOWN]:
            acceleration.y = 0

        if acceleration.length() != 0:
            acceleration = acceleration.normalize()

        self.scene.player.input_acceleration = acceleration