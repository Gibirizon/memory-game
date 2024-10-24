import argparse
import configparser
import logging

from textual.logging import TextualHandler

from app.memory_app import MemoryApp

LOG_FILE = "memory_game.log"
logger = logging.getLogger(__name__)


class ConfigHandler:
    """Handles configuration loading and validation."""

    def __init__(self, setup_file):
        self.config = self.read_config(setup_file)

    def read_config(self, setup_file):
        config = configparser.ConfigParser(interpolation=None)
        logger.info(f"Reading configuration file {setup_file}...")
        config.read(setup_file)
        logger.info("Read configuration file {setup_file}.")
        return config

    def load_config_params(self) -> dict[str, str]:
        """Load configuration from INI file."""

        params = {}
        for section in self.config.sections():
            for key, value in self.config[section].items():
                params[key] = value

        return params


def configure_logger():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_date_format = "%Y-%m-%d %H:%M:%S"
    log_th = TextualHandler()
    log_fh = logging.FileHandler(LOG_FILE)
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=log_date_format,
        handlers=[log_th, log_fh],
    )


def get_configuration() -> dict[str, str]:
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

    # If config file is provided, try to load it
    if var_args["config_file"]:
        config_handler = ConfigHandler(var_args["config_file"])
        params = config_handler.load_config_params()
        logger.info(f"Parameters from INI file: {params}")
        return params

    # If no config file provided, return empty dict
    logger.info("No configuration file provided.")
    return {}


def main():
    configure_logger()

    config = get_configuration()

    app = MemoryApp(config=config)
    app.run()


if __name__ == "__main__":
    main()
