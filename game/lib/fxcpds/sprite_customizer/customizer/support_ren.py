import renpy  # type: ignore
from renpy import InputValue  # type: ignore

from ..options.text_option_ren import SCTextOption

"""renpy
init -1 python:
"""


class SCTextInput(InputValue):
    def __init__(self, option: SCTextOption):
        if not isinstance(option, SCTextOption):
            raise Exception("option must be an SCTextOption instance")

        self.default = False
        self._option = option

    def get_text(self) -> str:
        return self._option.current_value

    def set_text(self, text: str):
        self._option.set_value(text)
        renpy.restart_interaction()

    def enter(self):
        self._option.commit_to_selection()
        renpy.run(self.Disable())
        raise renpy.IgnoreEvent()
