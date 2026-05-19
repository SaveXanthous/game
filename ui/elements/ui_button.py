import pygame

from ui.elements.interfaces.easing_movable import EasingMovable
from ui.elements.interfaces.scalable import Scalable
from ui.elements.interfaces.positionable import Positionable
from ui.utils.nine_slice_image import NineSliceImage
from ui.decorator.register_ui_element import register_ui_element

@register_ui_element
class Button(Scalable, Positionable, EasingMovable):
    def __init__(self, id, x, y, w, h, normal_image_path, pressed_image_path,
                 text="", text_color=(255, 255, 255), font_size=24, font_name='monospace',
                 action=None, style="nine_slice"):
        """
        id, x, y, w, h, normal_image_path, pressed_image_path - стандартные параметры.
        style - может быть:
            "nine_slice" -> стандартная 9-slice кнопка.
            "stretch"    -> обычные изображения, растянутые под w, h.
        """
        w = self.scaled_width(w)
        h = self.scaled_height(h)

        self.style = style

        if self.style == "nine_slice":
            self.normal_image = NineSliceImage(normal_image_path).generate_surface(w, h)
            self.pressed_image = NineSliceImage(pressed_image_path).generate_surface(w, h)
        elif self.style == "stretch":
            raw_normal = pygame.image.load(normal_image_path).convert_alpha()
            raw_pressed = pygame.image.load(pressed_image_path).convert_alpha()
            self.normal_image = pygame.transform.scale(raw_normal, (w, h))
            self.pressed_image = pygame.transform.scale(raw_pressed, (w, h))
        else:
            raw_normal = pygame.image.load(normal_image_path).convert_alpha()
            raw_pressed = pygame.image.load(pressed_image_path).convert_alpha()
            self.normal_image = pygame.transform.scale(raw_normal, (w, h))
            self.pressed_image = pygame.transform.scale(raw_pressed, (w, h))

        self.text = text
        if self.text:
            scaled_font_size = int(self.scaled_size_front(font_size))
            font = pygame.font.SysFont(font_name, scaled_font_size)

            text_surface = font.render(self.text, True, text_color)
            text_rect = text_surface.get_rect()
            text_rect.center = (w // 2, h // 2)

            self.normal_image.blit(text_surface, text_rect)
            self.pressed_image.blit(text_surface, text_rect)

        self.image = self.normal_image
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.topleft = (self.x, self.y)

        self.action = action
        self.is_pressed = False

    def handle_event(self, event):
        self.rect.topleft = (self.x, self.y)

        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if is_hovered:
                self.image = self.pressed_image
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed:
                self.image = self.normal_image
                self.is_pressed = False
                if is_hovered:
                    self.trigger_action()

        elif event.type == pygame.MOUSEMOTION:
            if self.is_pressed and not is_hovered:
                self.image = self.normal_image
            elif self.is_pressed and is_hovered:
                self.image = self.pressed_image

    def trigger_action(self):
        if self.action:
            self.action()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)