import logging
import pathlib
from typing import cast

from rich.console import RenderableType
from rich_pixels import Pixels
from textual.app import ComposeResult
from textual.containers import Grid
from textual.widget import Widget
from textual.widgets import Button

logger = logging.getLogger(__name__)

DEFAULT_IMAGE = "question_mark.png"


class ImageWidget(Widget):
    """A widget that displays images using rich-pixels."""

    def __init__(self, image_path: str) -> None:
        super().__init__()

        project_dir = pathlib.Path(__file__).parent.parent.parent.parent
        self.image_path = project_dir / "assets" / "images" / image_path

    def render(self) -> RenderableType:
        pixels = Pixels.from_image_path(self.image_path)
        return pixels


class CardGrid(Grid):
    def __init__(
        self,
        width: int,
        height: int,
        symbols: list[str],
        matched_cards: list[bool] = [],
    ) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.card_symbols = symbols
        self.styles.grid_size_rows = self.height
        self.styles.grid_size_columns = self.width
        self.matched_cards = matched_cards

    def compose(self):
        for x in range(self.height):
            for y in range(self.width):
                position = x * self.width + y
                yield Card(self.card_symbols[position], (x, y), classes="card")

    def on_mount(self):
        """When loading the game from saved state, update matched cards."""
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
        yield ImageWidget(DEFAULT_IMAGE)

    def flip(self):
        """Flip the card to show its symbol."""
        self.is_flipped = not self.is_flipped
        images = self.query("ImageWidget")
        if images:
            images.last().remove()
        if self.is_flipped:
            self.mount(ImageWidget(self.symbol))
        else:
            self.mount(ImageWidget(DEFAULT_IMAGE))
