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

            textbutton "Done!":
                xalign 0.5
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
                for option_key, option_name in options.items():
                    use sprite_creator_option_group_option(sprite, option_key, option_name)

screen sprite_creator_option_group_option(sprite, option_key, option_name):
    hbox:
        text option_name:
            min_width 200
            line_leading 5

        imagebutton:
            auto "cc_gui_option_arrow_left_%s"
            xsize 50
            ysize 50
            action Function(sprite.dec_selection, option_key)
        text "{:02d}".format(sprite.get_option_selection(option_key)):
            line_leading 5
        imagebutton:
            auto "cc_gui_option_arrow_right_%s"
            xsize 50
            ysize 50
            action Function(sprite.inc_selection, option_key)
