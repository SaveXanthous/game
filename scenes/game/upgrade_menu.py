import pygame
import random

from entities.upgrades_list.upgrades_list import UPGRADES_LIST
from ui.elements.ui_panel import Panel
from ui.elements.ui_button import Button
from ui.elements.ui_label import Label


class UpgradeMenu:
    PANEL_IMG = "data/ui/panel/RegularPaper.png"
    SLOT_BG_IMG = "data/ui/panel/SpecialPaper.png"
    CARD_NORMAL_IMG = "data/ui/button/BigBlueButton_Regular.png"
    CARD_PRESSED_IMG = "data/ui/button/BigBlueButton_Pressed.png"

    PANEL_STYLE = "nine_slice"
    SLOT_STYLE = "nine_slice"
    CARD_STYLE = "nine_slice"

    def __init__(self, scene):
        self.scene = scene
        self.active = False
        self.current_upgrades = []

        self.bg_panel = None
        self.title_label = None

        self.ui_slot_panels = []
        self.ui_icons = []
        self.ui_cards = []

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

        self.ui_slot_panels.clear()
        self.ui_icons.clear()
        self.ui_cards.clear()

        panel_w, panel_h = 1050, 600
        slot_w, slot_h = 300, 440
        spacing = 30

        self.bg_panel = Panel(
            "upgrade_bg_panel",
            x=0, y=900,
            w=panel_w, h=panel_h,
            image_path=self.PANEL_IMG,
            style=self.PANEL_STYLE
        )

        self.bg_panel.move_by_easing(y=900)

        self.title_label = Label(
            "upgrade_title",
            x=0, y=900-250,
            w=1140, h=90,
            text="Choose an Upgrade!",
            font_size=42,
            font_color=(255, 230, 150),
            bg_image_path='data/ui/label/BigRibbons.png',
            show_bg=True,
            bg_color_index=0
        )

        self.title_label.move_by_easing(y=900)

        total_slots_w = (slot_w * sample_size) + (spacing * (sample_size - 1))
        start_offset_x = - (total_slots_w // 2) + (slot_w // 2)

        base_y_offset = 50 + 900

        for i, upgrade in enumerate(self.current_upgrades):
            self.kill()

            slot_x_offset = start_offset_x + i * (slot_w + spacing)

            slot_panel = Panel(
                f"upgrade_slot_bg_{i}",
                x=slot_x_offset,
                y=base_y_offset,
                w=slot_w,
                h=slot_h,
                image_path=self.SLOT_BG_IMG,
                style=self.SLOT_STYLE
            )
            self.ui_slot_panels.append(slot_panel)
            slot_panel.move_by_easing(y=900)

            icon_path = upgrade.get("image", "data/ui/panel/DefaultIcon.png")
            icon_panel = Panel(
                f"upgrade_icon_{i}",
                x=slot_x_offset,
                y=base_y_offset + 60,
                w=300, h=300,
                image_path=icon_path,
                style="stretch"
            )
            self.ui_icons.append(icon_panel)
            icon_panel.move_by_easing(y=900)

            def make_action(upg_data=upgrade):
                self.scene.ability_manager.apply_upgrade(upg_data)
                self.hide()

            card_button = Button(
                f"upgrade_card_{i}",
                x=slot_x_offset,
                y=base_y_offset - 130,
                w=260, h=100,
                normal_image_path=self.CARD_NORMAL_IMG,
                pressed_image_path=self.CARD_PRESSED_IMG,
                text=upgrade["description"],
                text_color=(255, 255, 255),
                font_size=28,
                font_name='monospace',
                action=make_action,
                style=self.CARD_STYLE
            )
            self.ui_cards.append(card_button)
            card_button.move_by_easing(y=900)

    def hide(self):
        self.active = False
        self.scene.is_paused = False

        self.bg_panel.move_by_easing(y=900)
        self.title_label.move_by_easing(y=900)

        for slot in self.ui_slot_panels:
            slot.move_by_easing(y=900)

        for icon in self.ui_icons:
            icon.move_by_easing(y=900)

        for card in self.ui_cards:
            card.move_by_easing(y=900)

    def kill(self):
        try:
            if self.bg_panel:
                self.bg_panel.kill()

            if self.title_label:
                self.title_label.kill()

            for slot in self.ui_slot_panels:
                slot.kill()

            for icon in self.ui_icons:
                icon.kill()

            for card in self.ui_cards:
                card.kill()
        except:
            pass

    def handle_event(self, event):
        if not self.active:
            return False

        for card in self.ui_cards:
            card.handle_event(event)

        return True

    def draw(self, screen):
        is_finished = self.bg_panel.is_finished if self.bg_panel else False
        if not self.active and is_finished:
            return

        if self.bg_panel:
            self.bg_panel.draw(screen)
            self.bg_panel.update_easing()

        if self.title_label:
            self.title_label.draw(screen)
            self.title_label.update_easing()

        for slot in self.ui_slot_panels:
            slot.draw(screen)
            slot.update_easing()

        for icon in self.ui_icons:
            icon.draw(screen)
            icon.update_easing()

        for card in self.ui_cards:
            card.draw(screen)
            card.update_easing()