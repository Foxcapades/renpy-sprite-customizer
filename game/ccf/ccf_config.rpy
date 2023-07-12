# Here we will define all the callbacks that will be used to render changes to
# our custom character sprites.  There will be one callback per layer to provide
# the customization for that layer.
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

    def cc_skin(skin_color, **kwargs):
        """
        CustomizedCharacter Example: Skin Callback

        The `cc_skin` callback takes the `skin_color` argument and uses it to
        generate a displayable for the chosen skin color option.

        The `skin_color` argument value will be one of the hex code values
        defined in the `skin_color=CCOpt(...` declaration below and is used with
        a TintMatrix to Transform the colorless base image into a base image
        with the selected color overlayed.
        """
        return Transform("images/ccp/base/base.png", matrixcolor=TintMatrix(skin_color))

    def cc_clothes(clothes, **kwargs):
        """
        CustomizedCharacter Example: Clothes Callback

        The `cc_clothes` callback takes the `clothes` argument and uses it to
        generate a displayable for the chosen clothes option.

        The `clothes` argument value will be one of the values defined in the
        `clothes=CCOpt(...` declaration below and is used to generate the path
        to the correct clothing option to render.
        """
        return "images/ccp/clothes/{}.png".format(clothes)

    def cc_hair(hair_style, hair_color, **kwargs):
        """
        CustomizedCharacter Example: Hair Callback

        The `cc_hair` callback takes the `hair_style` and `hair_color` arguments
        and uses them to generate a displayable for the chosen hair options.

        The `hair_style` argument value will be one of the hair style options
        defined in the layer declaration below.  This value is used to form the
        path to the target image that will be used as the base for the
        customized character's hair.

        The `hair_color` argument is one of the hex code options defined in the
        layer declaration below.  This value is used to create a TintMatrix
        transform to apply color to the selected base hair style.
        """
        return Transform("images/ccp/hair/{}.png".format(hair_style), matrixcolor=TintMatrix(hair_color))

    def cc_accessory(accessory, **kwargs):
        """
        CustomizedCharacter Example: Accessory Callback

        The `cc_accessory` callback takes the `accessory` argument and uses it
        to generate the path to the target accessory image.

        The `accessory` value will be one of the accessory options defined in
        the layer declaration below.
        """
        return "images/ccp/accessories/{}.png".format(accessory)

    def cc_eyes(eye_color, **kwargs):
        """
        CustomizedCharacter Example: Eyes Callback

        The `cc_eyes` callback takes an `eye_color` argument and uses it to
        generate the path to the target eye image.

        The `eye_color` value will be one of the eye color options defined in
        the layer declaration below.
        """
        return "images/ccp/eyes/{}_eyes.png".format(eye_color)

# Customized Character Factory Declaration.
#
# This demonstrates the creation of a customized character sprite.  The creation
# of this sprite takes 2+ parameters.
#
# The first parameter is the name of the customized character sprite to be used
# wherever a displayable may normally be referenced.  (`show` statements, `add`
# statements, Transforms, etc...).
#
# The following parameter is the base image layer for the sprite.  A base layer
# is required to construct a CustomizedCharacter instance.
#
# All following parameters are additional layers that are placed on top of one
# another in declaration order stepping "closer" to the player with each new
# layer.
define ccf = CustomizedCharacterFactory(
    # Skin Layer
    CCLayer("skin", cc_skin, skin_color=CCOpt("Skin", [
        "#513021",
        "#874c2c",
        "#803716",
        "#b66837",
        "#a96238",
        "#f9bf91",
        "#ecc19f"
    ])),

    # Clothes Layer
    CCLayer("clothes", cc_clothes, clothes=CCOpt("Clothes", [ "cottoncandy", "plaid" ])),

    # Hair Layer
    CCLayer(
        "hair",
        cc_hair,
        hair_style=CCOpt("Hair Style", [ "afro", "bob", "buns" ]),
        hair_color=CCOpt("Hair Color", [
            "#3D2314",
            "#100C07",
            "#DA680F",
            "#FFCC47",
            "#9A9E9F",
            "#FAFAFA",
            "#801818",
            "#580271",
            "#1592CA",
            "#11694E",
            "#FF87C5"
        ]),
    ),

    # Accessory Layer
    CCLayer("accessories", cc_accessory, accessory=CCOpt("Accessory", [
        "none",
        "cottoncandy_bow",
        "cottoncandy_clips",
        "plaid_bow",
        "plaid_clips",
    ])),


    # Eye Layer
    CCLayer("eyes", cc_eyes, eye_color=CCOpt("Eyes", [
        "blue",
        "brown",
        "green",
        "grey"
    ])),
)

# Create defines for the sprite controller classes which are used by screens to
# manipulate our custom sprites.
#
# The string value passed into the `customized_character` method is the name of
# the image that will be created.  Meaning if you pass in the string
# "player_base" you can now reference that image like normal by doing things
# such as `show player_base`.
define cc_player_sprite = ccf.customized_character("player_base")
define cc_antagonist_sprite = ccf.customized_character("antagonist_base")