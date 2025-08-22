class Sequences:
    """ANSI codes to control the position of cursor and clear the screen"""

    ESC = "\x1b"  # \e
    CR = "\x0d"  # \r move to start of line

    # Position
    HOME = "\x1b[H"  # move cursor home position
    POS = "\x1b[{line};{column}H"  # move to line and column
    UP = "\x1b[{line}A"  # move cursor up
    DOWN = "\x1b[{line}B"  # move cursor down
    RIGHT = "\x1b[{column}C"  # move cursor right
    LEFT = "\x1b[{column}D"  # move cursor left
    UP_S = "\x1b[{line}E"  # move cursor up at start
    DOWN_S = "\x1b[{line}F"  # move cursor down at start
    SAVE = "\x1b[s"  # save cursor position
    RESTORE = "\x1b[u"  # restore cursor position

    # Clear
    CLR_ESCREEN = "\x1b[2J"  # clears entire screen
    CLR_BCURSOR = "\x1b[1J"  # clear from cusror to start of screen
    CLR_ACURSOR = "\x1b[0J"  # clear from cursor to end of screen
    CLR_LINE = "\x1b[2K"  # clear entire line
