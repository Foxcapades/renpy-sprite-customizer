import renpy # type: ignore
from renpy.store import DynamicDisplayable, Solid # type: ignore

from .option_ren import SCOption, SC_OPTION_TYPE_COLOR
from ..colors.cshsl_ren import CSHSL
from ..colors.csrgb_ren import CSRGB
from ..utils.hex_color_ren import _validate_hex


"""renpy
init -1 python:
"""


class SCColorOption(SCOption):
    def __init__(
        self,
        key: str,
        name: str,
        group: str,
        default: str | CSHSL | CSRGB,
    ):
        from uuid import uuid4
        super().__init__(key, name, group, SC_OPTION_TYPE_COLOR)

        if isinstance(default, str):
            _validate_hex(default)
            self._default = default
        elif isinstance(default, CSHSL):
            self._default = default.to_rgb().hex_string
        elif isinstance(default, CSRGB):
            self._default = default.hex_string
        else:
            raise Exception('"default" must be a string, a CSHSL instance, or a CSRGB instance')

        self._image_name = str(uuid4())

    @property
    def preview_image_name(self):
        return self._image_name

    @property
    def selection_value(self) -> str:
        if not self._req_state().has_selection(self._key):
            self._state.set_selection(self._key, self._default)

        return self._state.get_selection(self._key)

    def _clone(self):
        return SCColorOption(self._key, self._name, self._group, self._default)

    def _post_clone(self):
        renpy.image(self._image_name, DynamicDisplayable(self._color_cb))

    def _color_cb(self, st, at):
        return (Solid(self.selection_value), 0.0)

    def set_selection(self, value: str):
        if not isinstance(value, str):
            raise Exception('"value" must be a hex string')

        _validate_hex(value)
        self._req_state().set_selection(self._key, value)

    def randomize(self):
        self.set_selection(CSRGB(
            renpy.random.randint(0, 255),
            renpy.random.randint(0, 255),
            renpy.random.randint(0, 255),
        ).hex_string)
