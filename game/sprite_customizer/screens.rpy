# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#    Images
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

image cc_gui_option_arrow_right_idle:
    "sprite_customizer/img/arrow.png"
    xsize 50
    ysize 50

image cc_gui_option_arrow_right_hover = Transform("cc_gui_option_arrow_right_idle", matrixcolor=BrightnessMatrix(-0.5))

image cc_gui_option_arrow_left_idle:
    "sprite_customizer/img/arrow.png"
    xsize 50
    ysize 50
    xzoom -1.0

image cc_gui_option_arrow_left_hover = Transform("cc_gui_option_arrow_left_idle", matrixcolor=BrightnessMatrix(-0.5))

image cc_checkbox_blank_idle:
    "sprite_customizer/img/checkbox_blank_idle.png"
    xsize 50
    ysize 50

image cc_checkbox_blank_hover:
    "sprite_customizer/img/checkbox_blank_hover.png"
    xsize 50
    ysize 50

image cc_checkbox_checked_idle:
    "sprite_customizer/img/checkbox_checked_idle.png"
    xsize 50
    ysize 50

image cc_checkbox_checked_hover:
    "sprite_customizer/img/checkbox_checked_hover.png"
    xsize 50
    ysize 50


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#    Screens
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


screen sprite_creator(sprite, customizer):
    modal True

    hbox:
        use sprite_creator_left(sprite)
        use sprite_creator_right(customizer)


screen sprite_creator_left(sprite):
    frame:
        background Solid("#9cb9cb")
        xsize 0.7
        ysize 1.0

        add sprite:
            xalign 0.5


screen sprite_creator_right(customizer):
    frame:
        background Solid("#1f1f1f")
        ysize 1.0
        xsize 1.0

        vbox:
            spacing 50
            yalign 0.5
            xcenter 0.5

            for group, options in customizer.get_options_by_group().items():
                use sprite_creator_option_group(customizer, group, options)

            null:
                height 50

            hbox:
                xalign 0.5
                spacing 50

                textbutton "Randomize":
                    action Function(customizer.randomize)

                textbutton "Done":
                    action Return(0)

screen sprite_creator_option_group(sprite, group, options):
    vbox:
        spacing 20

        text group:
            color "#FFB69D"

        hbox:
            null:
                width 25
            vbox:
                spacing 15
                for option_key, option in options.items():
                    use sprite_creator_option_group_option(sprite, option_key, option)


screen sprite_creator_option_group_option(sprite, option_key, option):
    hbox:
        text option.display_name:
            min_width 200
            line_leading 5

        if isinstance(option, SCValueListOption):
            use sprite_creator_value_list_option(option)
        elif isinstance(option, SCValidatableTextOption):
            use sprite_creator_validatable_text_option(option)
        elif isinstance(option, SCTextOption):
            use sprite_creator_text_option(option)
        elif isinstance(option, SCBooleanOption):
            use sprite_creator_boolean_option(option)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#    Option Components
#
# The following screens are components for rendering specific types of options.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# Value List Option Selector
screen sprite_creator_value_list_option(option):
    hbox:
        xsize 200

        imagebutton:
            auto "cc_gui_option_arrow_left_%s"
            xsize 50
            ysize 50
            action Function(option.dec_selection)
        text "{:02d}".format(option.selection_index + 1):
            line_leading 5
        imagebutton:
            auto "cc_gui_option_arrow_right_%s"
            xsize 50
            ysize 50
            action Function(option.inc_selection)


# Text Option Input
screen sprite_creator_text_option(option):
    default option_value = SCTextInput(option)

    button:
        xsize 175

        key_events True
        action option_value.Toggle()

        background "#2e2c2c"
        hover_background "#383535"

        input:
            value option_value
            copypaste True

            if option.has_prefix:
                prefix option.prefix

            if option.has_suffix:
                suffix option.suffix

            if option.has_max_len:
                length option.max_len


# Validatable Text Option Input
screen sprite_creator_validatable_text_option(option):
    default option_value = SCTextInput(option)

    button:
        xsize 175

        key_events True
        background "#2e2c2c"
        hover_background "#383535"
        action option_value.Toggle()

        input:
            value option_value
            copypaste True

            if not option.is_valid:
                color "#FF0000"

            if option.has_prefix:
                prefix option.prefix

            if option.has_suffix:
                suffix option.suffix

            if option.has_max_len:
                length option.max_len


# Boolean Option Input
screen sprite_creator_boolean_option(option):
    hbox:
        xsize 200
        ysize 50

        imagebutton:
            xcenter 0.5
            ycenter 0.5

            if option.value:
                auto "cc_checkbox_checked_%s"
            else:
                auto "cc_checkbox_blank_%s"

            action Function(option.toggle)
