import asyncio
import logging
import time
from random import sample, shuffle

from emoji import EMOJI_DATA
from textual.app import ComposeResult
from textual.containers import Container, Grid
from textual.screen import Screen
from textual.widgets import Button, Label, Static

logger = logging.getLogger(__name__)


class CardGrid(Grid):
    def __init__(self, width: int, height: int, symbols: list[str]) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.card_symbols = symbols
        self.styles.grid_size_rows = self.height
        self.styles.grid_size_columns = self.width
        logger.debug(f"Card symbols: {len(self.card_symbols)}")

    def compose(self):
        """Pre-define children that will be mounted with the grid"""
        for x in range(self.height):
            for y in range(self.width):
                position = x * self.width + y
                yield Card(self.card_symbols[position], (x, y))


class Card(Button):
    """A single card in the memory game."""

    def __init__(self, symbol: str, position: tuple[int, int]):
        super().__init__("?")
        self.symbol = symbol
        self.position = position
        self.is_flipped = False
        self.is_matched = False

    def flip(self):
        """Flip the card."""
        self.is_flipped = not self.is_flipped
        if self.is_flipped:
            self.label = self.symbol
            self.add_class("-flipped")
        else:
            self.label = "?"
            self.remove_class("-flipped")


class ScoreBoard(Container):
    """Display player scores."""

    def __init__(self):
        super().__init__()
        self.player1_score = 0
        self.player2_score = 0
        self.current_player = 1

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Score:", classes="score"),
            Label(
                f"Player 1: {self.player1_score} | Player 2: {self.player2_score}",
                classes="score",
            ),
            id="score-container",
        )
        yield Label(f"Current Player: {self.current_player}", id="current-player")

    def update_score(self, player: int):
        """Update the score for a player."""
        if player == 1:
            self.player1_score += 1
        else:
            self.player2_score += 1
        self.query_one(Label).update(
            f"Player 1: {self.player1_score} | Player 2: {self.player2_score}"
        )

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 3 - self.current_player  # Switches between 1 and 2
        self.query(Label)[1].update(f"Current Player: {self.current_player}")


class GameplayScreen(Screen):
    """Main screen for the memory game."""

    CSS_PATH = "gameplay_screen.tcss"

    def __init__(self):
        super().__init__()
        self.board_height = 0
        self.board_width = 0
        self.flipped_cards: list[Card] = []
        self.can_flip = True

    def set_dimensions(self, board_width: int, board_height: int) -> None:
        self.board_width = board_width
        self.board_height = board_height

        self.card_symbols = sample(list(EMOJI_DATA.keys()), board_width * board_height)
        shuffle(self.card_symbols)
        logger.debug(f"Card symbols: {self.card_symbols}")

    def update_board_size(self) -> None:
        board_size = self.query_one("#board-size", Static)
        board_size.update(f"Board Size: {self.board_width}x{self.board_height}")

    def mount_grid(self) -> None:
        grid = CardGrid(self.board_width, self.board_height, self.card_symbols)
        self.mount(grid)

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Memory Game", id="game-title"),
            Static(
                f"Board Size: {self.board_height}x{self.board_width}", id="board-size"
            ),
            ScoreBoard(),
            id="game-container",
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if not self.can_flip:
            return

        card = event.button
        if isinstance(card, Card) and not card.is_flipped and not card.is_matched:
            card.flip()
            self.flipped_cards.append(card)

            if len(self.flipped_cards) == 2:
                self.can_flip = False
                await self.check_match()

    async def check_match(self) -> None:
        """Check if the two flipped cards match."""
        card1, card2 = self.flipped_cards
        scoreboard = self.query_one(ScoreBoard)

        # Wait a moment to show both cards
        # await asyncio.sleep(5.0)

        if card1.symbol == card2.symbol:
            card1.is_matched = card2.is_matched = True
            scoreboard.update_score(scoreboard.current_player)
        else:
            # TO DO:
            # add NEXT button to move to next player

            # card1.flip()
            # card2.flip()
            scoreboard.switch_player()

        self.flipped_cards = []
        self.can_flip = True
