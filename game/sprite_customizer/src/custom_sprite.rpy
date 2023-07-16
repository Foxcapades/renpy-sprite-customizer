init -1 python:
    from collections import OrderedDict

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
            self._options_by_group = OrderedDict()

            if len(layers) == 0:
                raise Exception("CustomizedSprite needs at least one layer to display!")

            # For each given item...
            for layer in layers:
                # ensure that it is an SCLayer
                if not isinstance(layer, SCLayer):
                    raise Exception("CustomizedSprite arguments 1+ must all be SCLayer instances.")

                # For each option attached to the layer...
                for option_name, option in layer._options.items():
                    # If the option is already known to this sprite, then it is
                    # a duplicate.
                    if option_name in self._option_to_layer:
                        raise Exception("Duplicate option \"{}\"".format(option_name))

                    # Record the option to layer link
                    self._option_to_layer[option_name] = layer

                    opt_group = option.group if option.has_group else option.display_name

                    # Record the group to option link.
                    if opt_group in self._options_by_group:
                        self._options_by_group[opt_group].append(option_name)
                    else:
                        self._options_by_group[opt_group] = [ option_name ]

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

        def get_options_by_group(self, group_order=None):
            """
            Returns an index of options and display names grouped by layer group
            name.  This index may optionally be ordered by providing a list of
            the desired group order.

            [NOTE]
            --
            Options that do not have a group name declared on them, their
            display name will be used as the group name.
            --

            ```python
            sprite.get_options_by_group()

            sprite.get_options_by_group(["Body", "Face", "Hair"])
            ```

            Arguments:

            group_order (list): Optional list of option group names by which the
            output dict will be ordered.  This list *MUST* contain all of the
            groups declared in the SCLayer definitions, and ONLY those groups.

            Returns:

            An index of the declared sprite customization options grouped by
            the configured option groups.

            ```python
            {
                "Body": {
                    "skin_color": "Skin Color",
                    "clothes": "Clothes",
                },
                "Face": {
                    "eyes": "Eye Color"
                }
                "Hair": {
                    "hair_style": "Hair Style",
                    "hair_color": "Hair Color",
                    "accessory": "Accessory"
                },
            }
            ```
            """
            out = OrderedDict()

            if group_order == None:
                for group, options in self._options_by_group.items():
                    out[group] = OrderedDict()
                    for option in options:
                        out[group][option] = self.get_option_display_name(option)
            elif isinstance(group_order, list):
                for group in group_order:
                    out[group] = OrderedDict()
                    for option in self._options_by_group[group]:
                        out[group][option] = self.get_option_display_name(option)
            else:
                raise Exception("group_order must be a list, a set, or None")

            return out


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
            out = OrderedDict()
            for layer in self._layers:
                for opt in layer._options.keys():
                    out[layer.get_option_display_name(opt)] = opt

            return out
