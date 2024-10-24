from pyfiglet import figlet_format
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class GameOverScreen(ModalScreen):
    CSS_PATH = "game_over_screen.tcss"

    def compose(self) -> ComposeResult:
        game_over_text = figlet_format("GAME OVER", font="big")
        yield Container(
            Static(game_over_text, classes="game-over"),
            Button("Close", variant="error", id="close-button"),
            classes="game-over-modal",
        )

    def on_button_pressed(self) -> None:
        self.app.pop_screen()
