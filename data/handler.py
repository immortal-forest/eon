import json

from .exceptions import GameFileError, ScriptError


def get_scene(name: str, script: dict):
    """Get `name` scene from the `script`"""
    try:
        scene = script[name]
    except KeyError:
        raise ScriptError(f"Couldn't get the scene: {name}")
    return scene


def load_script() -> dict:
    """Load the game script file"""
    try:
        with open("data/game.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, IOError):
        raise GameFileError("Corrupted or missing game files.")
