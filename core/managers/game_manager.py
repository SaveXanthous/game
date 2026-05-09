import pygame
from game.initializer_game_manager import Initializer


class GameManager(Initializer):
    def start(self):
        while self.running:
            time_delta = self.clock.tick(self.FPS) / 1000.0

            self.process_events()

            self.ui_manager.manager.update(time_delta)

            self.screen.fill((20, 20, 30))

            self.scenes_manager.update()
            self.scenes_manager.draw()

            self.ui_manager.manager.draw_ui(self.screen)

            pygame.display.update()

        pygame.quit()

    
    def stop(self):
        self.running = False

    def process_events(self):
        for system_event in pygame.event.get():
            self.ui_manager.manager.process_events(system_event)

            for handler_event in self.events_manager.events:
                handler_event.process(system_event)
