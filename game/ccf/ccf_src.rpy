init -1 python:

    class SCState:
        """
        # Sprite Customizer State

        This class defines an object that is used to hold sprite customization
        option selections.  This is used to persist the selected options as part
        of the game saves and reload those selections when loading the game from
        a save.

        ```python
        my_sprite_state = SCState()
        my_sprite.set_state(my_sprite_state)
        ```
        """
        def __init__(self):
            """
            Constructs an empty state block.
            """
            self._state = {}

        def get_selection(self, key):
            """
            Looks up the target selection value.  If the target selection value
            is unknown to the `SCState` object, the value `1` will be recorded
            in the state and returned from this method.

            Arguments:

            key (str): Selection key.

            Returns:

            int: Current selection state for the given option selection.
            """
            if not key in self._state:
                self._state[key] = 1

            return self._state[key]

        def inc_selection(self, key, max):
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

        def dec_selection(self, key, max):
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


    class SCOpt:
        """
        Sprite Customizer Option Set

        Represents an option set for a `CustomizedSprite` layer, providing
        options for customizing that layer and the display name for those
        options.

        ...

        Attributes
        ----------

        display_name (str): Display name for the set of options.

        values (list): List of option values.

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

            self.display_name = display_name
            self.values = option_values


    class SCLayer:
        """
        # Sprite Customization Layer

        Represents a single layer in a customizable sprite.

        This layer has zero or more customization options provided at
        construction time via named `SCOpt` keyword args.  The user's selections
        of those options are then passed to the given `layer_callback` to
        construct the underlying Displayable for the layer.

        ```python
        SCLayer("name", callback, option=SCOpt("Option", [ "some", "choices" ]))
        ```
        """

        def __init__(self, name, layer_callback, **options):
            """
            Initializes the new `SCLayer` instance with the given arguments.

            Arguments:

            name (str): Name of the layer.

            layer_callback (function): Callback used to create the displayable
            that backs this layer.

            **options (dict): Dictionary of keyword arguments that define the
            options available to this layer.  Keyword args must all be `SCOpt`
            values.
            """

            if not isinstance(name, str):
                raise Exception("SCLayer name must be a string.")
            if not callable(layer_callback):
                raise Exception("SCLayer layer_callback must be callable.")
            for key, opt in options.items():
                if not isinstance(opt, SCOpt):
                    raise Exception("SCLayer options must be SCOpt instances.")

            self._name  = name
            self._func  = layer_callback
            self._state = None
            self._options = options

        def _require_option(self, option):
            if option not in self._options:
                raise Exception("Unrecognized SCLayer option \"{}\"".format(option))

        def _render(self, st, at, **kwargs):
            """
            Render Callback

            This callback is passed to the underlying `DynamicDisplayable` to
            render the layer's image.

            This method calls out to the configured `layer_callback` callback
            with the options selected in the SCState.

            Returns:

            tuple:  A tuple containing 2 values; the `Displayable` generated by
            the `layer_callback` callback passed to the `SCLayer` on
            construction, and an int representing the time to pause before
            rerendering.
            """
            for key in self._options.keys():
                kwargs[key] = self._options[key].values[self._state.get_selection(key) - 1]

            return (self._func(**kwargs), 0)

        def clone(self):
            """
            Creates a clone of this layer instance.

            Returns:

            SCLayer: A new `SCLayer` instance containing the same values
            configured on this instance.
            """
            return SCLayer(self._name, self._func, **self._options)

        def set_state(self, state):
            """
            Replaces the state of this `SCLayer` instance with the given
            `state` object.

            Arguments:

            state (SCState): New state object to back this layer's customization
            option selections.
            """
            if not isinstance(state, SCState):
                raise Exception("Cannot call set_state with a non SCState value.")
            self._state = state

        def inc_selection(self, option):
            """
            Increment Option Selection

            Increments the selection for the given option.

            Arguments:

            option str: Keyword for the option whose selection should be
            incremented.
            """
            self._require_option(option)
            self._state.inc_selection(option, len(self._options[option].values))

        def dec_selection(self, option):
            """
            Decrement Option Selection

            Decrements the selection for the given option.

            Arguments:

            option str: Keyword for the option whose selection should be
            decremented.
            """
            self._require_option(option)
            self._state.dec_selection(option, len(self._options[option].values))

        def get_option(self, option):
            self._require_option(option)
            return self._options[option]

        def get_option_value(self, option, selection):
            self._require_option(option)
            return self._options[option].values[selection - 1]

        def option_display_name(self, option):
            self._require_option(option)
            return self._options[option].display_name

        def option_selection(self, option):
            self._require_option(option)
            return self._state.get_selection(option)

        def build_image(self):
            """
            Build Image

            Builds the DynamicDisplayable that represents this `SCLayer`
            instance.

            Returns:

            DynamicDisplayable: The DynamicDisplayable that represents this
            `SCLayer` instance.
            """
            return DynamicDisplayable(self._render)

        def build_attribute(self):
            """
            Build Attribute

            Builds a LayeredImage Attribute instance to represent this `SCLayer`
            instance.

            Returns:

            Attribute: A LayeredImage Attribute instance to represent this
            `SCLayer` instance.
            """
            return Attribute(None, self._name, image=self.build_image(), default=True)


    class CustomizedSprite:
        """
        # Customized Sprite

        Represents a multi-layered sprite image composed of customizable layers.

        This type provides methods for manipulating the layers by changing their
        customizations between each layer's configured customization options.

        ## Usage

        ### In Scripts

        Whether constructed directly, or via the `CustomizedSpriteFactory` type,
        the first step to using the `CustomizedSprite` is to give it its state.

        This is done by creating a new `SCState` instance in a runtime variable
        via a Python line or a `default` statement:

        ```renpy
        default my_sprite_state = SCState()
        ```

        Then pass that newly created state to the `CustomizedSprite` instance
        via the `set_state` method.

        ------------------------------------------------------------------------
        | IMPORTANT! | This MUST be done in both the `start` and `after_load`  |
        |            | labels to ensure the state is properly loaded from the  |
        |            | save.                                                   |
        ------------------------------------------------------------------------

        ```renpy
        label after_load:
            $ my_sprite.set_state(my_sprite_state)

        label start:
            $ my_sprite.set_state(my_sprite_state)
        ```

        ### Construction

        The `CustomizedSprite` class may be constructed directly or via the
        `CustomizedSpriteFactory` type.  Deciding whether to construct the type
        directly or via the factory comes down to whether you want to create
        multiple sprites from the same set of options.

        If you only want to create a single sprite out of a set of layers and
        options, then it is fine to construct new `CustomizedSprite` instances
        directly.

        If you want to create more than a single sprite out of a set of layers
        and options then it is best to create a `CustomizedSpriteFactory`
        instance then use that to create the `CustomizedSprite` instances.
        """
        def __init__(self, image_name, *layers):
            """
            Initializes a new `CustomizedSprite` instance with the given
            arguments.

            Arguments:

            image_name (str):  Name of the image that will be created for this
            sprite.  This name is the value that will be used when referencing
            the sprite elsewhere in scripts via `show`, `add`, etc..

            layers (SCLayer[]):  A list of one or more layers from which the
            sprite should be created.  The layers are stacked on top of one
            another in the passed order.  This means the first given layer will
            be at the "back" of the sprite, where the last given layer will be
            the "front".
            """

            self._layers = layers
            self._state  = SCState()

            self._option_to_layer = {}

            if len(layers) == 0:
                raise Exception("CustomizedSprite needs at least one layer to display!")

            # Verify that the given option names are unique.
            for layer in layers:
                if not isinstance(layer, SCLayer):
                    raise Exception("CustomizedSprite arguments 1+ must all be SCLayer instances.")

                for option_name, option in layer._options.items():
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
                raise Exception("Unrecognized CustomizedSprite option \"{}\"".format(option))

        def set_state(self, state):
            """
            Sets the internal state object of this `CustomizedSprite` instance
            to the given `SCState` instance.

            Arguments:

            state (SCState): State object to use for storing customization
            option selections.
            """
            if not isinstance(state, SCState):
                raise Exception("Value passed to set_state must be an SCState instance.")

            self._state = state
            for layer in self._layers:
                layer.set_state(state)

        def inc_selection(self, option):
            """
            Increments the selection value for the given option.

            Arguments:

            option (str): Key of the option for which the selection should be
            incremented.
            """
            self._require_option(option)
            self._option_to_layer[option].inc_selection(option)

        def dec_selection(self, option):
            """
            Decrements the selection value for the given option.

            Arguments:

            option (str): Key of the option for which the selection should be
            decremented.
            """
            self._require_option(option)
            self._option_to_layer[option].dec_selection(option)

        def option_display_name(self, option):
            self._require_option(option)
            return self._option_to_layer[option].option_display_name(option)

        def option_selection(self, option):
            self._require_option(option)
            return self._option_to_layer[option].option_selection(option)

        def get_option(self, option):
            self._require_option(option)
            self._option_to_layer[option].get_option(option)

        def option_value(self, option, selection):
            self._require_option(option)
            return self._option_to_layer[option].get_option_value(option, selection)

        @property
        def option_keys(self):
            """
            A list of all the option keys.
            """
            return self._option_to_layer.keys()

        @property
        def option_count(self):
            """
            Returns the total number of registered options.
            """
            return len(self._option_to_layer.keys())

        @property
        def menu_components(self):
            """
            Builds a map of option display names to the actual option keys to be
            used when generating a menu screen.
            """
            out = {}
            for layer in self._layers:
                for opt in layer._options.keys():
                    out[layer.option_display_name(opt)] = opt
            return out


    class CustomizedSpriteFactory:
        """
        # Customized Sprite Factory

        A factory that can be used to generate multiple `CustomizedSprite`
        instances with the same set of base options.
        """
        def __init__(self, *layers):
            """
            Initializes a new `CustomizedSpriteFactory` instance with the given
            arguments.

            Arguments:

            layers (SCLayer[]):  A list of one or more layers from which
            `CustomizedSprite` instances should be created.  The layers are
            stacked on top of one another in the passed order.  This means the
            first given layer will be at the "back" of the sprite, where the
            last given layer will be the "front".
            """
            if len(layers) == 0:
                raise Exception("CustomizedSpriteFactory needs at least one layer to display!")

            for layer in layers:
                if not isinstance(layer, SCLayer):
                    raise Exception("CustomizedSpriteFactory parameters must all be SCLayer instances.")

            self._layers = layers

        def new_sprite(self, image_name):
            """
            Constructs a new `CustomizedSprite` instance with the given name.

            Arguments:

            image_name (str):  Name of the image that will be created for the
            returned sprite.  This name is the value that will be used when
            referencing the sprite elsewhere in scripts via `show`, `add`, etc..
            """
            return CustomizedSprite(image_name, *[ layer.clone() for layer in self._layers ])