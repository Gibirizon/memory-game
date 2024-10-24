from pyfiglet import figlet_format
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class GameOverScreen(ModalScreen):
    CSS_PATH = "game_over_screen.tcss"

    def __init__(self, player1_score: int, player2_score: int) -> None:
        """Initialize the GameOverScreen to show which player won."""
        super().__init__()
        self.player1_score = player1_score
        self.player2_score = player2_score
        if self.player1_score > self.player2_score:
            self.who_won = figlet_format("PLAYER 1 WON")
        elif self.player1_score < self.player2_score:
            self.who_won = figlet_format("PLAYER 2 WON")
        else:
            self.who_won = figlet_format("DRAW")

    def compose(self) -> ComposeResult:
        yield Container(
            Static(figlet_format("GAME OVER", font="big"), classes="game-over"),
            Static(self.who_won, classes="game-over"),
            Button("Close", variant="error", id="close-button"),
            classes="game-over-modal",
        )

    def on_button_pressed(self) -> None:
        self.app.pop_screen()
