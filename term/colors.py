class Colors:
    """ANSI sequence for coloring text"""

    BLACK_FG = "\x1b[30m"
    BLACK_BG = "\x1b[40m"
    RED_FG = "\x1b[31m"
    RED_BG = "\x1b[41m"
    GREEN_FG = "\x1b[32m"
    GREEN_BG = "\x1b[42m"
    YELLOW_FG = "\x1b[33m"
    YELLOW_BG = "\x1b[43m"
    BLUE_FG = "\x1b[34m"
    BLUE_BG = "\x1b[44m"
    MAGENTA_FG = "\x1b[35m"
    MAGENTA_BG = "\x1b[45m"
    CYAN_FG = "\x1b[36m"
    CYAN_BG = "\x1b[46m"
    WHITE_FG = "\x1b[37m"
    WHITE_BG = "\x1b[47m"
    DEFAULT_FG = "\x1b[39m"
    DEFAULT_BG = "\x1b[49m"


class Style:
    """ANSI sequence for styling text"""

    BOLD = "\x1b[1m"
    DIM = "\x1b[2m"
    ITALIC = "\x1b[3m"
    UNDERLINE = "\x1b[4m"
    BLINKING = "\x1b[5m"
    RESET = "\x1b[0m"
