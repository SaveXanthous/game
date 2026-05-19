import pygame
from game.initializer_game_manager import Initializer


class GameManager(Initializer):
    def start(self):
        while self.running:
            self.time_delta = self.clock.tick(self.FPS) / 1000.0

            self.process_events()

            self.screen.fill((20, 20, 30))

            self.scenes_manager.update()
            self.scenes_manager.draw()

            self.ui_manager.draw()

            pygame.display.update()

        pygame.quit()

    
    def stop(self):
        self.running = False

    def process_events(self):
        for system_event in pygame.event.get():
            for handler_event in self.events_manager.events:
                handler_event.process(system_event)
