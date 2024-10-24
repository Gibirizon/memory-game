import argparse
import configparser
import logging

from app.memory_app import MemoryApp
from textual.logging import TextualHandler

LOG_FILE = "memory_game.log"
DEFAULT_CONFIG = {"board_width": 0, "board_height": 0}
logger = logging.getLogger(__name__)


class ConfigHandler:
    """Handles configuration loading and validation."""

    def __init__(self):
        self.config = configparser.ConfigParser()

    def load_config_file(self, config_path: str) -> dict[str, int]:
        """Load and validate configuration from INI file."""
        if not self.config.read(config_path):
            raise ValueError(f"Could not read config file: {config_path}")

        try:
            # Assuming config file has a [BOARD] section
            height = self.config.getint("BOARD", "height")
            width = self.config.getint("BOARD", "width")

            return {
                "board_width": width,
                "board_height": height,
            }
        except (
            configparser.NoSectionError,
            configparser.MissingSectionHeaderError,
            configparser.NoOptionError,
            ValueError,
        ) as error:
            logger.warning(f"Invalid config file: {str(error)}")
        except Exception as error:
            logger.warning(f"Unexpected error when loading config: {str(error)}")

        # Return default config if config file is invalid
        return DEFAULT_CONFIG


def configure_logger():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_date_format = "%Y-%m-%d %H:%M:%S"
    log_th = TextualHandler()
    log_fh = logging.FileHandler(LOG_FILE)
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        datefmt=log_date_format,
        handlers=[log_th, log_fh],
    )


def get_configuration() -> dict[str, int]:
    """Function to handle configuration loading."""

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Board Game Configuration")
    parser.add_argument(
        "-c",
        "--config_file",
        metavar="config_file",
        type=str,
        help="Path to config file (INI format file)",
        required=False,
    )
    args = parser.parse_args()
    var_args = vars(args)

    config_handler = ConfigHandler()

    # If config file is provided, try to load it
    if var_args["config_file"]:
        return config_handler.load_config_file(var_args["config_file"])

    # If no config file provided, return default config
    return DEFAULT_CONFIG


def main():
    configure_logger()
    config = get_configuration()
    logger.info(f"Configuration from file: {config}")
    app = MemoryApp(config=config)
    app.run()


if __name__ == "__main__":
    main()
