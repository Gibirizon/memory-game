import json
import logging
import os
from dataclasses import asdict, dataclass

from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)


@dataclass
class BoardState:
    width: int
    height: int


@dataclass
class PlayerState:
    score: int


@dataclass
class PlayersState:
    player1: PlayerState
    player2: PlayerState
    current_player: int


@dataclass
class CardsState:
    all_cards: list[str]
    matched_cards: list[bool]


@dataclass
class GameState:
    board: BoardState
    players: PlayersState
    cards: CardsState

    @classmethod
    def from_dict(cls, data: dict) -> "GameState":
        return cls(
            board=BoardState(width=data["board"]["width"], height=data["board"]["height"]),
            players=PlayersState(
                player1=PlayerState(score=data["players"]["player1"]["score"]),
                player2=PlayerState(score=data["players"]["player2"]["score"]),
                current_player=data["players"]["current_player"],
            ),
            cards=CardsState(
                all_cards=data["cards"]["all_cards"],
                matched_cards=data["cards"]["matched_cards"],
            ),
        )


class GameSaveManager:
    def __init__(self, save_file: str = "game_save.dat", key_file: str = "save.key") -> None:
        current_dir = os.getcwd()

        self.save_file = (
            save_file if os.path.isabs(save_file) else os.path.join(current_dir, save_file)
        )
        self.key_file = (
            key_file if os.path.isabs(key_file) else os.path.join(current_dir, key_file)
        )

        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            with open(self.key_file, "wb") as f:
                f.write(self.key)

        self.fernet = Fernet(self.key)

    def save_game(self, game_state: GameState) -> tuple[str, str]:
        """
        Save game data to an encrypted file

        Args:
            game_state (GameState): Current game state
        """
        os.makedirs(os.path.dirname(self.save_file), exist_ok=True)

        # Convert GameState to dictionary using dataclass's asdict
        json_data = json.dumps(asdict(game_state))
        encrypted_data = self.fernet.encrypt(json_data.encode())

        with open(self.save_file, "wb") as f:
            f.write(encrypted_data)

        # Return save and key file paths
        return self.save_file, self.key_file

    def load_game(self) -> GameState | None:
        """
        Load game data from encrypted file

        Returns:
            Optional[GameState]: Loaded game state or None if file doesn't exist
        """
        if not os.path.exists(self.save_file):
            return None

        with open(self.save_file, "rb") as f:
            encrypted_data = f.read()

        json_data = self.fernet.decrypt(encrypted_data).decode()
        data_dict = json.loads(json_data)
        return GameState.from_dict(data_dict)
