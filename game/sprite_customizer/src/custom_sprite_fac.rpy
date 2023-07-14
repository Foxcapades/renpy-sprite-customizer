init -1 python:
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