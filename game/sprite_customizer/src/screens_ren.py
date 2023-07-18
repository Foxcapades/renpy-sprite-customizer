import renpy # type: ignore
from renpy import InputValue # type: ignore

from options.option_ren import SCTextOption

"""renpy
init -1 python:
"""

class SCTextInput(InputValue):
    def __init__(self, option):
        if not isinstance(option, SCTextOption):
            raise Exception("option must be an SCTextOption instance")

        self._option = option

    def get_text(self):
        return self._option.current_value

    def set_text(self, text):
        self._option.set_value(text)
        renpy.restart_interaction()

    def enter(self):
        self._option.commit_to_selection()
