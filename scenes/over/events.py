import pygame
from core.events.base_events import BaseEvents
from utils.json_handler import JSONHandler


class GameOverEvents(BaseEvents):
    def process(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.scene.nickname = self.scene.nickname[:-1]

            elif event.key == pygame.K_RETURN:
                nickname = self.scene.nickname.strip()
                if nickname:
                    filepath = "data/scores/scores.json"

                    JSONHandler.update(filepath, self.scene.score, nickname)

                    self.game_manager.events_manager.remove_events(self)

                    self.game_manager.stop()

            else:
                if len(self.scene.nickname) < 12 and (event.unicode.isalnum() or event.unicode in " _-"):
                    self.scene.nickname += event.unicode