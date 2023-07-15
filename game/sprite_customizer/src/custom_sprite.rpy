init -1 python:
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
        def __init__(self, image_name, *layers, **kwargs):
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

            transform (callable): An optional transform function that will be
            applied to the created image.
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

            if "transform" in kwargs:
                if not callable(kwargs["transform"]):
                    raise Exception("CustomizedSprite transform must be callable.")
                else:
                    transform = kwargs["transform"]
            else:
                transform = None

            # Build the layered image
            attrs = [ layers[0].build_image() ]

            for i in range(1, len(layers)):
                attrs.append(layers[i].build_attribute())

            if transform == None:
                renpy.image(image_name, LayeredImage(attrs))
            else:
                from uuid import uuid4
                tmp_name = str(uuid4())
                renpy.image(tmp_name, LayeredImage(attrs))
                renpy.image(image_name, transform(tmp_name))

        def _require_option(self, option):
            if not option in self._option_to_layer:
                raise Exception("Unrecognized CustomizedSprite option \"{}\"".format(option))

        def set_state(self, state):
            """
            Sets the internal state object of this CustomizedSprite instance to
            the given SCState instance.

            [source, python]
            ----
            define my_sprite = CustomizedSprte("sprite", ...)
            default my_sprite_state = SCState()

            label start:
                $ my_sprite.set_state(my_sprite_state)

            label after_load:
                $ my_sprite.set_state(my_sprite_state)
            ----

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

        def get_option_display_name(self, option):
            """
            Returns the display name for the target option.

            Arguments:

            option (str): Keword for the option whose display name should be
            returned.

            Returns:

            str: Display name for the target option.
            """
            self._require_option(option)
            return self._option_to_layer[option].get_option_display_name(option)

        def get_option_selection(self, option):
            self._require_option(option)
            return self._option_to_layer[option].get_option_selection(option)

        def get_option(self, option):
            self._require_option(option)
            return self._option_to_layer[option].get_option(option)

        def get_option_value(self, option):
            self._require_option(option)
            return self._option_to_layer[option].get_option_value(option, selection)

        def get_selected_option_value(self, option):
            """
            Returns the currently selected option value for the target option.

            ```python
            my_sprite = CustomizedSprite(
                "sprite",
                SCLayer("hair", hair_lcb, hair_style=SCOpt("Hair Style", [ "afro", "bob", "bun" ]))
            )
            my_sprite.set_state(SCState())

            my_sprite.get_selected_option_value("hair_style") == "afro"

            my_sprite.inc_selection("hair_style")

            my_sprite.get_selected_option_value("hair_style") == "bob"
            ```

            Arguments:

            option (str): Keyword for the option whose user selected value
            should be returned.

            Returns:

            any: The currently selected option value for the target option.
            """
            self._require_option(option)
            return self._option_to_layer[option].get_selected_option_value(option)

        @property
        def layers(self):
            return [ *self._layers ]

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
                    out[layer.get_option_display_name(opt)] = opt

            return out
