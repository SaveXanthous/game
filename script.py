import pygame
import pygame_gui
import math
import random
import json

pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# ================= SAVE =================
def save_game():
    data = {
        "points": points,
        "click_value": click_value,
        "auto_income": auto_income,
        "upgrade1_cost": upgrade1_cost,
        "upgrade2_cost": upgrade2_cost
    }
    with open("example/save.json", "w") as f:
        json.dump(data, f)

def load_game():
    try:
        with open("example/save.json", "r") as f:
            return json.load(f)
    except:
        return None

save = load_game()

# Game variables
points = save["points"] if save else 0
click_value = save["click_value"] if save else 1
auto_income = save["auto_income"] if save else 0

upgrade1_cost = save["upgrade1_cost"] if save else 10
upgrade2_cost = save["upgrade2_cost"] if save else 10

multiplier = 1.0

# Panel animation
panel_visible = False
panel_y = -300
panel_target_y = 50
panel_speed = 800

# UI Elements
button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((200, 300), (200, 100)),
    text='CLICK',
    manager=manager
)

points_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((200, 50), (200, 50)),
    text=f'Points: {points}',
    manager=manager
)

# Window instead of panel
window = pygame_gui.elements.UIWindow(
    rect=pygame.Rect((150, panel_y), (300, 300)),
    manager=manager,
    window_display_title='Upgrades'
)

upgrade1_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 50), (200, 50)),
    text='Upgrade Click',
    manager=manager,
    container=window
)
upgrade1_button.set_tooltip("Increase click power")

upgrade2_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 120), (200, 50)),
    text='Auto Income',
    manager=manager,
    container=window
)
upgrade2_button.set_tooltip("Gain points every second")

# Progress bar
progress = pygame_gui.elements.UIProgressBar(
    relative_rect=pygame.Rect((150, 120), (300, 25)),
    manager=manager
)

# Slider (multiplier demo)
slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((50, 200), (200, 30)),
    start_value=1,
    value_range=(1, 5),
    manager=manager,
    container=window
)

running = True
auto_timer = 0

while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                panel_visible = not panel_visible

        manager.process_events(event)

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            multiplier = event.value

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button:
                # crit system
                if random.random() < 0.1:
                    gain = click_value * 5
                else:
                    gain = click_value
                points += gain * multiplier

            if event.ui_element == upgrade1_button:
                if points >= upgrade1_cost:
                    points -= upgrade1_cost
                    click_value += 1
                    upgrade1_cost = int(upgrade1_cost * 1.5)

            if event.ui_element == upgrade2_button:
                if points >= upgrade2_cost:
                    points -= upgrade2_cost
                    auto_income += 1
                    upgrade2_cost = int(upgrade2_cost * 1.5)

    # Auto income
    auto_timer += time_delta
    if auto_timer >= 1:
        points += auto_income * multiplier
        auto_timer = 0

    # Hold click
    if pygame.mouse.get_pressed()[0]:
        points += click_value * time_delta * 5 * multiplier

    # Panel animation
    if panel_visible:
        if panel_y < panel_target_y:
            panel_y += panel_speed * time_delta
    else:
        if panel_y > -300:
            panel_y -= panel_speed * time_delta

    window.set_relative_position((150, int(panel_y)))

    # Progress example (to next 1000)
    progress.set_current_progress(points % 1000)

    # Update UI text
    points_label.set_text(f'Points: {int(points)}')
    upgrade1_button.set_text(f'+Click ({upgrade1_cost})')
    upgrade2_button.set_text(f'+Auto ({upgrade2_cost})')

    manager.update(time_delta)

    screen.fill((20, 20, 30))
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()
