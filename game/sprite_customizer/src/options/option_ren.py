"""renpy
init -2 python:
"""


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   Enum Values
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


SC_OPTION_TYPE_VALUE_LIST = 0
SC_OPTION_TYPE_TEXT_INPUT = 1
SC_OPTION_TYPE_BOOLEAN    = 2


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   Classes
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


class SCOption:
    """
    Base type for Sprite Customizer option types.
    """
    def __init__(self, key, name, group, option_type):
        if not isinstance(key, str):
            raise Exception("\"key\" argument must be a string")

        if not isinstance(name, str):
            raise Exception("\"name\" argument must be a string")

        if not isinstance(group, str):
            raise Exception("\"group\" argument must be a string")

        if not isinstance(option_type, int):
            raise Exception("\"option_type\" argument must be an int")

        self._key = key
        self._name = name
        self._group = group
        self._type = option_type
        self._state = None


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Properties
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    @property
    def key(self):
        """
        str : Option keyword.
        """
        return self._key

    @property
    def display_name(self):
        """
        str : Display name for the option.
        """
        return self._name

    @property
    def group(self):
        """
        str : Group display name for the option.
        """
        return self._group

    @property
    def option_type(self):
        """
        int : Option type indicator.
        """
        return self._type

    @property
    def selection_value(self):
        raise Exception("selection_value must be implemented by extending classes!")


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   SC-Internal Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def _set_state(self, state):
        self._state = state

    def _req_state(self):
        if self._state == None:
            raise Exception("CustomizedSprite state is not yet set!  Did you forget to call `set_state`?")

        return self._state

    def _clone(self):
        """
        Returns a copy of this SCOption sans state.
        """
        return SCOption(self._key, self._name, self._group, self._type)


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Public Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def randomize(self):
        """
        Extension point method for randomizable options to override and
        provide their own randomization logic.
        """
        pass
