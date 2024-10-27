import logging

from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.screen import ModalScreen
from textual.validation import Number
from textual.widgets import Button, Input, Label, Static

logger = logging.getLogger(__name__)


class ConfigPromptScreen(ModalScreen):
    """The screen for the configuration prompt to get board dimensions."""

    CSS_PATH = "config_prompt_screen.tcss"

    def __init__(self, width: str | None, height: str | None) -> None:
        super().__init__()
        self.width = width
        self.height = height

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Board Size", id="title"),
            Label("Board Width"),
            Input(
                id="input_board_width",
                type="integer",
                value=self.width if self.width else None,
                placeholder="Enter board width...",
                validators=[
                    Number(
                        minimum=2,
                        maximum=6,
                    )
                ],
            ),
            Label("Board Height"),
            Input(
                id="input_board_height",
                type="integer",
                value=self.height if self.height else None,
                placeholder="Enter board height...",
                validators=[
                    Number(
                        minimum=2,
                        maximum=6,
                    )
                ],
            ),
            Button("Confirm", id="submit_button", variant="primary"),
            id="form-container",
            classes="form",
        )

    @on(Input.Changed)
    def add_titles_to_inputs(self, event: Input.Changed) -> None:
        """
        Clear warning message when user starts typing.
        Validate input as user types.
        """
        existing_warning = self.query("#warning-message")
        if existing_warning:
            existing_warning.last().remove()

        if event.validation_result and event.validation_result.is_valid:
            event.input.border_title = "Appropriate value"
        else:
            event.input.border_title = "Invalid value - must be between 2 and 6"

    def show_warning(self, message: str) -> None:
        """Add or update warning message."""
        existing_warning = self.query("#warning-message")
        try:
            # Update existing label
            existing_warning = self.query_one("#warning-message", expect_type=Label)
            existing_warning.update(message)
        except NoMatches as e:
            logger.info(f"Expected error when trying to get Label from Query: {e}")
            # Create new label if doesn't exist
            warning_label = Label(message, id="warning-message")
            self.query_one("#form-container").mount(warning_label)

    @on(Button.Pressed, "#submit_button")
    def validate_and_submit(self) -> None:
        """Validate inputs when submit button is pressed."""
        height_input = self.query_one("#input_board_height", Input)
        width_input = self.query_one("#input_board_width", Input)

        # Check if both inputs have values
        if not height_input.value or not width_input.value:
            self.show_warning("Both fields are required!")
            return

        height = int(height_input.value)
        width = int(width_input.value)

        # Validate ranges
        if not (2 <= height <= 6 and 2 <= width <= 6):
            self.show_warning("Board size must be between 2 and 6!")
            return

        # All cards number should be an even number
        if (height * width) % 2:
            self.show_warning("Board size must be an even number!")
            return

        # Submit values
        self.dismiss(
            {
                "board_width": int(width_input.value),
                "board_height": int(height_input.value),
            }
        )
