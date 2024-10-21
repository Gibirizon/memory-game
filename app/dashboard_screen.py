from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Label, Static


class DashboardScreen(Screen):
    """Main screen for the memory game."""

    CSS_PATH = "dashboard_screen.tcss"

    def __init__(self):
        super().__init__()
        self.board_height = 0
        self.board_width = 0

    def set_dimensions(self, board_height: int, board_width: int) -> None:
        self.board_height = board_height
        self.board_width = board_width

    def update_board_size(self) -> None:
        board_size = self.query_one("#board-size", Static)
        board_size.update(f"Board Size: {self.board_width}x{self.board_height}")

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Memory Game", id="game-title"),
            Static(
                f"Board Size: {self.board_height}x{self.board_width}", id="board-size"
            ),
            Label("Player 1's turn", id="player-turn"),
            id="game-container",
        )
