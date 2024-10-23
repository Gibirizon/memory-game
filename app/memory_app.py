import logging
from typing import cast

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from app.config_prompt_screen import ConfigPromptScreen
from app.gameplay_screen import GameplayScreen

logger = logging.getLogger(__name__)


class MemoryApp(App):
    """Textual app to play the memory game."""

    SCREENS = {
        "config": ConfigPromptScreen,
        "dashboard": GameplayScreen,
    }

    def __init__(self, config: dict[str, int] | None) -> None:
        super().__init__()
        self.config = config

    @work
    async def on_mount(self) -> None:
        """Handle mount event with different flows for existing and new configs."""
        if self.config:
            # Flow when config exists:
            # 1. Set dimensions first
            # 2. Then push dashboard screen
            self.set_board_dimensions(
                self.config["board_width"], self.config["board_height"], update=False
            )
            self.push_screen("dashboard")
        else:
            # Flow when no config exists:
            # 1. Push dashboard screen first
            # 2. Get config from config screen
            # 3. Set dimensions and update board
            self.push_screen("dashboard")
            self.config = await self.push_screen_wait("config")
            logger.info(f"Config: {self.config}")

            self.set_board_dimensions(
                self.config["board_width"], self.config["board_height"]
            )

        # Finally, mount grid for both flows
        dashboard_screen = cast(GameplayScreen, self.get_screen("dashboard"))

        # TO DO: when self.config, wait for compose, and then mount grid
        dashboard_screen.mount_grid()

    def set_board_dimensions(
        self, board_width: int, board_height: int, update: bool = True
    ) -> None:
        dashboard_screen = cast(GameplayScreen, self.get_screen("dashboard"))
        dashboard_screen.set_dimensions(board_width, board_height)
        if update:
            dashboard_screen.update_board_size()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
