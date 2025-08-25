import os
import sys
import textwrap
from random import random
from time import sleep

from data import Enemy, Player, get_scene, load_script
from data.exceptions import GameFileError
from player import save_game
from player.handler import load_game
from term import (
    Colors,
    Style,
    clear_acursor,
    clear_screen,
    display,
    move_cursor,
    stylize,
    typing_anim,
)


def render_status_line(player: Player, scene_name: str, enemy: Enemy | None):
    """Displays the status line (HUD)"""

    # i didn't know we could do this damn
    term_cols = os.get_terminal_size().columns

    hp_status = stylize(
        f"HP: {player.hp}/{player.max_hp}", Colors.BLACK_FG, Colors.GREEN_BG, Style.BOLD
    )
    damage_status = stylize(
        f"Attack: {player.damage}", Colors.BLACK_FG, Colors.YELLOW_BG, Style.ITALIC
    )
    item_status = stylize(
        f"Items: {','.join(player.inventory) if player.has_items() else 0}",
        Colors.WHITE_FG,
        Colors.BLUE_BG,
    )

    left_status = " ".join([hp_status, damage_status, item_status])
    center_status = scene_name
    right_status = ""

    right_count = 0
    if enemy and enemy.is_alive():
        enemy_hp_text = f"HP: {enemy.hp}/{enemy.max_hp}"
        enemy_damage_text = f"Attack: {enemy.damage}"

        enemy_hp = stylize(enemy_hp_text, Colors.BLACK_FG, Colors.RED_BG)
        enemy_damage = stylize(enemy_damage_text, Colors.BLACK_FG, Colors.MAGENTA_BG)

        right_status = " ".join([enemy_hp, enemy_damage])
        right_count = len(enemy_hp_text) + len(enemy_damage_text)

    center_pos = (term_cols - len(scene_name)) // 2
    right_pos = term_cols - right_count
    display(left_status, 2, 1)
    display(center_status, 2, center_pos)
    display(right_status, 2, right_pos)


def render_main_window(scene: dict, combat_log=None):
    """Display the main content i.e. scene description or the combat logs"""

    player_art = [" .---. ", "/ o o \\", "|   > |", " *___*"]
    enemy_art = [" ,o8888o. ", "888888888o", "`8888' `8'"]
    term_cols = os.get_terminal_size().columns
    line_num = 0

    if combat_log is not None:
        # Draw ASCII art
        for i, line in enumerate(player_art):
            display(line, 6 + i, 10)

        for i, line in enumerate(enemy_art):
            display(line, 6 + i, round(term_cols - len(max(enemy_art))) - 5)

        display(stylize("Combat:", style=Style.UNDERLINE), 12, 2)
        for i, log in enumerate(combat_log[-2:]):  # gives last 2 logs
            display(
                "- "
                + (
                    stylize(log, Colors.RED_FG, Colors.BLACK_BG)
                    if "attack" in log.lower() or "damage" in log.lower()
                    else stylize(log, Colors.BLUE_FG, Colors.BLACK_BG)
                ),
                13 + i,
                4,
            )
            line_num = 13 + i
    else:
        display(stylize("Description:", style=Style.UNDERLINE), 8, 2)
        wrapped_lines = textwrap.wrap(scene["description"], width=75)
        for i, line in enumerate(wrapped_lines):
            move_cursor(9 + i, 4)
            typing_anim(line)
            line_num = 9 + i
    return line_num


def render_options(line: int, scene: dict, player: Player, enemy: Enemy | None):
    """
    Displays all choices, styling them based on whether they are available.
    Returns a list of booleans indicating which choices are selectable.
    """
    display(stylize("Options:", style=Style.UNDERLINE), line + 4, 2)

    valid_opts = []
    line_num = 0

    if enemy and enemy.is_alive():
        combat_options = [{"text": "Attack"}, {"text": "Defend"}]
        for i, opt in enumerate(combat_options):
            combat_text = f"{i + 1}. {opt['text']}"
            display(stylize(combat_text, style=Style.BOLD), line + 4 + 1 + i, 4)
            line_num = line + 4 + 1 + i
        return combat_options, line_num

    if "options" in scene:
        for i, option in enumerate(scene["options"]):
            preq = option.get("prerequisites", {})
            # if player has all the prerequisites items
            has_items = all(item in player.inventory for item in preq.get("items", []))

            valid_opts.append(has_items)

            display_text = f"{i + 1}. {option['text']}"
            if has_items:
                styled_text = stylize(display_text, style=Style.BOLD)
            else:
                styled_text = stylize(display_text, style=Style.DIM)

                # Add the requirement text in red
                required_items = preq.get("items", [])
                if required_items:
                    req_text = f" (Requires: {', '.join(required_items)})"
                    styled_text += stylize(req_text, fg=Colors.RED_FG)
            move_cursor(line + 4 + 1 + i, 4)
            typing_anim(styled_text, 0.02)
            line_num = line + 4 + 1 + i
    return valid_opts, line_num


def get_player_action(line_num: int, num_ops: int):
    """Get valid input from the user"""
    SPECIAL_CMDS = ["save", "load", "quit", "inventory"]

    while True:
        # this will be error line
        move_cursor(line_num + 2, 0)
        clear_acursor()
        # input line
        move_cursor(line_num + 3, 0)

        user_input = input(f"? {Colors.MAGENTA_FG}").strip().lower()
        print(f"{Colors.DEFAULT_FG}", end="")

        if user_input in SPECIAL_CMDS:
            return user_input

        if user_input == "help":
            display(", ".join(SPECIAL_CMDS), line_num + 2, 0)
            move_cursor(line_num + 3, 0)
            input("Press any key to go back.")
            continue

        try:
            choice = int(user_input)
            if 1 <= choice <= num_ops:
                move_cursor(line_num + 3, 0)
                clear_acursor()
                return choice
            else:
                error_text = (
                    f"Wrong choice. Please enter a number between 1 and {num_ops}"
                )
                display(stylize(error_text, Colors.RED_FG), line_num + 2, 0)
                sys.stdout.flush()  # force the text to terminal
                sleep(2)
        except ValueError:
            error_text = (
                "Invalid command/choice. Type a number or a command like 'help'"
            )
            display(stylize(error_text, Colors.RED_FG), line_num + 2, 0)
            sys.stdout.flush()  # force the text to terminal
            sleep(2)


def update_game_state(player: Player, selected_opt: dict) -> str:
    """Updates the player's state based on their chosen option and returns the next scene name"""
    if "gives_item" in selected_opt:
        item = selected_opt["gives_item"]
        if item not in player.inventory:
            player.inventory.append(item)
    return selected_opt["next_scene"]


def handle_combat(player: Player, enemy: Enemy, player_action, combat_log):
    """
    Manages one full round of combat, checking both player and enemy health,
    and updates the combat log.
    """

    # player's action
    if player_action["text"].lower() == "attack":
        player.attack(enemy)
        combat_log.append(f"You attack the {enemy.name}.")
    elif player_action["text"].lower() == "defend":
        player.is_defending = True
        combat_log.append("You take a defensive stance.")

    if not enemy.is_alive():
        combat_log.append(f"You have defeated the {enemy.name}.")
        return 1  # victory

    enemy.action(player)

    if enemy.is_defending:
        combat_log.append(f"The {enemy.name} braces for an attack.")
    else:
        combat_log.append(f"The {enemy.name} attacks you.")

    if not player.is_alive():
        combat_log.append("Your systems fail... you have been defeated.")
        return 0  # defeat


def handle_command(
    action: str,
    player: Player,
    enemy: Enemy | None,
    scene_name: str,
    combat_log: list | None,
):
    if action == "quit":
        clear_screen()
        display(
            stylize(
                "Are you sure you want to quit?",
                fg=Colors.RED_FG,
                style=Style.BOLD,
            ),
            1,
            5,
        )
        move_cursor(3, 1)
        while True:
            try:
                uinput = input("Y / N >").lower()
                if uinput.lower() not in ["y", "n"]:
                    raise ValueError
                elif uinput.lower() == "y":
                    clear_screen()
                    display(
                        stylize(
                            "Thank you for playing Echoes of Nebula",
                            Colors.BLUE_FG,
                        ),
                        1,
                        1,
                    )
                    move_cursor(4, 0)
                    exit(0)
                else:
                    break
            except ValueError:
                move_cursor(2, 0)
                clear_acursor()
                display(
                    stylize("Wrong option.", Colors.RED_FG, Colors.BLACK_BG),
                    2,
                    1,
                )
                sys.stdout.flush()
                sleep(2)
                continue
        return 0
    elif action == "save":
        clear_screen()
        move_cursor(1, 1)
        typing_anim("Saving the game...")
        try:
            save_game(player, enemy, scene_name, combat_log)
            move_cursor(2, 1)
            typing_anim("Game has been saved!")
            sleep(2)

        except GameFileError as e:
            move_cursor(2, 1)
            typing_anim(stylize(str(e), Colors.RED_FG))
        return 0
    elif action == "load":
        clear_screen()
        move_cursor(1, 1)
        typing_anim("Loading the game...")
        try:
            game = load_game()
            move_cursor(2, 1)
            typing_anim("Successfully loaded saved game!")
            sleep(1)
            return game

        except GameFileError as e:
            move_cursor(2, 1)
            typing_anim(stylize(str(e), Colors.RED_FG))
    elif action == "map":
        pass
    elif action == "inventory":
        clear_screen()
        move_cursor(2, 1)
        typing_anim(
            stylize(f"You have {len(player.inventory)} items", style=Style.UNDERLINE)
        )
        if player.has_items():
            for i, itm in enumerate(player.inventory):
                move_cursor(3 + i, 1)
                typing_anim(f"- {itm}")
                sleep(2)
        return 0
    else:
        pass


def main():
    # initialize the variables
    player = Player(name="Ali", hp=40, max_hp=50, damage=12, inventory=[])
    game_script = load_script()
    scene_name = game_script["start_scene"]
    combat_log = []
    random_combat = []
    enemy = None

    # game loop
    while True:
        current_scene = get_scene(scene_name, game_script)

        if "combat" in current_scene:
            # 20% chance of triggering combat
            if random() < 0.2 and scene_name not in random_combat:
                scene_name = current_scene["combat"]
                random_combat.append(scene_name)
                continue

        if "enemy" in current_scene and not enemy:
            enemy_data = current_scene["enemy"]
            enemy = Enemy(
                name=enemy_data["name"],
                hp=enemy_data["hp"],
                max_hp=enemy_data["hp"],
                damage=enemy_data["damage"],
            )
            combat_log = [
                stylize(
                    f"A wild {enemy.name} appears!",
                    Colors.CYAN_FG,
                    Colors.BLACK_BG,
                    Style.BOLD,
                )
            ]

        display(stylize(""), 0, 0)  # set the default terminal colors
        clear_screen()
        render_status_line(player, scene_name.replace("_", " ").title(), enemy)
        line_num_mw = render_main_window(current_scene, combat_log if enemy else None)
        valid_opts, line_num_opt = render_options(
            line_num_mw, current_scene, player, enemy
        )
        player_action = get_player_action(line_num_opt, len(valid_opts))

        if type(player_action) is not int:
            # some command
            result = handle_command(
                player_action, player, enemy, scene_name, combat_log
            )
            if type(result) is int:
                continue  # re-render the game
            if type(result) is tuple:
                # loading a game
                player, enemy, scene_name, combat_log = result
                continue
            continue

        if enemy:
            choice = valid_opts[player_action - 1]
            combat_result = handle_combat(player, enemy, choice, combat_log)
            if combat_result == 1:
                scene_name = current_scene["on_victory"]
                enemy = None
                combat_log.clear()

        else:
            if not valid_opts[player_action - 1]:
                display(
                    stylize(
                        "You can't do that right now.",
                        fg=Colors.RED_FG,
                        style=Style.BOLD,
                    ),
                    line_num_opt + 2,
                    0,
                )
                sys.stdout.flush()
                sleep(2)
                continue
            choice = current_scene["options"][player_action - 1]
            scene_name = update_game_state(player, choice)

        if not player.is_alive():
            clear_screen()
            move_cursor(1, 1)
            typing_anim("You ded bro!")
            break

        if scene_name in ["end", "over"]:
            clear_screen()
            for i, part in enumerate(textwrap.wrap(current_scene["message"], 60)):
                move_cursor(1 + i, 1)
                typing_anim(part)
            break
    sleep(2)
    clear_screen()
    final_text = (
        stylize(
            "Thank " + stylize("you", Colors.GREEN_FG, style=Style.ITALIC),
            Colors.GREEN_FG,
        )
        + " for playing "
        + stylize("Echoes of Nebula", Colors.BLUE_FG, Colors.BLACK_BG, Style.BOLD)
    )
    move_cursor(4, round(os.get_terminal_size().columns / 2) - round(38 / 2))
    typing_anim(stylize(final_text, Colors.BLUE_FG))
    move_cursor(8, 0)
    sleep(2)
    exit(0)


if __name__ == "__main__":
    main()
