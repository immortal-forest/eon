import json
from dataclasses import asdict

from data import GameFileError, Player


class PlayerJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player):
            return asdict(obj)
        return super().default(self, obj)


def save_game(player: Player):
    try:
        with open("player/state.json", "w") as file:
            json.dump(player, file, cls=PlayerJsonEncoder, indent=4)
    except (FileNotFoundError, IOError):
        raise GameFileError("Could not save game state")


def load_game():
    try:
        with open("player/state.json", "r") as file:
            data = json.load(file)
            return Player(**data)
    except FileNotFoundError:
        GameFileError("No save file found.")
        return None
    except (json.JSONDecodeError, TypeError):
        GameFileError("Could not load save file. It may be corrupted")
        return None
