image cc_gui_option_arrow_right_idle:
    "ccf/img/arrow.png"
    xsize 50
    ysize 50

image cc_gui_option_arrow_right_hover = Transform("cc_gui_option_arrow_right_idle", matrixcolor=BrightnessMatrix(-0.5))

image cc_gui_option_arrow_left_idle:
    "ccf/img/arrow.png"
    xsize 50
    ysize 50
    xzoom -1.0

image cc_gui_option_arrow_left_hover = Transform("cc_gui_option_arrow_left_idle", matrixcolor=BrightnessMatrix(-0.5))


screen character_creator(character, customizer):
    modal True

    hbox:
        use character_creator_left(character)
        use character_creator_right(customizer)

screen character_creator_left(character):
    frame:
        background Solid("#9cb9cb")
        xsize 0.7
        ysize 1.0

        add character:
            xalign 0.5

screen character_creator_right(customizer):
    frame:
        background Solid("#1f1f1f")
        ysize 1.0
        xsize 1.0

        vbox:
            spacing 50
            yalign 0.5

            for name, opt in customizer.menu_components.items():
                hbox:
                    xalign 0.5
                    xminimum 550
                    yminimum 1.0

                    null:
                        width 50
                    text name:
                        min_width 200
                        line_leading 5
                    imagebutton:
                        auto "cc_gui_option_arrow_left_%s"
                        xsize 50
                        ysize 50
                        action Function(customizer.dec_option, opt)
                    text customizer.option_value_text(opt):
                        line_leading 5
                    imagebutton:
                        auto "cc_gui_option_arrow_right_%s"
                        xsize 50
                        ysize 50
                        action Function(customizer.inc_option, opt)

            null:
                height 50

            textbutton "Done!":
                xalign 0.5
                action Return(0)
