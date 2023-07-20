from renpy.store import LayeredImage  # type: ignore
import renpy.exports as renpy  # type: ignore

from .layer_ren import SCLayer
from ..state.state_ren import SCState
from ..options.option_ren import SCOption

"""renpy
init -1 python:
"""

from collections import OrderedDict


# noinspection PyProtectedMember
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

    def __init__(self, image_name: str, *layers: SCLayer, **kwargs: any):
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
        self._layers: list[SCLayer] = [*layers]
        self._options = OrderedDict()
        self._option_to_layer = OrderedDict()
        self._options_by_group = OrderedDict()

        if len(layers) == 0:
            raise Exception("CustomizedSprite needs at least one layer to display!")

        # For each given item...
        for layer in layers:
            if not isinstance(layer, SCLayer):
                raise Exception("CustomizedSprite arguments 1+ must all be SCLayer instances.")

            for option_key, option in layer._options.items():
                if option_key in self._options:
                    raise Exception("Duplicate option \"{}\"".format(option_key))

                self._option_to_layer[option_key] = layer
                self._options[option_key] = option

                if option.group in self._options_by_group:
                    self._options_by_group[option.group].append(option)
                else:
                    self._options_by_group[option.group] = [option]

        if "transform" in kwargs:
            if not callable(kwargs["transform"]):
                raise Exception("CustomizedSprite transform must be callable.")
            else:
                transform = kwargs["transform"]
        else:
            transform = None

        # Build the layered image
        attrs = [layers[0]._build_image()]

        for i in range(1, len(layers)):
            attrs.append(layers[i]._build_attribute())

        if transform is None:
            renpy.image(image_name, LayeredImage(attrs))
        else:
            from uuid import uuid4
            tmp_name = str(uuid4())
            renpy.image(tmp_name, LayeredImage(attrs))
            renpy.image(image_name, transform(tmp_name))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Properties
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @property
    def layers(self) -> list[SCLayer]:
        """
        The list of layers attached to this CustomizedSprite instance.
        """
        return [*self._layers]

    @property
    def option_keys(self) -> list[str]:
        """
        A list of the keys for all the options attached to this
        CustomizedSprite instance.
        """
        return [*self._option_to_layer.keys()]

    @property
    def option_count(self) -> int:
        """
        Returns the total number of registered options.
        """
        return len(self._option_to_layer.keys())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Internal Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _require_option(self, option: str):
        if option not in self._option_to_layer:
            raise Exception("Unrecognized CustomizedSprite option \"{}\"".format(option))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    #
    #   Public Methods
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def set_state(self, state: SCState):
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

        for layer in self._layers:
            layer._set_state(state)

    def get_options(self) -> list[SCOption]:
        """
        Gets a list of the options attached to this CustomizedSprite
        instance.

        Returns
        -------

        SCOption[]
            List of the options attached to this CustomizedSprite instance.
        """
        return [*self._options.values()]

    def get_options_by_key(self) -> OrderedDict:
        """
        Gets a dict of option keys mapped to SCOption instances for all the
        options attached to this CustomizedSprite.

        Returns
        -------

        dict
            Dict of option keys mapped to SCOption instances.
        """
        return self._options.copy()

    def get_options_by_group(self, group_order: list | None = None) -> OrderedDict:
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
                "skin_color": <SCOption>,
                "clothes": <SCOption>,
            },
            "Face": {
                "eyes": <SCOption>
            }
            "Hair": {
                "hair_style": <SCOption>,
                "hair_color": <SCOption>,
                "accessory": <SCOption>
            },
        }
        ```
        """
        out = OrderedDict()

        if group_order is None:
            for group, options in self._options_by_group.items():
                out[group] = OrderedDict()
                for option in options:
                    out[group][option] = option

        elif isinstance(group_order, list):
            if len(group_order) != len(self._options_by_group):
                raise Exception("group_order parameter must contain all and only the declared option group names for "
                                "this CustomizedSprite's layers")

            for group in group_order:
                out[group] = OrderedDict()

                if group not in self._options_by_group:
                    raise Exception("unrecognized option group name \"{}\"".format(group))

                for option in self._options_by_group[group]:
                    out[group][option] = option

        else:
            raise Exception("group_order must be a list, a set, or None")

        return out

    def randomize(self):
        """
        Randomizes the selections for all the options on this
        CustomizedSprite instance.
        """
        for option in self._options.values():
            option.randomize()


class CustomizedSpriteFactory:
    """
    # Customized Sprite Factory

    A factory that can be used to generate multiple `CustomizedSprite`
    instances with the same set of base options.
    """

    def __init__(self, *layers: SCLayer, **kwargs: any):
        """
        Initializes a new `CustomizedSpriteFactory` instance with the given
        arguments.

        Arguments:

        layers (SCLayer[]):  A list of one or more layers from which
        `CustomizedSprite` instances should be created.  The layers are
        stacked on top of one another in the passed order.  This means the
        first given layer will be at the "back" of the sprite, where the
        last given layer will be the "front".

        transform (callable): An optional transform function that will be
        applied to images created by this factory.
        """
        if len(layers) == 0:
            raise Exception("CustomizedSpriteFactory needs at least one layer to display!")

        for layer in layers:
            if not isinstance(layer, SCLayer):
                raise Exception("CustomizedSpriteFactory parameters must all be SCLayer instances.")

        self._layers = layers
        self._kwargs = kwargs

    def new_sprite(self, image_name: str, **kwargs: any):
        """
        Constructs a new `CustomizedSprite` instance with the given name.

        Arguments:

        image_name (str):  Name of the image that will be created for the
        returned sprite.  This name is the value that will be used when
        referencing the sprite elsewhere in scripts via `show`, `add`, etc..
        """
        for key in self._kwargs.keys():
            if not key in kwargs:
                kwargs[key] = self._kwargs[key]

        return CustomizedSprite(image_name, *[layer._clone() for layer in self._layers], **kwargs)
