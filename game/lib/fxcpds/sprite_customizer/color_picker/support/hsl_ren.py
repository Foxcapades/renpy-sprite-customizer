import renpy # type: ignore
from renpy.store import InputValue # type: ignore

from ...utils.hex_color_ren import _parse_hex
from ...options.color_option_ren import SCColorOption


"""renpy
init python:
"""


class HSLPicker:
    """
    Wrapper fo an `SCColorOption` instance that provides methods for changing
    the state of the option via controls for HSL channels.
    """

    def __init__(self, option: SCColorOption):
        """
        Initializes the new HSLPicker with the given option.

        Arguments
        ---------
        option : SCColorOption
            The color option that this picker will manipulate.
        """
        if not isinstance(option, SCColorOption):
            raise Exception('"option" must be an SCColorOption')

        self._option = option
        self._last   = option.selection_value
        self._hsl    = _parse_hex(self._last).to_hsl()

    @property
    def _hsl_hex(self) -> str:
        return self._hsl.to_rgb().hex_string

    @property
    def hue(self) -> int:
        """
        The current hue value.

        This value will be between `0` and `359` (inclusive).
        """
        self._course_correction()
        return self._hsl.hue

    @property
    def saturation(self) -> int:
        """
        The current saturation value.

        This value will be between `0` and `100` (inclusive).
        """
        self._course_correction()
        return int(self._hsl.saturation * 100)

    @property
    def lightness(self) -> int:
        """
        The current lightness value.

        This value will be between `0` and `100` (inclusive).
        """
        self._course_correction()
        return int(self._hsl.lightness * 100)

    @property
    def hex_string(self) -> str:
        """
        The hex string that represents the current color selection.
        """
        self._course_correction()
        return self._option.selection_value

    def _course_correction(self):
        sel = self._option.selection_value
        if sel != self._last:
            self._hsl = _parse_hex(sel).to_hsl()
            self._last = sel

    def _update_color(self):
        self._last = self._hsl.to_rgb().hex_string
        self._option.set_selection(self._last)
        renpy.restart_interaction()

    def set_hue(self, hue: int):
        if not (isinstance(hue, int) and 0 <= hue < 360):
            raise Exception("invalid hue value")
        self._hsl.set_hue(hue)
        self._update_color()

    def set_saturation(self, saturation: int):
        if not (isinstance(saturation, int) and 0 <= saturation <= 100):
            raise Exception("invalid saturation value")
        self._hsl.set_saturation(saturation / 100)
        self._update_color()

    def set_lightness(self, lightness: int):
        if not (isinstance(lightness, int) and 0 <= lightness <= 100):
            raise Exception("invalid lightness value")
        self._hsl.set_lightness(lightness / 100)
        self._update_color()
