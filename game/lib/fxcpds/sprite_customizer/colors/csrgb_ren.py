from ..utils.hex_color_ren import _parse_hex, _ubyte_to_hex
from .cshsl_ren import CSHSL
from .csrgba_ren import CSRGBA


"""renpy
init python:
"""


class CSRGB:
    def __init__(self, red: int, green: int, blue: int):
        CSRGB._validate_component('red', red)
        CSRGB._validate_component('green', green)
        CSRGB._validate_component('blue', blue)

        self._r = red
        self._g = green
        self._b = blue

    def __str__(self) -> str:
        return f'rgb({self._r}, {self._g}, {self._b})'

    ############################################################################
    #
    #   Properties
    #
    ############################################################################

    @property
    def red(self) -> int:
        return self._r

    @property
    def green(self) -> int:
        return self._g

    @property
    def blue(self) -> int:
        return self._b

    @property
    def hex_string(self) -> str:
        return ('#' + _ubyte_to_hex(self._r) + _ubyte_to_hex(self._g) + _ubyte_to_hex(self._b))

    ############################################################################
    #
    #   Static Methods
    #
    ############################################################################

    @staticmethod
    def _validate_component(key: str, value: int):
        if not (0 <= value <= 255):
            raise Exception(f'{key} value was out of bounds, must be between 0 and 255 (inclusive)')

    ############################################################################
    #
    #   Public Methods
    #
    ############################################################################

    def set_red(self, red: int):
        CSRGB._validate_component('red', red)
        self._r = red

    def set_green(self, green: int):
        CSRGB._validate_component('green', green)
        self._g = green

    def set_blue(self, blue: int):
        CSRGB._validate_component('blue', blue)
        self._b = blue

    def to_hsl(self) -> CSHSL:
        r = self._r / 255
        g = self._g / 255
        b = self._b / 255

        a = max(r, g, b)
        i = min(r, g, b)

        l = (a + i) / 2
        d = a - i

        s = 0.0
        if d != 0:
            s = d / (1 - abs(2 * l - 1))

        h = 0.0
        if d > 0:
            if a == r:
                h = ((g - b) / d) % 6
            elif a == g:
                h = 2 + (b - r) / d
            elif a == b:
                h = 4 + (r - g) / d
            else:
                raise Exception("illegal state")
        h *= 60

        return CSHSL(int(round(h)), s, l)

    def to_rgba(self, alpha: int | float) -> CSRGBA:
        return CSRGBA(self._r, self._g, self._b, alpha)


def hex_to_csrgb(hex: str) -> CSRGB:
    return _parse_hex(hex)
