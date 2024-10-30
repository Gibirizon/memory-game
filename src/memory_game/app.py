import logging

from textual.app import App

from memory_game.config import configure_logger, get_configuration
from memory_game.gameplay.gameplay_screen import GameplayScreen

logger = logging.getLogger(__name__)


class MemoryApp(App):
    """Textual app to play the memory game."""

    def __init__(self, config: dict[str, str]) -> None:
        super().__init__()
        self.config = config

    def on_mount(self) -> None:
        self.push_screen(GameplayScreen(self.config))


def main():
    configure_logger()
    config = get_configuration()

    app = MemoryApp(config=config)
    app.run()


if __name__ == "__main__":
    main()
