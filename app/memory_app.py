import logging

from textual.app import App

from app.gameplay.gameplay_screen import GameplayScreen

logger = logging.getLogger(__name__)


class MemoryApp(App):
    """Textual app to play the memory game."""

    def __init__(self, config: dict[str, str]) -> None:
        super().__init__()
        self.config = config

    def on_mount(self) -> None:
        self.push_screen(GameplayScreen(self.config))
