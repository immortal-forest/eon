import sys
import time

from .colors import Colors, Style
from .sequences import Sequences


def _print(*arg):
    print(*arg, end="")


def clear_screen():
    """Clear the entire screen"""
    _print(Sequences.CLR_ESCREEN)


def clear_bcursor():
    """Clear the screen before the cursor"""
    _print(Sequences.CLR_BCURSOR)


def clear_acursor():
    """Clear the screen after the cursor"""
    _print(Sequences.CLR_ACURSOR)


def clear_line():
    """Clear the current line"""
    _print(Sequences.CLR_LINE)


def move_cursor(line: int, column: int):
    """Move the cursor to line x column"""
    _print(Sequences.POS.format(line=line, column=column))
    _print(Sequences.SAVE)


def line(n: int, up=False):
    """Move to `n` line up/down"""
    if up:
        _print(Sequences.UP.format(line=n))
    else:
        _print(Sequences.DOWN.format(line=n))
    _print(Sequences.SAVE)


def column(n: int, right=False):
    """Move to `n` column right/left"""
    if right:
        _print(Sequences.RIGHT.format(column=n))
    else:
        _print(Sequences.LEFT.format(column=n))
    _print(Sequences.SAVE)


def display(text: str, line: int, column: int):
    """Prints text at line x column"""
    _print(Sequences.SAVE)
    _print(Sequences.POS.format(line=line, column=column))
    _print(text)
    _print(Sequences.RESTORE)


def typing_anim(text: str, delay: float = 0.03):
    """Creates a typing animation effect. Use `delay` to set time between each character output"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # force it to diplay the char immediately
        time.sleep(delay)


def stylize(
    text: str,
    fg: str = Colors.DEFAULT_FG,
    bg: str = Colors.DEFAULT_BG,
    style: str = Style.RESET,
) -> str:
    """Returns stylized ANSI string."""
    return f"{style}{fg}{bg}{text}{Colors.DEFAULT_FG}{Colors.DEFAULT_BG}{Style.RESET}"
