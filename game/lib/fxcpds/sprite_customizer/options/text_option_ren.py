from .option_ren import SCOption, SC_OPTION_TYPE_TEXT_INPUT

"""renpy
init -1 python:
"""

class SCTextOption(SCOption):
    """
    Represents an option that is a string value that may be set by the player.

    This option is intended to be updated by a text input, but may be updated by
    any source of a string value.

    ```python
    SCTextOption("my_option", "My Option", "My Group", "default value")
    ```

    **IMPORTANT**: This option type is state dependent and cannot be used on its
    own, it **MUST** be registered to an SCLayer instance to be in any way
    useful.
    """
    def __init__(
        self,
        key: str,
        name: str,
        group: str | None,
        default: str = "",
        prefix: str | None = None,
        suffix: str | None = None,
        max_len: int | None = None,
        **kwargs
    ):
        """
        Initializes the new SCTextOption instance with the given arguments.

        Arguments
        ---------
        key : str
            Key for this option.

        name : str
            Display name for this option.

        group : str | None
            Option group.  If this value is set to `None`, the `name` value will
            be used as the group name.

        default : str, optional
            Default/starting value to use when no value has yet been set.

        prefix : str, optional
            Static prefix that should appear before the value when rendering
            this option as an input.

        suffix : str, optional
            Static suffix that should appear after the value when rendering this
            option as an input.

        max_len : int, optional
            Maximum allowed length for the text value.

            **WARNING**: The max length is *NOT* enforced by this type, it must
            be enforced by the input when rendering this option.
        """
        super().__init__(key, name, group, SC_OPTION_TYPE_TEXT_INPUT, **kwargs)

        if not isinstance(default, str):
            raise Exception('"default" must be a string')

        if not (prefix == None or isinstance(prefix, str)):
            raise Exception('"prefix" must be a string')

        if not (suffix == None or isinstance(suffix, str)):
            raise Exception('"suffix" must be a string')

        if isinstance(max_len, int):
            if max_len < 0:
                raise Exception('"max_len" must be greater than or equal to zero')
        elif max_len != None:
            raise Exception('"max_len" must be an int value')

        self._default = default
        self._current = None
        self._prefix = prefix
        self._suffix = suffix
        self._max_len = max_len


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Properties
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    @property
    def default(self) -> str:
        """
        The default value set on this option.

        The default value is used as the value of this option when no value has
        yet been set.
        """
        return self._default

    @property
    def selection_value(self) -> str:
        """
        The current user selection value for this option.
        """
        if not self._req_state().has_selection(self._key):
            self._state.set_selection(self._key, self._default)

        return self._state.get_selection(self._key)

    @property
    def current_value(self) -> str:
        """
        The current value for this text input.  This is not the same as the
        selection value.  This value is used to track the text the user has set
        before they attempted to "commit" their change to an option selection.

        This is primarily used by screen inputs to store the value as it is
        being typed but before it is saved.
        """
        if self._current == None:
            self._current = self.selection_value

        return self._current

    @property
    def has_prefix(self) -> bool:
        """
        Whether this option has a prefix value set.
        """
        return self._prefix != None

    @property
    def prefix(self) -> str | None:
        """
        This option's prefix value.

        The prefix is a static value that should appear before the option text
        when rendering this option as an input.
        """
        return self._prefix

    @property
    def has_suffix(self) -> bool:
        """
        Whether this option has a suffix value set.
        """
        return self._suffix != None

    @property
    def suffix(self) -> str | None:
        """
        This option's suffix value.

        The suffix is a static value that should appear after the option text
        when rendering this option as an input.
        """
        return self._suffix

    @property
    def has_max_len(self) -> bool:
        """
        Whether this option has a max_len value set.
        """
        return self._max_len != None

    @property
    def max_len(self) -> int | None:
        """
        Max length.

        This value is to be used when rendering the current option as an input
        to prevent users from inputting a value that is too long.

        **WARNING**: The max length is *NOT* enforced automatically, it is only
        for use when rendering this option as an input.
        """
        return self._max_len


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   SC-Internal Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def _clone(self):
        return SCTextOption(
            self._key,
            self._name,
            self._group,
            self._default,
            self._prefix,
            self._suffix,
            self._max_len,
        )


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Public Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def commit_to_selection(self):
        """
        Commits the `current_value` of this option to the user selections.
        """
        self._req_state().set_selection(self._key, self._current)

    def set_value(self, value: str):
        """
        Sets the `current_value` of this option to the given value.

        Arguments
        ---------
        value : str
            New current value to set.
        """
        if not isinstance(value, str):
            raise Exception("value must be a string")

        self._current = value


class SCValidatableTextOption(SCTextOption):
    """
    Represents an option that is a string value that may be set by the player
    but must be valid according to a given validator function.

    This option is intended to be updated by a text input, but may be updated by
    any source of a string value.

    ```python
    SCValidatableTextOption("my_option", "My Option", "My Group", validator_func, "default value")
    ```

    **IMPORTANT**: This option type is state dependent and cannot be used on its
    own, it **MUST** be registered to an SCLayer instance to be in any way
    useful.
    """
    def __init__(
        self,
        key: str,
        name: str,
        group: str | None,
        validator: function,
        default: str = "",
        autocommit: bool = False,
        prefix: str | None = None,
        suffix: str | None = None,
        max_len: int | None = None,
        **kwargs
    ):
        """
        Initializes the new SCValidatableTextOptoin instance with the given
        arguments.

        Arguments
        ---------
        key : str
            Key for this option.

        name : str
            Display name for this option.

        group : str | None
            Option group.  If this value is set to `None`, the `name` value will
            be used as the group name.

        validator : callable
            A function that should take a string value as its single argument
            and return a boolean flag indicating whether the given value was
            valid.

            See `sc_validator_hex_color`.

        default : str, optional
            Default/starting value to use when no value has yet been set.

        autocommit : bool
            Whether the `current_value` should be automatically committed as
            soon as it is valid, without requiring a call to
            `commit_to_selection`.

        prefix : str, optional
            Static prefix that should appear before the value when rendering
            this option as an input.

        suffix : str, optional
            Static suffix that should appear after the value when rendering this
            option as an input.

        max_len : int, optional
            Maximum allowed length for the text value.

            **WARNING**: The max length is *NOT* enforced by this type, it must
            be enforced by the input when rendering this option.
        """
        super().__init__(key, name, group, default, prefix, suffix, max_len, **kwargs)

        if not callable(validator):
            raise Exception("validator must be callable")

        if not isinstance(autocommit, bool):
            raise Exception("autocommit must be a boolean value")

        self._validator = validator
        self._autocommit = autocommit


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Properties
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    @property
    def is_valid(self) -> bool:
        """
        Whether the `current_value` of this option is valid against the given
        validation function.
        """
        out = self._validator(self.current_value)

        if not isinstance(out, bool):
            raise Exception("SCValidatableTextOption validator returned a non-boolean value")

        return out


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   SC-Internal Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def _clone(self):
        return SCValidatableTextOption(
            self._key,
            self._name,
            self._group,
            self._validator,
            self._default,
            self._autocommit,
            self._prefix,
            self._suffix,
            self._max_len,
        )


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    # Public Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


    def commit_to_selection(self):
        """
        Commits the `current_value` of this option to the user selections only
        if the value is valid.
        """
        if self.is_valid:
            super().commit_to_selection()

    def set_value(self, value: str):
        """
        Sets the `current_value` of this option to the given value.

        Additionally, if `autocommit` is `True` and the given value is valid, it
        will be automatically committed to the user selections.

        Arguments
        ---------
        value : str
            New current value to set.
        """
        super().set_value(value)

        if self._autocommit and self.is_valid:
            super().commit_to_selection()

