import pygame

from utils.timer import Timer


class Animation:
    def __init__(self, sheet, frame_width, frame_height, scale=1, duration=100, loop=True):

        self.frames = []
        self.loop = loop
        self.timer = Timer(duration)
        self.current_frame = 0
        self.finished = False

        sheet_width, sheet_height = sheet.get_size()
        for y in range(0, sheet_height, frame_height):
            for x in range(0, sheet_width, frame_width):
                frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))

                if scale != 1:
                    new_size = (int(frame_width * scale), int(frame_height * scale))
                    frame = pygame.transform.scale(frame, new_size)

                self.frames.append(frame)

    def get_current_frame(self):
        return self.frames[self.current_frame]

    def reset(self):
        self.current_frame = 0
        self.finished = False
        self.timer.next_tick = pygame.time.get_ticks() + self.timer.duration

    def update(self):
        if self.finished and not self.loop:
            return

        if self.timer.check():
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
