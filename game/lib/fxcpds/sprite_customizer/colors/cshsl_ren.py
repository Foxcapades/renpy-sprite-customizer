from .csrgb_ren import CSRGB
from .cshsla_ren import CSHSLA


"""renpy
init python:
"""


class CSHSL:
    """
    HSL value container.

    Provides methods for storing and dealing with HSL values.
    """

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
        """
        The current hue value.
        """
        return self._h

    @property
    def saturation(self) -> float:
        """
        The current saturation value.
        """
        return self._s

    @property
    def lightness(self) -> float:
        """
        The current lightness value.
        """
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
            return tmp, tmp, tmp
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

        return r, g, b

    ############################################################################
    #
    #   Public Methods
    #
    ############################################################################

    def set_hue(self, hue: int):
        """
        Sets the hue value.

        The hue value will be corrected automatically, for example, if the value
        `360` is given, the actual value set will be `0`; if the value `-12` is
        set, the actual value set will be `348`

        If the given value is not an int, this method will raise an exception.

        Arguments
        ---------
        hue : int
            The new hue value to set.
        """
        if not isinstance(hue, int):
            raise Exception("'hue' must be an int value.")
        self._h = self._fix_hue(hue)

    def set_saturation(self, saturation: float):
        """
        Sets the saturation value.

        If the saturation value not a float value between `0.0` and `1.0`
        (inclusive) this method will raise an exception.
        """
        if not isinstance(saturation, float):
            raise Exception("'saturation' must be a float value")
        CSHSL._validate_percent('saturation', saturation)
        self._s = saturation

    def set_lightness(self, lightness: float):
        """
        Sets the lightness value.

        If the lightness value not a float value between `0.0` and `1.0`
        (inclusive) this method will raise an exception.
        """
        if not isinstance(lightness, float):
            raise Exception("'lightness' must be a float value")
        CSHSL._validate_percent('lightness', lightness)
        self._l = lightness

    def to_rgb(self) -> CSRGB:
        """
        Converts this HSL value to RGB and returns a new CSRGB instance.

        Returns
        -------
        CSRGB
            The converted CSRGB instance.
        """
        tmp = self._to_rgb()
        return CSRGB(tmp[0], tmp[1], tmp[2])

    def to_hsla(self, alpha: float) -> CSHSLA:
        """
        Converts this HSL value to an HSLA value by adding an alpha channel set
        to the given value.

        If the alpha value not a float value between `0.0` and `1.0` (inclusive)
        this method will raise an exception.

        Arguments
        ---------
        alpha : float
            The alpha value to set on the new CSHSLA instance.

        Returns
        -------
        CSHSLA
            A new CSHSLA instance with the same hue, saturation, and lightness
            values as this CSHSL instance in addition to the given alpha value.
            """
        if not isinstance(alpha, float):
            raise Exception("'alpha' must be a float value")
        CSHSL._validate_percent('a', alpha)
        return CSHSLA(self._h, self._s, self._l, alpha)

