from colorama import init

init()


def color_factory(color_code):
    def apply(text: str, format_spec=''):
        return f'{color_code}{text:{format_spec}}\x1b[0m'

    def mix(*colors):
        return [color_factory(c.color_code + color_code) for c in colors]

    apply.mix, apply.color_code = mix, color_code
    return apply


# colors
BLUE = color_factory('\x1b[94m')
GREEN = color_factory('\x1b[92m')
YELLOW = color_factory('\x1b[93m')
RED = color_factory('\x1b[91m')
MAGENTA = color_factory('\x1b[95m')
CYAN = color_factory('\x1b[96m')
ORANGE = color_factory('\x1b[38;5;208m')

# modifiers
BOLD = color_factory('\x1b[1m')
DIM = color_factory('\x1b[2m')
ITALIC = color_factory('\x1b[3m')
UNDERLINE = color_factory('\x1b[4m')

BLUE_BOLD, BLUE_DIM, BLUE_IT, BLUE_UNDER = BLUE.mix(BOLD, DIM, ITALIC, UNDERLINE)
GREEN_BOLD, GREEN_DIM, GREEN_IT, GREEN_UNDER = GREEN.mix(BOLD, DIM, ITALIC, UNDERLINE)
YELLOW_BOLD, YELLOW_DIM, YELLOW_IT, YELLOW_UNDER = YELLOW.mix(BOLD, DIM, ITALIC, UNDERLINE)
RED_BOLD, RED_DIM, RED_IT, RED_UNDER = RED.mix(BOLD, DIM, ITALIC, UNDERLINE)
MAGENTA_BOLD, MAGENTA_DIM, MAGENTA_IT, MAGENTA_UNDER = MAGENTA.mix(BOLD, DIM, ITALIC, UNDERLINE)
CYAN_BOLD, CYAN_DIM, CYAN_IT, CYAN_UNDER = CYAN.mix(BOLD, DIM, ITALIC, UNDERLINE)
ORANGE_BOLD, ORANGE_DIM, ORANGE_IT, ORANGE_UNDER = ORANGE.mix(BOLD, DIM, ITALIC, UNDERLINE)
