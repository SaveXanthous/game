import pygame
import pygame_gui
from initializer_game_manager import InitializerGameManager


class GameManager:
    def __init__(self):
        self.running: bool = False
        self.screen: pygame.Surface = None
        self.clock: pygame.time.Clock = None
        self.FPS: int = 60
        self.manager = None  # Для pygame_gui

        InitializerGameManager(self)
    
    def start(self):
        while self.running:
            time_delta = self.clock.tick(self.FPS) / 1000.0

            self.process_events()

            self.manager.update(time_delta)

            self.screen.fill((20, 20, 30))
            self.manager.draw_ui(self.screen)

            pygame.display.update()

        pygame.quit()

    
    def stop(self):
        self.running = False

    
    def process_events(self):
        for system_event in pygame.event.get():
            self.manager.process_events(system_event)

            for handler_event in self.event_manager.events:
                handler_event.process(system_event)

    
    def get_ui_manager(self):
        return self.manager

