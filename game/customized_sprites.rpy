# Here we will define all the callbacks that will be used to render changes to
# our custom character sprites.  Layers may use these callbacks to provide the
# customization.
#
# Each callback will be passed to a layer as a constructor argument, and should
# take the option keys defined on that layer as function arguments.
#
# The values of those arguments will be one of the options defined when creating
# a layer.
#
# For example, if you were to define a layer with the options "foo_bar" and
# "fizz_buzz", the callback given to that layer should take 2 arguments named
# "foo_bar" and "fizz_buzz":
#
#    def my_callback(foo_bar, fizz_buzz, **kwargs):
#        return ...
#
# These callbacks must return a displayable.
init python:

    def sc_skin(skin_color, **kwargs):
        """
        CustomizedSprite Example: Skin Callback

        The `sc_skin` callback takes the `skin_color` argument and uses it to
        generate a displayable for the chosen skin color option.

        The `skin_color` argument value will be one of the hex code values
        defined in the `skin_color=SCListOption(...` declaration below and is
        used with a TintMatrix to Transform the colorless base image into a base
        image with the selected color overlayed.
        """
        return Transform("images/ccp/base/base.png", matrixcolor=TintMatrix(skin_color))

    def sc_hair(hair_style, hair_color, **kwargs):
        """
        CustomizedSprite Example: Hair Callback

        The `sc_hair` callback takes the `hair_style` and `hair_color` arguments
        and uses them to generate a displayable for the chosen hair options.

        The `hair_style` argument value will be one of the hair style options
        defined in the layer declaration below.  This value is used to form the
        path to the target image that will be used as the base for the
        customized character's hair.

        The `hair_color` argument is one of the hex code options defined in the
        layer declaration below.  This value is used to create a TintMatrix
        transform to apply color to the selected base hair style.
        """
        if hair_color == None:
            raise Exception("oops")
        return Transform("images/ccp/hair/{}.png".format(hair_style), matrixcolor=TintMatrix(hair_color))

    def sc_accessory(has_accessory, accessory, **kwargs):
        """
        CustomizedSprite Example: Accessory Callback

        The `sc_accessory` callback takes the `has_accessory` and `accessory`
        arguments and uses them to generate a displayable for the accesory
        options.

        The `has_accessory` argument value will be a boolean flag indicating
        whether an accessory should be shown.

        The `accessory` argument value will be the name of the accessory image
        to show if `has_accessory` is true.
        """
        if has_accessory:
            return f"images/ccp/accessories/{accessory}.png"
        else:
            return Null()


# Customized Sprite Factory Declaration.
#
# The CustomizedSpriteFactory may be used to generate one or more custom sprite
# instances.
define ccf = CustomizedSpriteFactory(

    # Skin Layer : List Option
    SCLayer("skin", sc_skin, SCListOption("skin_color", "Skin", "Body", [
        "#513021",
        "#874c2c",
        "#803716",
        "#b66837",
        "#a96238",
        "#f9bf91",
        "#ecc19f"
    ])),

    # Clothes Layer : List Option
    SCLayer(
        "clothes",
        "images/ccp/clothes/{clothes}.png",
        SCListOption("clothes", "Clothes", "Body", [ "cottoncandy", "plaid" ])
    ),

    # Hair Layer : List Option + Color Option
    SCLayer("hair", sc_hair, [
        SCListOption("hair_style", "Style", "Hair", [ "afro", "bob", "buns" ]),
        SCColorOption("hair_color", "Color", "Hair", "#704024")
    ]),

    # Accessory Layer : Boolean Option + Value List
    SCLayer(
        "accessories",
        sc_accessory,
        [
            SCBooleanOption("has_accessory", "Show", "Accessory"),
            SCListOption("accessory", "Type", "Accessory", [
                "cottoncandy_bow",
                "cottoncandy_clips",
                "plaid_bow",
                "plaid_clips",
            ])
        ]
    ),

    # Eye Layer : Value List
    SCLayer(
        "eyes",
        "images/ccp/eyes/{eye_color}_eyes.png",
        SCListOption("eye_color", "Eyes", "Face", [
            "blue",
            "brown",
            "green",
            "grey"
        ])
    ),
)

# Create defines for the sprite controller classes which are used by screens to
# manipulate our custom sprites.
#
# The string value passed into the `new_sprite` method is the name of
# the image that will be created.  Meaning if you pass in the string
# "player_base" you can now reference that image like normal by doing things
# such as `show player_base`.
define sc_player_sprite = ccf.new_sprite("player_base")
define sc_antagonist_sprite = ccf.new_sprite("antagonist_base")
