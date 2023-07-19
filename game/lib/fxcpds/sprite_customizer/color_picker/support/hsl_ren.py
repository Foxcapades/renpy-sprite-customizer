import renpy # type: ignore
from renpy.store import InputValue # type: ignore

from ...utils.hex_color_ren import _parse_hex
from ...options.color_option_ren import SCColorOption


"""renpy
init python:
"""


class HSLPicker:
    def __init__(self, option: SCColorOption):
        if not isinstance(option, SCColorOption):
            raise Exception(f'"option" must be an SCColorOption')

        self._option = option
        self._last   = option.selection_value
        self._hsl    = _parse_hex(self._last).to_hsl()

    @property
    def _hsl_hex(self):
        return self._hsl.to_rgb().hex_string

    @property
    def hue(self) -> int:
        self._course_correction()
        return self._hsl.hue

    @property
    def saturation(self) -> int:
        self._course_correction()
        return self._hsl.saturation * 100

    @property
    def lightness(self) -> int:
        self._course_correction()
        return self._hsl.lightness * 100

    @property
    def hex_string(self) -> str:
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
        if not (0 <= hue < 360):
            raise Exception("invalid hue value")
        self._hsl.set_hue(hue)
        self._update_color()

    def set_saturation(self, saturation: int):
        if not (0 <= saturation <= 100):
            raise Exception("invalid saturation value")
        self._hsl.set_saturation(saturation / 100)
        self._update_color()

    def set_lightness(self, lightness: int):
        if not (0 <= lightness <= 100):
            raise Exception("invalid lightness value")
        self._hsl.set_lightness(lightness / 100)
        self._update_color()
