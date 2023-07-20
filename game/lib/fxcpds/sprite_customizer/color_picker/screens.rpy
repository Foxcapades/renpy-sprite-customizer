screen _sc_color_picker(option):

    default hsl_picker = HSLPicker(option)
    default rgb_picker = RGBPicker(option)
    default tabs = [ "HSL", "RGB" ]

    frame:
        modal True

        background "_cs_color_picker_coverall"

        xfill True
        yfill True

        frame:
            background None
            xcenter 0.5
            ycenter 0.5

            vbox:
                use _sc_color_picker_tab_bar(tabs)

                frame:

                    background sc.color_picker_background

                    xsize 0.5
                    xpadding 20
                    ypadding 20

                    if _cs_color_picker_tab == "HSL":
                        use _color_picker_hsl_body(option, hsl_picker)
                    elif _cs_color_picker_tab == "RGB":
                        use _color_picker_rgb_body(option, rgb_picker)

screen _sc_color_picker_tab_bar(tabs):
    hbox:
        for val in tabs:
            use _sc_color_picker_tab(val)


screen _sc_color_picker_tab(val):
    button:
        padding (0, 0)

        if _cs_color_picker_tab == val:
            background sc.color_picker_background
        else:
            background sc.color_picker_background_muted

        vbox:
            if _cs_color_picker_tab == val:
                add "_cs_color_picker_tab_header_active":
                    ysize 5
                    xsize 125
            else:
                add "_cs_color_picker_tab_header_muted":
                    ysize 5
                    xsize 125

            null:
                height 15

            text val:
                xcenter 0.5
                if _cs_color_picker_tab == val:
                    color sc.color_picker_text_color
                else:
                    color sc.color_picker_text_color_muted

            null:
                height 15

        action SetVariable("_cs_color_picker_tab", val)



screen _color_picker_hsl_body(option, bg_picker):
    default hex_value = HexInputValue(option)

    vbox:
        spacing 20

        hbox:
            spacing 20

            imagebutton:
                idle option.preview_image_name
                xsize 270
                ysize 270
                yalign 1.0

            vbox:
                spacing 20

                vbox:
                    text "Hue":
                        color sc.color_picker_text_color
                        yalign 0.5
                    bar:
                        value bg_picker.hue
                        range 359
                        changed bg_picker.set_hue
                vbox:
                    text "Saturation":
                        color sc.color_picker_text_color
                        yalign 0.5
                    bar:
                        value bg_picker.saturation
                        range 100
                        changed bg_picker.set_saturation
                vbox:
                    text "Brightness":
                        color sc.color_picker_text_color
                        yalign 0.5
                    bar:
                        value bg_picker.lightness
                        range 100
                        changed bg_picker.set_lightness

        use _color_picker_footer(hex_value, bg_picker)


screen _color_picker_rgb_body(option, bg_picker):
    default h_value = HexInputValue(option)

    vbox:
        spacing 20

        hbox:
            spacing 20

            imagebutton:
                idle option.preview_image_name
                xsize 270
                ysize 270
                yalign 1.0

            vbox:
                spacing 20

                vbox:
                    text "Red":
                        color sc.color_picker_text_color
                        yalign 0.5
                    bar:
                        value bg_picker.red
                        range 255
                        changed bg_picker.set_red
                vbox:
                    text "Green":
                        color sc.color_picker_text_color
                        yalign 0.5
                    bar:
                        value bg_picker.green
                        range 255
                        changed bg_picker.set_green
                vbox:
                    text "Blue":
                        color sc.color_picker_text_color
                        yalign 0.5
                    bar:
                        value bg_picker.blue
                        range 255
                        changed bg_picker.set_blue

        use _color_picker_footer(h_value, bg_picker)

screen _color_picker_footer(h_value, bg_picker):
    hbox:
        button:
            key_events True
            xsize 195
            background sc.input_background_idle_color
            hover_background sc.input_background_hover_color

            input:
                value h_value
                prefix '#'
                length 6
                copypaste True
                color sc.input_text_color

            action h_value.Toggle()

        null:
            width 619

        textbutton "Done":
            text_style "_color_picker_text_button_style"
            action Hide("_cs_color_picker")
