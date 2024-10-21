import logging

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Label

from app.config_prompt_screen import ConfigPromptScreen
from app.dashboard_screen import DashboardScreen

logger = logging.getLogger(__name__)


class MemoryApp(App):
    """Textual app to play the memory game."""

    SCREENS = {
        "config": ConfigPromptScreen,
        "dashboard": DashboardScreen,
    }

    def __init__(self, config: dict[str, int] | None) -> None:
        super().__init__()
        self.config = config

    @work
    async def on_mount(self) -> None:
        if self.config:
            dashboard_screen = self.get_screen("dashboard")
            dashboard_screen.set_dimensions(
                self.config["board_height"], self.config["board_width"]
            )

        self.push_screen("dashboard")

        if not self.config:
            self.config = await self.push_screen_wait("config")
            logger.info(f"Config: {self.config}")

            dashboard_screen = self.get_screen("dashboard")
            dashboard_screen.set_dimensions(
                self.config["board_height"], self.config["board_width"]
            )
            dashboard_screen.update_board_size()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
