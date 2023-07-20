import renpy # type: ignore
from .option_ren import SCOption, SC_OPTION_TYPE_BOOLEAN

"""renpy
init -1 python:
"""

class SCBooleanOption(SCOption):
    """
    Represents a toggleable option that can be represented by boolean flag.

    This option is intended to be updated by a toggle switch or checkbox of some
    kind.

    ```python
    SCBooleanOption("my_option", "My Option", "My Group", False, ("Hello", "Goodbye"))
    ```

    **IMPORTANT**: This option type is state dependent and cannot be used on its
    own, it **MUST** be registered to an SCLayer instance to be in any way
    useful.

    Internal Properties
    -------------------

    _default : bool
        The default value to return when no selection has yet been made by the
        user.

    _value : bool
        Boolean indicator for the state of the option.

    _when_true : any
        The selection value to set when this option is `True`.

    _when_false : any
        The selection value to set when this option is `False`.
    """

    def __init__(
        self,
        key: str,
        name: str,
        group: str,
        default: bool = False,
        values: tuple[any, any] | None = None,
        **kwargs
    ):
        """
        Initializes the new SCBooleanOption instance with the given arguments.

        Arguments
        ---------
        key : str
            Key for this option.

        name : str
            Display name for this option.

        group : str
            Group name for this option.

        default : bool, optional
            Optional default value to use when no selection has yet been made by
            the user.  Defaults to `False`.

        values : tuple, optional
            Optional tuple of actual values to use for user selections made by
            this option.  The given tuple *MUST* be a two-tuple where the first
            value is the selection when this option is `True` and the second
            value is the selection when this option is `False`.  Defaults to
            `(True, False)`.
        """
        super().__init__(key, name, group, SC_OPTION_TYPE_BOOLEAN, **kwargs)

        if not isinstance(default, bool):
            raise Exception('"default" must be a boolean value')

        if values != None:
            if (not isinstance(values, tuple)) or len(values) != 2:
                raise Exception('"values" must be a two-tuple')
            self._when_true = values[0]
            self._when_false = values[1]
        else:
            self._when_true = True
            self._when_false = False

        self._default = default

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Properties
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @property
    def value(self) -> bool:
        """
        bool
            The current boolean value of this SCBooleanOption.
        """
        return self.selection_value == self._when_true

    @property
    def selection_value(self) -> any:
        """
        any
            The current selection value for this SCBooleanOption.
        """
        if not self._req_state().has_selection(self._key):
            self._state.set_selection(self._key, self._pick_value(self._default))

        return self._state.get_selection(self._key)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   SC-Internal Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _clone(self):
        return SCBooleanOption(
            self._key,
            self._name,
            self._group,
            self._default,
            (self._when_true, self._when_false),
        )

    def _pick_value(self, tf: bool) -> any:
        return self._when_true if tf else self._when_false

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Public Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def set_selection(self, value: bool):
        """
        Sets the selection based on the given boolean `value`.  The selection
        will be set to one of the values provided in the `values` tuple in the
        constructor (or `True`/`False` if not values were set.)

        Arguments
        ---------
        value : bool
            Boolean value indicating the selection to set.
        """
        if not isinstance(value, bool):
            raise Exception('"value" must be a boolean value')

        self._req_state().set_selection(self._key, self._pick_value(value))

    def toggle(self):
        """
        Toggles the state of this SCBooleanOption.  This means if the value was
        `True` before calling this method, it will be `False` after calling this
        method and vice versa.
        """
        self.set_selection(not self.value)

    def randomize(self):
        """
        Selects a "random" option from either `True` or `False` and sets the
        user selection accordingly.
        """
        if renpy.random.randint(1, 2) == 1:
            self.set_selection(True)
        else:
            self.set_selection(False)
