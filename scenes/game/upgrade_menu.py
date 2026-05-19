import pygame
import random

from entities.upgrades_list.upgrades_list import UPGRADES_LIST


class UpgradeMenu:
    def __init__(self, scene):
        self.scene = scene
        self.active = False
        self.current_upgrades = []
        self.cards = []

        pygame.font.init()
        self.font_title = pygame.font.Font(None, 64)
        self.font_text = pygame.font.Font(None, 36)

    def show(self):
        self.active = True
        self.scene.is_paused = True

        tracker = self.scene.ability_manager.acquired_upgrades
        available_upgrades = []

        for upg in UPGRADES_LIST:
            current_level = tracker.get(upg["id"], 0)

            if current_level < upg["max_level"]:
                available_upgrades.append(upg)

        sample_size = min(3, len(available_upgrades))

        if sample_size > 0:
            self.current_upgrades = random.sample(available_upgrades, sample_size)
        else:
            print("All upgrades at max level")
            self.hide()
            return

        self.cards.clear()
        screen_w, screen_h = self.scene.game_manager.screen.get_size()
        card_w, card_h = 250, 350
        spacing = 50

        total_width = (card_w * sample_size) + (spacing * (sample_size - 1))
        start_x = (screen_w - total_width) // 2
        start_y = (screen_h - card_h) // 2

        for i, upgrade in enumerate(self.current_upgrades):
            rect = pygame.Rect(start_x + i * (card_w + spacing), start_y, card_w, card_h)
            self.cards.append({"rect": rect, "data": upgrade})

    def hide(self):
        self.active = False
        self.scene.is_paused = False

    def draw(self, screen):
        if not self.active:
            return

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title_surf = self.font_title.render("New level!", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surf, title_rect)

        for card in self.cards:
            rect = card["rect"]
            data = card["data"]

            pygame.draw.rect(screen, (50, 50, 60), rect, border_radius=15)
            pygame.draw.rect(screen, (200, 200, 200), rect, width=3, border_radius=15)

            text_surf = self.font_text.render(data["description"], True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            screen.blit(text_surf, text_rect)

    def handle_click(self, mouse_pos):
        if not self.active:
            return False

        for card in self.cards:
            if card["rect"].collidepoint(mouse_pos):
                self.scene.ability_manager.apply_upgrade(card["data"])
                self.hide()
                return True
        return False
