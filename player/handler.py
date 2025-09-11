import json
from dataclasses import asdict

from data import Enemy, GameFileError, Player

# nothing too complex here,
# json allows us to convert dict to str and vice-versa
# here we want to change from class to str/dict maybe?

# this just converts the class to dict at first, thnx to magic of dataclass: `asdict`
# and tells json module to use it
# tldr; tells json how to serialize or deserialize our Entity classes to dict/str


class EntityJsonEncoder(json.JSONEncoder):
    def default(self, o):
        # as explained above, player/enemy dataclass converts to dict and is used
        if isinstance(o, Player):
            return asdict(o)
        # incase its not Player/Enemy class, we call the super (parent) class's default method
        return super().default(o)


def save_game(
    player: Player, enemy: Enemy | None, scene_name: str, combat_log: list | None
):
    """Saves the game to a json file in data"""
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
    """Load the save file from data"""
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
