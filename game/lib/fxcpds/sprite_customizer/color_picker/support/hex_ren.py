from renpy.store import InputValue  # type: ignore
import renpy  # type: ignore

from ...utils.hex_color_ren import _validate_hex, _is_hex_digit
from ...options.color_option_ren import SCColorOption

"""renpy
init python:
"""


class HexInputValue(InputValue):
    """
    Wrapper for an `SCColorOption` instance that provides a method for changing
    the state of the option via a screen control that provides a hex code
    string.
    """

    def __init__(self, option: SCColorOption):
        """
        Initializes the new HexInputValue with the given option.

        Arguments
        ---------
        option : SCColorOption
            The color option that this input value will manipulate.
        """
        self.default = False

        self._value = self._last = option.selection_value[1:]
        self._option = option

    def get_text(self) -> str:
        """
        The current hex or input value for this input.
        """
        attr = self._option.selection_value[1:]
        if attr == self._last:
            return self._value
        else:
            self._last = self._value = attr
            return attr

    def set_text(self, text: str):
        """
        Sets the input value to the given string.

        If the given value is not a string, this method will raise an exception.

        If the given value is not a valid hex string, the backing option will
        not be updated.

        If the given option contains a non-hex value the input will be rejected.
        """
        if not isinstance(text, str):
            raise Exception("invalid 'text' value")

        for c in text:
            if not _is_hex_digit(c):
                renpy.restart_interaction()
                return

        l = len(text)

        if l == 3 or l == 6:
            tmp = '#' + text
            try:
                _validate_hex(tmp)
                self._option.set_selection(tmp)
            except:
                pass
        self._value = text
        renpy.restart_interaction()
