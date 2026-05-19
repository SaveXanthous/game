import pygame
from scenes.base.base_scene import BaseScene
from scenes.over.events import GameOverEvents
from utils.json_handler import JSONHandler


class GameOver(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        self.score = self.game_manager.last_score
        self.nickname = ""

        self.title_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.font = pygame.font.SysFont("Arial", 36)

        self.scores_filepath = "game/data/scores.json"

        game_manager.events_manager.add_events(GameOverEvents(game_manager, self))

    def save_result(self):
        final_nickname = self.nickname.strip()
        JSONHandler.update(self.scores_filepath, self.score, final_nickname)

    def init_ui(self):
        pass

    def draw(self):
        screen = self.game_manager.screen

        screen.fill((15, 15, 25))

        center_x = screen.get_width() // 2

        title_surf = self.title_font.render("GAME OVER", True, (220, 40, 40))
        title_rect = title_surf.get_rect(center=(center_x, 150))
        screen.blit(title_surf, title_rect)

        score_surf = self.font.render(f"Your final score: {self.score}", True, (240, 240, 240))
        score_rect = score_surf.get_rect(center=(center_x, 250))
        screen.blit(score_surf, score_rect)

        prompt_surf = self.font.render("Enter your nickname:", True, (160, 160, 160))
        prompt_rect = prompt_surf.get_rect(center=(center_x, 360))
        screen.blit(prompt_surf, prompt_rect)

        nick_text = self.nickname + ("|" if pygame.time.get_ticks() % 1000 < 500 else " ")
        nick_surf = self.font.render(nick_text, True, (255, 215, 0))
        nick_rect = nick_surf.get_rect(center=(center_x, 420))

        box_width = max(300, nick_rect.width + 40)
        pygame.draw.rect(screen, (50, 50, 70), (center_x - box_width // 2, 400, box_width, 45), border_radius=5)
        screen.blit(nick_surf, nick_rect)

        info_surf = self.font.render("Press Enter to save", True, (100, 100, 120))
        info_rect = info_surf.get_rect(center=(center_x, screen.get_height() - 100))
        screen.blit(info_surf, info_rect)


    def update(self):
        pass