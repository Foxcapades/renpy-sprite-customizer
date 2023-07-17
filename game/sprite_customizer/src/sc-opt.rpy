init -1 python:
    #
    # ENUM VALUES
    #
    SC_OPTION_TYPE_VALUE_LIST = 0

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


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #
        #   Properties
        #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


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


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #
        #   SC-Internal Methods
        #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


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


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #
        #   Public Methods
        #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        def randomize(self):
            """
            Extension point method for randomizable options to override and
            provide their own randomization logic.
            """
            pass


    class SCValueListOption(SCOption):
        """
        Represents an option group that is a list or set of option choices that
        are navigated via an index that can be incremented or decremented.

        ```python
        SCValueListOption("my_option", "My Option", "My Group", [ "some", "choices" ])
        ```

        **IMPORTANT**: This option type is state dependent and cannot be used on
        its own, it **MUST** be registered to an SCLayer instance to be in any
        way useful.
        """

        def __init__(self, key, name, group, values, display_digits=2, **kwargs):
            """
            Initializes the new SCValueListOption instance with the given
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

            self._values = [ value for value in values ]


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #
        # Properties
        #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


        @property
        def values(self):
            """
            The list of values that are part of this option group.
            """
            return self._values.copy()

        @property
        def value_count(self):
            """
            The number of options in this option group.
            """
            return len(self._values)

        @property
        def selection_index(self):
            """
            Index of the current selection for this option group.
            """
            if self._req_state().has_selection(self._key):
                return self._state.get_selection(self._key)
            else:
                return 0

        @property
        def selection_value(self):
            """
            The currently selected value for this option group.
            """
            return self._values[self.selection_index]


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #
        #   SC-Internal Methods
        #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


        def _clone(self):
            """
            Returns a copy of this SCValueListOption sans user state.

            Returns
            -------

            SCValueListOption
                A copy of the current SCValueListOption instance without any
                user state.
            """
            out = SCValueListOption(
                self._key,
                self._name,
                self._group,
                self._values
            )
            out._display_pattern = self._display_pattern
            return out


        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #
        # Public Methods
        #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


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
