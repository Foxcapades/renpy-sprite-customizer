import renpy # type: ignore

from .option_ren import SCOption, SC_OPTION_TYPE_VALUE_LIST

"""renpy
init -1 python:
"""

class SCListOption(SCOption):
    """
    Represents an option group that is a list or set of option choices that
    are navigated via an index that can be incremented or decremented.

    ```python
    SCListOption("my_option", "My Option", "My Group", [ "some", "choices" ])
    ```

    **IMPORTANT**: This option type is state dependent and cannot be used on its
    own, it **MUST** be registered to an SCLayer instance to be in any way
    useful.
    """

    def __init__(
        self,
        key: str,
        name: str,
        group: str,
        values: list[any] | set[any],
        display_digits: int = 2,
        **kwargs
    ):
        """
        Initializes the new SCListOption instance with the given
        arguments.

        Arguments
        ---------

        key : str
            Key for this option.

        name : str
            Display name for this option.

        group : str
            Group name for this option.

        values : any[]
            List of values for this option.

        display_digits : int
            Number of digits to display when rendering the selection index
            as a string.  The index will be left padded with zeros to reach
            this digit count.  For example, given the `display_digits` value
            `3`, when rendering the first index as a string, the returned
            string would be "001".
        """
        SCOption.__init__(self, key, name, group, SC_OPTION_TYPE_VALUE_LIST, **kwargs)

        if not (isinstance(values, list) or isinstance(values, set)):
            raise Exception("\"values\" argument must be a list or a set")

        if len(values) < 1:
            raise Exception("\"values\" argument must contain at least one option value")

        if not isinstance(display_digits, int):
            raise Exception("\"display_digits\" argument must be an int value")

        if display_digits < 1:
            raise Exception("\"display_digits\" argument must be greater than or equal to 1")

        self._display_pattern = "{{0{}d}}".format(display_digits)

        self._values: list[any] = [ value for value in values ]


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Properties
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    @property
    def values(self) -> list[any]:
        """
        The list of values that are part of this option group.
        """
        return self._values.copy()

    @property
    def value_count(self) -> int:
        """
        The number of options in this option group.
        """
        return len(self._values)

    @property
    def selection_index(self) -> int:
        """
        Index of the current selection for this option group.
        """
        if self._req_state().has_selection(self._key):
            return self._state.get_selection(self._key)
        else:
            return 0

    @property
    def selection_value(self) -> any:
        """
        The currently selected value for this option group.
        """
        return self._values[self.selection_index]


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   SC-Internal Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def _clone(self):
        """
        Returns a copy of this SCListOption sans user state.

        Returns
        -------

        SCListOption
            A copy of the current SCListOption instance without any
            user state.
        """
        out = SCListOption(
            self._key,
            self._name,
            self._group,
            self._values
        )
        out._display_pattern = self._display_pattern
        return out


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Public Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def inc_selection(self):
        """
        Increments the selection index for this option group, "selecting"
        the next value in the option list.  If the selection is already on
        the last item in the option group it will "roll over" to the first
        option in the group when incremented.
        """
        next = self.selection_index + 1

        if next < self.value_count:
            self._state.set_selection(self._key, next)
        else:
            self._state.set_selection(self._key, 0)

    def dec_selection(self):
        """
        Decrements the selection index for this option group, "selecting"
        the previous value in the option list.  If the selection is already
        on the first item in the option group it will "roll over" to the
        last option in the group when decremented.
        """
        next = self.selection_index - 1

        if next < 0:
            self._state.set_selection(self._key, self.value_count - 1)
        else:
            self._state.set_selection(self._key, next)

    def randomize(self):
        """
        Selects a "random" option from this option group and records that
        selection in the user state.
        """
        self._state.set_selection(self._key, renpy.random.randint(0, self.value_count - 1))
