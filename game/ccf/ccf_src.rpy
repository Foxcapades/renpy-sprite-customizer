init -1 python:

    class CCState:
        """
        # Customized Character State

        This class defines an object that is used to hold character
        customization option selections.  This is used to persist the selected
        options as part of the game saves and reload those selections when
        loading the game from a save.
        """
        def __init__(self):
            """
            Constructs an empty state block.
            """
            self._state = {}

        def __getitem__(self, key):
            """
            Looks up a selection value, defaulting to option `1` if no such
            selection has ever been made before.

            Arguments:
            key (str): Selection key.

            Returns:
            int: Current state for the given option selection.
            """
            if not key in self._state:
                self._state[key] = 1

            return self._state[key]

        def __setitem__(self, key, value):
            """
            Override dict access setter to disable it.
            """
            raise Exception("Unsupported operation.")

        def inc_option(self, key, max):
            """
            Increment the selection value for the given option to a maximum of
            `max`, rolling back over to `1` if it would exceed that maximum.

            Arguments:

            key (str): Key of the selection option whose value should be
            incremented.

            max (int): Max value the selection option can possibly be.
            """
            if not key in self._state:
                self._state[key] = 2
            elif self._state[key] >= max:
                self._state[key] = 1
            else:
                self._state[key] += 1

        def dec_option(self, key, max):
            """
            Decrement the selection value for the given option to a minimum of
            `1`, rolling over to `max` if it would go below `1`.

            Arguments:

            key (str): Key of the selection option whose value should be
            decremented.

            max (int): Max value the selection option can possibly be.
            """
            if not key in self._state:
                self._state[key] = max
            elif self._state[key] == 1:
                self._state[key] = max
            else:
                self._state[key] -= 1

        def option_text(self, key):
            """
            Returns the displayable text for the value of the selection for the
            given option key.

            Arguments:

            key (str): Key of the selection option whose value should be
            rendered as a string and returned.

            Returns:

            str: String representation of the selection option for `key`.
            """
            return str(self[key]).rjust(2, '0')


    class CCOpt:
        def __init__(self, display_name, option_values):
            self.display_name = display_name
            self.values = option_values

        def len(self):
            return len(self.values)


    class CCLayer:
        def __init__(self, name, frame_constructor, **options):
            for key, opt in options.items():
                if not isinstance(opt, CCOpt):
                    raise Exception("CCLayer options must be CCOpt instances.")

            self._name  = name
            self._func  = frame_constructor
            self._state = None
            self.options = options

        def _require_option(self, option):
            if option not in self.options:
                raise Exception("Unrecognized CCLayer option \"{}\"".format(option))

        def _render(self, st, at, **kwargs):
            for key in self.options.keys():
                kwargs[key] = self.options[key].values[self._state[key] - 1]

            return (self._func(**kwargs), 0)

        def _copy(self):
            return CCLayer(self._name, self._func, **self.options)

        def set_state(self, state):
            self._state = state

        def inc_option(self, option):
            self._require_option(option)
            self._state.inc_option(option, len(self.options[option].values))

        def dec_option(self, option):
            self._require_option(option)
            self._state.dec_option(option, len(self.options[option].values))

        def option_display_text(self, option):
            self._require_option(option)
            return self.options[option].display_name

        def option_value_text(self, option):
            self._require_option(option)
            return self._state.option_text(option)

        def build_image(self):
            return DynamicDisplayable(self._render)

        def build_attribute(self):
            return Attribute(None, self._name, image=self.build_image(), default=True)


    class CustomizedCharacter:
        def __init__(self, image_name, *layers):
            self._layers = layers
            self._state  = CCState()

            self._option_to_layer = {}

            if len(layers) == 0:
                raise Exception("CustomizedCharacter needs at least one layer to display!")

            # Verify that the given option names are unique.
            for layer in layers:
                if not isinstance(layer, CCLayer):
                    raise Exception("CustomizedCharacter arguments 1+ must all be CCLayer instances.")

                for option_name, option in layer.options.items():
                    if option_name in self._option_to_layer:
                        raise Exception("Duplicate option \"{}\"".format(option_name))
                    self._option_to_layer[option_name] = layer
                layer.set_state(self._state)

            # Build the layered image

            attrs = [ layers[0].build_image() ]

            for i in range(1, len(layers)):
                attrs.append(layers[i].build_attribute())

            renpy.image(image_name, LayeredImage(attrs))

        def _require_option(self, option):
            if not option in self._option_to_layer:
                raise Exception("Unrecognized CustomizedCharacter option \"{}\"".format(option))

        def reset(self):
            self.set_state(CCState())

        def set_state(self, state):
            self._state = state
            for layer in self._layers:
                layer.set_state(state)

        def inc_option(self, option):
            self._require_option(option)
            self._option_to_layer[option].inc_option(option)

        def dec_option(self, option):
            self._require_option(option)
            self._option_to_layer[option].dec_option(option)

        def option_display_text(self, option):
            self._require_option(option)
            return self._option_to_layer[option].option_display_text(option)

        def option_value_text(self, option):
            self._require_option(option)
            return self._option_to_layer[option].option_value_text(option)

        @property
        def option_count(self):
            return len(self._option_to_layer.keys())

        @property
        def menu_components(self):
            """
            Builds a map of option display names to the actual option keys to be
            used when generating a menu screen.
            """
            out = {}
            for layer in self._layers:
                for opt in layer.options.keys():
                    out[layer.option_display_text(opt)] = opt
            return out


    class CustomizedCharacterFactory:
        def __init__(self, *layers):
            if len(layers) == 0:
                raise Exception("CustomizedCharacterFactory needs at least one layer to display!")

            for layer in layers:
                if not isinstance(layer, CCLayer):
                    raise Exception("CustomizedCharacterFactory parameters must all be CCLayer instances.")

            self._layers = layers

        def customized_character(self, image_name):
            return CustomizedCharacter(image_name, *[ layer._copy() for layer in self._layers ])