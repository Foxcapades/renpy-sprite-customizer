from renpy.store import InputValue # type: ignore
import renpy # type: ignore

from ...utils.hex_color_ren import _validate_hex, _is_hex_digit
from ...options.color_option_ren import SCColorOption


"""renpy
init python:
"""


class HexInputValue(InputValue):
    def __init__(self, option: SCColorOption):
        self.default = False

        self._value = self._last = option.selection_value[1:]
        self._option = option

    def get_text(self) -> str:
        attr = self._option.selection_value[1:]
        if attr == self._last:
            return self._value
        else:
            self._last = self._value = attr
            return attr

    def set_text(self, text: str):
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
