import logging

from textual import work
from textual.app import App

from app.config_prompt.config_prompt_screen import ConfigPromptScreen
from app.gameplay.gameplay_screen import GameplayScreen

logger = logging.getLogger(__name__)


class MemoryApp(App):
    """Textual app to play the memory game."""

    def __init__(self, config: dict[str, int]) -> None:
        super().__init__()
        self.config = config
        self.gameplay_screen = GameplayScreen()

    @work
    async def on_mount(self) -> None:
        """Handle mount event with different flows for existing and new configs."""
        self.push_screen(self.gameplay_screen)
        self.config = await self.push_screen_wait(
            ConfigPromptScreen(self.config["board_width"], self.config["board_height"])
        )

        logger.info(f"Config after prompt screen: {self.config}")

        # set dimensions and display grid
        self.setup_board()

    def setup_board(self) -> None:
        self.gameplay_screen.update_board_size(
            self.config["board_width"], self.config["board_height"]
        )
        self.gameplay_screen.mount_grid()
