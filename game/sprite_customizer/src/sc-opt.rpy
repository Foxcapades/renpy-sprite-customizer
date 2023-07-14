init -1 python:
    class SCOpt:
        """
        # Sprite Customizer Option Set

        Represents an option set for a `CustomizedSprite` layer, providing
        options for customizing that layer and the display name for those
        options.
        """
        def __init__(self, display_name, option_values):
            """
            Initializes a new SCOpt object.

            Arguments:

            display_name (str): Display name for the set of options.

            option_values (list): List of option values.
            """
            if not isinstance(display_name, str):
                raise Exception("SCOpt display_name argument must be a string.")

            if not (isinstance(option_values, list) or isinstance(option_values, set)):
                raise Exception("SCOpt option_values argument must be a list.")

            if len(option_values) < 1:
                raise Exception("Cannot construct an SCOpt instance with no option values.")

            self._display_name = display_name
            self._values = option_values

        @property
        def display_name(self):
            return self._display_name

        @property
        def values(self):
            return [ *self._values ]

        @property
        def size(self):
            return len(self._values)