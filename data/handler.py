import json

from .exceptions import GameFileError, ScriptError

def get_scene(name: str, script: dict):
    try:
        scene = script[name]
    except KeyError:
        raise ScriptError(f"Couldn't get the scene: {name}")
    return scene


def load_script() -> dict:
    try:
        with open("data/game.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, IOError):
        raise GameFileError("Corrupted or missing game files.")


def load_map() -> dict:
    try:
        with open("data/map.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, IOError):
        raise GameFileError("Corrupted or missing game files.")
