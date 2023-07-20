from .csrgb_ren import CSRGB
from .cshsla_ren import CSHSLA
from .csrgba_ren import CSRGBA


"""renpy
init python:
"""


class CSHSL:
    def __init__(self, hue: int, saturation: float, lightness: float):
        CSHSL._validate_percent('saturation', saturation)
        CSHSL._validate_percent('lightness', lightness)

        self._h = CSHSL._fix_hue(hue)
        self._s = saturation
        self._l = lightness

    def __str__(self) -> str:
        s = round(self._s, 2)
        l = round(self._l, 2)
        return f'hsl({self._h}, {s}, {l})'

    ############################################################################
    #
    #   Properties
    #
    ############################################################################

    @property
    def hue(self) -> int:
        return self._h

    @property
    def saturation(self) -> float:
        return self._s

    @property
    def lightness(self) -> float:
        return self._l

    ############################################################################
    #
    #   Static Methods
    #
    ############################################################################

    @staticmethod
    def _fix_hue(h: int):
        if h > 0:
            while h > 359:
                h -= 360
        else:
            while h < 0:
                h += 360

        return h

    @staticmethod
    def _validate_percent(key: str, value: float):
        if not (0.0 <= value <= 1.0):
            raise Exception(f'{key} must be a percent value between 0.0 and 1.0 (inclusive)')

    ############################################################################
    #
    #   Internal Methods
    #
    ############################################################################

    def _to_rgb(self):
        if self._s == 0:
            tmp = int(self._l * 255)
            return (tmp, tmp, tmp)
        else:
            c = (1 - abs(2 * self._l - 1)) * self._s
            x = c * (1 - abs(((self._h / 60) % 2) - 1))
            m = self._l - c/2

            r = 0.0
            g = 0.0
            b = 0.0

            if self._h < 60:
                r = c
                g = x
                b = 0
            elif self._h < 120:
                r = x
                g = c
                b = 0.0
            elif self._h < 180:
                r = 0.0
                g = c
                b = x
            elif self._h < 240:
                r = 0.0
                g = x
                b = c
            elif self._h < 300:
                r = x
                g = 0.0
                b = c
            elif self._h < 360:
                r = c
                g = 0.0
                b = x

            r = int((r + m) * 255)
            g = int((g + m) * 255)
            b = int((b + m) * 255)

        return (r, g, b)

    ############################################################################
    #
    #   Public Methods
    #
    ############################################################################

    def set_hue(self, hue: int):
        self._h = self._fix_hue(hue)

    def set_saturation(self, saturation: float):
        CSHSL._validate_percent('saturation', saturation)
        self._s = saturation

    def set_lightness(self, lightness: float):
        CSHSL._validate_percent('lightness', lightness)
        self._l = lightness

    def to_rgb(self) -> CSRGB:
        tmp = self._to_rgb()
        return CSRGB(tmp[0], tmp[1], tmp[2])

    def to_hsla(self, alpha: float) -> CSHSLA:
        CSHSL._validate_percent('a', alpha)
        return CSHSLA(self._h, self._s, self._l, alpha)

