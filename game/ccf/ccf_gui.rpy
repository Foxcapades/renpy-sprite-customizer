image gui_close_idle:
    "ccf/img/close_idle.png"
    xsize 50
    ysize 50
image gui_close_hover:
    "ccf/img/close_hover.png"
    xsize 50
    ysize 50

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
        xsize 0.5
        ysize 1.0

        add character:
            xalign 0.5

screen character_creator_right(customizer):
    frame:
        background Solid("#1f1f1f")
        ysize 1.0
        xsize 1.0

        vbox:
            grid 4 customizer.option_count:
                spacing 25

                for name, opt in customizer.menu_components.items():
                    text "[name]:"
                    imagebutton:
                        auto "cc_gui_option_arrow_left_%s"
                        xsize 50
                        ysize 50
                        action Function(customizer.dec_option, opt)
                    text customizer.option_value_text(opt)
                    imagebutton:
                        auto "cc_gui_option_arrow_right_%s"
                        xsize 50
                        ysize 50
                        action Function(customizer.inc_option, opt)
            imagebutton:
                auto "gui_close_%s"
                xsize 50
                ysize 50
                action Return(0)
