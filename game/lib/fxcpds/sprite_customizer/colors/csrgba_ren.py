from .csrgb_ren import CSRGB
from ..utils.hex_color_ren import _parse_hex, _ubyte_to_hex

"""renpy
init python:
"""


class CSRGBA(CSRGB):

    def __init__(self, red: int, green: int, blue: int, alpha: int | float):
        super().__init__(red, green, blue)

        self._a = CSRGBA._require_alpha(alpha)

    ############################################################################
    #
    #   Properties
    #
    ############################################################################

    @property
    def hex_string(self):
        return (
            '#' +
            _ubyte_to_hex(self._r) +
            _ubyte_to_hex(self._g) +
            _ubyte_to_hex(self._b) +
            _ubyte_to_hex(self._a)
        )

    @property
    def alpha(self) -> int:
        return self._r

    ############################################################################
    #
    #   Static Methods
    #
    ############################################################################

    @staticmethod
    def _require_alpha(a: int | float) -> int:
        if isinstance(a, int):
            if not (0 <= a <= 255):
                raise Exception('alpha must be between 0 and 255 (inclusive)')
            return a
        elif isinstance(a, float):
            if not (0.0 <= a <= 1.0):
                raise Exception('alpha must be between 0.0 and 1.0 (inclusive)')
            return int(a * 255)
        else:
            raise Exception('alpha must be an int or a float')

    ############################################################################
    #
    #   Public Methods
    #
    ############################################################################

    def to_rgb(self) -> CSRGB:
        return CSRGB(self._r, self._g, self._b)

    def set_alpha(self, alpha: int | float):
        self._a = CSRGBA._require_alpha(alpha)

def hex_to_csrgba(hex: str) -> CSRGBA:
    l = len(hex)

    if not (l == 5 or l == 9):
        raise Exception("invalid rgba hex string (are you sure you included an alpha channel?): {}".format(hex))

    return _parse_hex(hex)