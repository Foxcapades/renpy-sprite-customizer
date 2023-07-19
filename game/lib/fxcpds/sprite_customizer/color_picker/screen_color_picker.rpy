screen _cs_color_picker(option):

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
                use _cs_color_picker_tab_bar(tabs)

                frame:

                    background "_cs_color_picker_background"

                    xsize 0.5
                    xpadding 20
                    ypadding 20

                    if _cs_color_picker_tab == "HSL":
                        use _color_picker_hsl_body(option, hsl_picker)
                    elif _cs_color_picker_tab == "RGB":
                        use _color_picker_rgb_body(option, rgb_picker)

screen _cs_color_picker_tab_bar(tabs):
    hbox:
        for val in tabs:
            button:
                padding (25, 10)

                if _cs_color_picker_tab == val:
                    background "#2e2c2c"
                else:
                    background "#1f1f1f"

                text val:
                    if _cs_color_picker_tab == val:
                        color "#dddddd"
                    else:
                        color "#bbbbbb"

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
                        color "#dddddd"
                        yalign 0.5
                    bar:
                        value bg_picker.hue
                        range 359
                        changed bg_picker.set_hue
                vbox:
                    text "Saturation":
                        color "#dddddd"
                        yalign 0.5
                    bar:
                        value bg_picker.saturation
                        range 100
                        changed bg_picker.set_saturation
                vbox:
                    text "Brightness":
                        color "#dddddd"
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
                        color "#dddddd"
                        yalign 0.5
                    bar:
                        value bg_picker.red
                        range 255
                        changed bg_picker.set_red
                vbox:
                    text "Green":
                        color "#dddddd"
                        yalign 0.5
                    bar:
                        value bg_picker.green
                        range 255
                        changed bg_picker.set_green
                vbox:
                    text "Blue":
                        color "#dddddd"
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
            xsize 172
            background "#ddd"

            input:
                value h_value
                prefix '#'
                length 6
                copypaste True

            action h_value.Toggle()

        null:
            width 642

        textbutton "Done":
            text_style "_color_picker_text_button_style"
            action Hide("_cs_color_picker")
