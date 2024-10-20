import logging

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.validation import Number
from textual.widgets import Button, Footer, Header, Input, Label, Static

logger = logging.getLogger(__name__)


class ConfigPromptScreen(ModalScreen[dict[str, int]]):
    """The screen for the configuration prompt."""

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Wymiary planszy", id="title"),
            Label("Wysokość planszy"),
            Input(
                id="input_board_height",
                type="integer",
                placeholder="Wprowadź wysokość planszy...",
                validators=[
                    Number(
                        minimum=1,
                        maximum=20,
                    )
                ],
            ),
            Label("Szerokość planszy"),
            Input(
                id="input_board_width",
                type="integer",
                placeholder="Wprowadź szerokość planszy...",
                validators=[
                    Number(
                        minimum=1,
                        maximum=20,
                    )
                ],
            ),
            Button("Submit", id="submit_button", variant="primary"),
            id="form-container",
            classes="form",
        )

    @on(Input.Changed)
    def add_titles_to_inputs(self, event: Input.Changed) -> None:
        """Validate input as user types."""
        if event.validation_result and event.validation_result.is_valid:
            event.input.border_title = "Odpowiednia wartość"
        else:
            event.input.border_title = "Niepoprawna wartość - musi być z przedziału od 1 do 20"

    @on(Button.Pressed, "#submit_button")
    def check_board_size(self) -> None:
        """Check if board size is valid."""
        height_input = self.query_one("#input_board_height")
        width_input = self.query_one("#input_board_width")
        logger.info(f"Board size: {height_input.value}x{width_input.value}")
        if not (int(height_input.value) * int(width_input.value)) % 2:
            self.dismiss(
                {
                    "board_height": int(height_input.value),
                    "board_width": int(width_input.value),
                }
            )
        else:
            self.query_one("#form-container").mount(
                Label(
                    "Niepoprawne wymiary planszy - iloczyn wysokości i szerokości musi być"
                    " parzysty"
                )
            )


class MemoryApp(App):
    """Textual app to play the memory game."""

    CSS_PATH = "memory_app.tcss"

    def __init__(self, config: dict[str, int] | None) -> None:
        super().__init__()
        self.config = config

    def on_mount(self) -> None:
        if not self.config:
            self.push_screen(ConfigPromptScreen())

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(
            "fsdjf sljfd jsdlfjj flsjkdflkjkljdsfjsldjf kjfljdfk ljflorrem lorem loremldsj " * 8
        )
        yield Footer()
