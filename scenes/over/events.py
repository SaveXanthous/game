from core.events.base_events import BaseEvents
from ui.decorator.register_ui_element import ui_elements


class GameOverEvents(BaseEvents):
    def process(self, event):
        for element in list(ui_elements.values()):
            if hasattr(element, 'handle_event'):
                element.handle_event(event)