import pygame

class Timer:

    def __init__(self, duration):
        self.duration = duration
        self.next_tick = pygame.time.get_ticks() + duration
        self.active = True

    def check(self):
        if not self.active:
            return False

        if pygame.time.get_ticks() >= self.next_tick:
            self.next_tick = pygame.time.get_ticks() + self.duration
            return True
        return False

    def duration(self, new_duration):
        self.duration = new_duration
