import json
from dataclasses import asdict

from data import GameFileError, Player
from data.models import Enemy


class EntityJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player):
            return asdict(obj)
        return super().default(self, obj)


def save_game(
    player: Player, enemy: Enemy | None, scene_name: str, combat_log: list | None
):
    try:
        with open("data/state.json", "w") as file:
            player_json = json.dumps(player, cls=EntityJsonEncoder)
            if enemy is not None:
                enemy_json = json.dumps(enemy, cls=EntityJsonEncoder)
            json.dump(
                {
                    "player": player_json,
                    "enemy": None if enemy is None else enemy_json,
                    "scene_name": scene_name,
                    "combat_log": [] if not combat_log else combat_log,
                },
                file,
            )
    except (FileNotFoundError, IOError):
        raise GameFileError("Could not save game state")


def load_game():
    try:
        with open("data/state.json", "r") as file:
            data = json.load(file)
            player = Player(**json.loads(data["player"]))
            enemy = data["enemy"] if data["enemy"] is None else Enemy(**data["enemy"])
            scene_name = data["scene_name"]
            combat_log = data["combat_log"]
            return player, enemy, scene_name, combat_log
    except FileNotFoundError:
        raise GameFileError("No save file found.")

    except (json.JSONDecodeError, TypeError) as e:
        print(e)
        raise GameFileError("Could not load save file. It may be corrupted")
