import renpy  # type: ignore
from renpy.store import InputValue  # type: ignore

from ...utils.hex_color_ren import _parse_hex
from ...options.color_option_ren import SCColorOption


"""renpy
init python:
"""


class RGBPicker:
    """
    Wrapper for an `SCColorOption` instance that provides methods for changing
    the state of the option via screen controls for RGB channels.
    """

    def __init__(self, option: SCColorOption):
        """
        Initializes the new RGBPicker with the given option.

        Arguments
        ---------
        option : SCColorOption
            The color option that this picker will manipulate.
        """
        if not isinstance(option, SCColorOption):
            raise Exception('"option" must be an SCColorOption')

        self._option = option
        self._last = option.selection_value
        self._rgb = _parse_hex(self._last)

    @property
    def red(self) -> int:
        """
        The current red channel value.

        This value will be between `0` and `255` (inclusive).
        """
        self._course_correction()
        return self._rgb.red

    @property
    def green(self) -> int:
        """
        The current green channel value.

        This value will be between `0` and `255` (inclusive).
        """
        self._course_correction()
        return self._rgb.green

    @property
    def blue(self) -> int:
        """
        The current blue channel value.

        This value will be between `0` and `255` (inclusive).
        """
        self._course_correction()
        return self._rgb.blue

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
            self._rgb = _parse_hex(sel)
            self._last = sel

    def _update_color(self):
        self._last = self._rgb.hex_string
        self._option.set_selection(self._last)
        renpy.restart_interaction()

    def set_red(self, red: int):
        """
        Sets the red channel to the given value.

        If the given value is not between `0` and `255` (inclusive) then this
        method will raise an exception.
        """
        if not (isinstance(red, int) and 0 <= red <= 255):
            raise Exception("invalid red value")
        self._rgb.set_red(red)
        self._update_color()

    def set_green(self, green: int):
        """
        Sets the green channel to the given value.

        If the given value is not between `0` and `255` (inclusive) then this
        method will raise an exception.
        """
        if not (isinstance(green, int) and 0 <= green <= 255):
            raise Exception("invalid green value")
        self._rgb.set_green(green)
        self._update_color()

    def set_blue(self, blue: int):
        """
        Sets the blue channel to the given value.

        If the given value is not between `0` and `255` (inclusive) then this
        method will raise an exception.
        """
        if not (isinstance(blue, int) and 0 <= blue <= 255):
            raise Exception("invalid blue value")
        self._rgb.set_blue(blue)
        self._update_color()
