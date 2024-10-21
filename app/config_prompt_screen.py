import logging

from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.screen import ModalScreen
from textual.validation import Number
from textual.widgets import Button, Input, Label, Static

logger = logging.getLogger(__name__)


class ConfigPromptScreen(ModalScreen[dict[str, int]]):
    """The screen for the configuration prompt."""

    CSS_PATH = "config_prompt_screen.tcss"

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Wymiary planszy", id="title"),
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
            Button("Potwierdź", id="submit_button", variant="primary"),
            id="form-container",
            classes="form",
        )

    @on(Input.Changed)
    def add_titles_to_inputs(self, event: Input.Changed) -> None:
        """Clear warning message when user starts typing."""
        existing_warning = self.query("#warning-message")
        if existing_warning:
            existing_warning.last().remove()

        """Validate input as user types."""
        if event.validation_result and event.validation_result.is_valid:
            event.input.border_title = "Odpowiednia wartość"
        else:
            event.input.border_title = (
                "Niepoprawna wartość - musi być z przedziału od 1 do 20"
            )

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
            self.show_warning("Oba pola muszą być wypełnione!")
            return

        height = int(height_input.value)
        width = int(width_input.value)

        # Validate ranges
        if not (1 <= height <= 20 and 1 <= width <= 20):
            self.show_warning("Wymiary planszy muszą być między 1 a 20!")
            return

        # All cards number should be an even number - show a message
        if (height * width) % 2:
            self.show_warning("Plansza musi zawierać parzystą liczbę kart!")
            return

        # Submit values
        self.dismiss(
            {
                "board_height": int(height_input.value),
                "board_width": int(width_input.value),
            }
        )
