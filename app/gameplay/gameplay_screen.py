import logging
from random import sample, shuffle
from typing import cast

from pyfiglet import figlet_format
from rich.console import RenderableType
from rich_pixels import Pixels
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Container, Grid, Vertical
from textual.events import Mount
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Footer, Header, Label, Static

from app.config_prompt.config_prompt_screen import ConfigPromptScreen
from app.game_over.game_over_screen import GameOverScreen
from app.game_saver.game_save_manager import (
    BoardState,
    CardsState,
    GameSaveManager,
    GameState,
    PlayersState,
    PlayerState,
)

logger = logging.getLogger(__name__)


class ImageWidget(Widget):
    """A widget that displays images using rich-pixels with no spacing."""

    def __init__(self, image_path: str) -> None:
        super().__init__()
        self.image_path = "images/" + image_path

    def render(self) -> RenderableType:
        pixels = Pixels.from_image_path(self.image_path)
        return pixels


class CardGrid(Grid):
    def __init__(
        self,
        width: int,
        height: int,
        symbols: list[str],
        cards_matched: list[bool] = [],
    ) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.card_symbols = symbols
        self.styles.grid_size_rows = self.height
        self.styles.grid_size_columns = self.width
        self.matched_cards = cards_matched
        logger.debug(f"Card symbols: {len(self.card_symbols)}")

    def compose(self):
        """Pre-define children that will be mounted with the grid"""
        for x in range(self.height):
            for y in range(self.width):
                position = x * self.width + y
                yield Card(self.card_symbols[position], (x, y), classes="card")

    def on_mount(self):
        if self.matched_cards:
            for index, card in enumerate(cast("list[Card]", self.query("Card.card"))):
                logger.info(f"Card {index}: {card.symbol}")
                if self.matched_cards[index]:
                    card.is_matched = True
                    card.flip()


class Card(Button):
    """A single card in the memory game."""

    def __init__(self, symbol: str, position: tuple[int, int], **kwargs) -> None:
        super().__init__(**kwargs)
        self.symbol = symbol
        self.position = position
        self.is_flipped = False
        self.is_matched = False

    def compose(self) -> ComposeResult:
        yield ImageWidget("question_mark.png")

    def flip(self):
        """Flip the card."""
        self.is_flipped = not self.is_flipped
        images = self.query("ImageWidget")
        if images:
            images.last().remove()
        if self.is_flipped:
            self.mount(ImageWidget(self.symbol))
        else:
            self.mount(ImageWidget("question_mark.png"))


class ScoreBoard(Vertical):
    """Display player scores and who's turn it is."""

    def __init__(self):
        super().__init__()
        self.player1_score = 0
        self.player2_score = 0
        self.current_player = 1

    def compose(self) -> ComposeResult:
        with Vertical(id="score-container"):
            yield Static("Score:", classes="score")
            yield Label(
                f"Player 1: {self.player1_score} | Player 2: {self.player2_score}",
                classes="score",
            )
        yield Label(f"Current Player: {self.current_player}", id="current-player")

    def load_attributes_from_file(
        self, player1_score: int, player2_score: int, current_player: int
    ):
        """Load attributes from file."""
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.current_player = current_player
        self.query_one(Label).update(
            f"Player 1: {self.player1_score} | Player 2: {self.player2_score}"
        )
        cast(Label, self.query_one("#current-player")).update(
            f"Current Player: {self.current_player}"
        )

    def update_score(self, player: int):
        """Update the score for a player."""
        if player == 1:
            self.player1_score += 1
        else:
            self.player2_score += 1
        label = self.query_one(Label)
        label.update(f"Player 1: {self.player1_score} | Player 2: {self.player2_score}")

        score_container = self.query_one("#score-container")
        score_container.styles.animate(
            "background",
            "goldenrod",
            duration=0.5,
        )
        score_container.styles.animate(
            "color",
            "darkslateblue",
            duration=0.5,
        )

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 3 - self.current_player  # Switches between 1 and 2
        cast(Label, self.query_one("#current-player")).update(
            f"Current Player: {self.current_player}"
        )


class GameplayScreen(Screen):
    """Main screen for the memory game."""

    CSS_PATH = "gameplay_screen.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit the game"),
        ("s", "save", "Save the game"),
    ]

    def __init__(self, config: dict[str, str]):
        super().__init__()
        self.config = config
        self.board_height = 0
        self.board_width = 0
        self.flipped_cards: list[Card] = []
        self.can_flip = True

    def compose(self) -> ComposeResult:
        logger.debug("Composing screen...")
        yield Header()
        with Grid(id="header"):
            yield Static(figlet_format("Memory\nGame", font="big"), id="game-title")
            yield Static(f"Board Size: {self.board_height}x{self.board_width}", id="board-size")
            yield ScoreBoard()
        yield Footer()

    @on(Mount)
    def load_game_state(self) -> None:
        self.title = "Memory Game"
        if not self.config.get("load"):
            self.configure_game()
            return

        logger.debug("Loading game state from file...")
        """Load game state from file."""
        save_manager = GameSaveManager(
            self.config.get("game_load_file", "game_save.dat"),
            self.config.get("key_load_file", "save.key"),
        )
        if game_state := save_manager.load_game():
            logger.info(f"Game state: {game_state}")
            self.update_board_size(game_state.board.width, game_state.board.height)

            scoreboard = self.query_one(ScoreBoard)
            scoreboard.load_attributes_from_file(
                game_state.players.player1.score,
                game_state.players.player2.score,
                game_state.players.current_player,
            )

            self.card_symbols = game_state.cards.all_cards
            grid = CardGrid(
                self.board_width,
                self.board_height,
                self.card_symbols,
                game_state.cards.matched_cards,
            )

            self.mount(grid)

            # Game state loaded, no need to start a new game
            self.app.notify("Game state loaded", timeout=5)
        else:
            logger.warning("No saved game found.")

            # Create a new game
            self.app.notify("Could not load game state, starting a new game...", timeout=5)
            self.configure_game()

    @work
    async def configure_game(self) -> None:
        """Configure the game."""
        logger.info(f"Config before prompt screen: {self.config}")

        board_dimensions = await self.app.push_screen_wait(
            ConfigPromptScreen(
                self.config.get("width"),
                self.config.get("height"),
            )
        )

        logger.info(f"Config after prompt screen: {self.config}")

        # set dimensions and display grid

        self.update_board_size(board_dimensions["board_width"], board_dimensions["board_height"])
        self.mount_grid()

    def action_save(self) -> None:
        save_manager = GameSaveManager(
            self.config.get("game_save_file", "game_save.dat"),
            self.config.get("key_save_file", "save.key"),
        )
        scoreboard = self.query_one(ScoreBoard)
        all_cards = cast("list[Card]", self.query("Card.card"))
        game_state = GameState(
            board=BoardState(width=self.board_width, height=self.board_height),
            players=PlayersState(
                player1=PlayerState(score=scoreboard.player1_score),
                player2=PlayerState(score=scoreboard.player2_score),
                current_player=scoreboard.current_player,
            ),
            cards=CardsState(
                all_cards=self.card_symbols,
                matched_cards=[card.is_matched for card in all_cards],
            ),
        )
        saved_file, key_file = save_manager.save_game(game_state)
        self.app.notify(f"Game saved to {saved_file}\n Key saved to {key_file}", timeout=10)

    def action_quit(self) -> None:
        self.app.exit()

    def update_board_size(self, board_width: int, board_height: int) -> None:
        self.board_width = board_width
        self.board_height = board_height
        board_size = self.query_one("#board-size", Static)
        board_size.update(f"Board Size: {self.board_width}x{self.board_height}")

    def mount_grid(self) -> None:
        # Generate cards by choosing images from 1 to 18, then doubling them and shuffling to place them in the grid
        self.card_symbols = sample(
            [f"{i}.png" for i in range(1, 19)],
            int((self.board_width * self.board_height) / 2),
        )
        self.card_symbols.extend(self.card_symbols)
        shuffle(self.card_symbols)
        logger.debug(f"Card symbols: {self.card_symbols}")

        grid = CardGrid(self.board_width, self.board_height, self.card_symbols)
        self.mount(grid)

    @on(Button.Pressed, ".card")
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""

        if not self.can_flip:
            return

        # when new card is pressed, animate score container to go back to previous color
        score_container = self.query_one("#score-container")
        score_container.styles.animate(
            "background",
            "darkslateblue",
            duration=0.5,
        )
        score_container.styles.animate(
            "color",
            "goldenrod",
            duration=0.5,
        )

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

        if card1.symbol == card2.symbol:
            card1.is_matched = card2.is_matched = True
            scoreboard.update_score(scoreboard.current_player)
            self.flipped_cards = []
            self.can_flip = True

            # check is game over
            await self.check_game_over()

        else:
            button_container = Container(
                Button("Next player", id="next-button"), id="button-container"
            )
            self.mount(button_container)
            scoreboard.switch_player()

    async def check_game_over(self) -> None:
        """Check if the game is over."""
        cards = cast("list[Card]", self.query("Card.card"))
        matched_cards = [True if card.is_matched else False for card in cards]
        if all(matched_cards):
            self.app.push_screen(GameOverScreen())

    @on(Button.Pressed, "#next-button")
    def next_player_turn(self, event: Button.Pressed) -> None:
        self.query_one("#button-container").remove()

        card1, card2 = self.flipped_cards
        card1.flip()
        card2.flip()

        self.flipped_cards = []
        self.can_flip = True
