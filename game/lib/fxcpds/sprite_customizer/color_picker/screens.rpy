transform _color_picker_slider:
    shader "fxcpds.slider"


transform _color_picker_square(tr):
    shader "fxcpds.color_block"
    u_top_right_rgb _color_picker_normalize_rgb(tr.rgb)


screen _fox_color_picker(option, initial_color = FoxHSV(0, 1.0, 1.0)):
    default picker = ColorPicker(400, 400, option, initial_color if isinstance(initial_color, FoxColor) else hex_to_fox_rgb(initial_color))

    frame:
        background sc.modal_coverall_color
        xfill True
        yfill True

        use _fox_color_picker_body(picker)


screen _fox_color_picker_body(picker):
    default slider_tab = StringContainer("RGB")

    frame:
        style '_fox_color_picker_body'

        hbox:
            vbox:
                use _fox_color_picker_picker_tabs()
                use _fox_color_picker_picker_body(picker)
            vbox:
                use _fox_color_picker_slider_tabs(slider_tab)
                use _fox_color_picker_slider_body(picker, slider_tab)


screen _fox_color_picker_picker_tabs:
    hbox:
        vbox:
            button:
                style '_fox_color_picker_tab_marker_selected'

                text "Picker":
                    style '_fox_color_picker_tab_text'
            button:
                style '_fox_color_picker_tab_selected'
                text "Picker":
                    style '_fox_color_picker_tab_text_selected'


screen _fox_color_picker_picker_body(picker):
    frame:
        style '_fox_color_picker_picker_body'

        hbox:
            spacing 5
            add picker
            vbar:
                value picker.rotation
                xysize (25, 400)
                range 359
                base_bar At(Transform('#fff', xysize=(25, 400)), _color_picker_slider())
                thumb Transform("lib/fxcpds/sprite_customizer/color_picker/slider.png")
                thumb_offset 4
                changed picker.set_rotation


screen _fox_color_picker_slider_tabs(selected_tab):
    hbox:
        use _fox_color_picker_slider_tab("RGB", selected_tab)
        use _fox_color_picker_slider_tab("HSL", selected_tab)
        use _fox_color_picker_slider_tab("HSV", selected_tab)


screen _fox_color_picker_slider_tab(name, selected_tab):
    vbox:
        button:
            if selected_tab.value == name:
                style '_fox_color_picker_tab_marker_selected'
            else:
                style '_fox_color_picker_tab_marker_idle'

            text name:
                style '_fox_color_picker_tab_text'

        button:
            if selected_tab.value == name:
                style '_fox_color_picker_tab_selected'
            else:
                style '_fox_color_picker_tab_idle'

            text name:
                if selected_tab.value == name:
                    style '_fox_color_picker_tab_text_selected'
                else:
                    style '_fox_color_picker_tab_text_idle'

            action Function(selected_tab.set_value, name)


screen _fox_color_picker_slider_body(picker, selected_tab):
    frame:
        style '_fox_color_picker_slider_body'

        vbox:
            spacing 10
            yfill True

            use _fox_color_picker_slider_header(picker)

            if selected_tab.value == 'RGB':
                use _fox_color_picker_rgb_slider_pane(picker)
            elif selected_tab.value == 'HSL':
                use _fox_color_picker_hsl_slider_pane(picker)
            elif selected_tab.value == 'HSV':
                use _fox_color_picker_hsv_slider_pane(picker)

            null:
                height 10

            use _fox_color_picker_slider_footer(picker)


screen _fox_color_picker_slider_header(picker):
    default hex_input = HexInputValue(picker)

    hbox:
        spacing 5

        text "Hex"

        null:
            width 25

        button:
            style '_fox_color_picker_hex_input_button'

            key_events True

            input:
                style '_fox_color_picker_hex_input_input'
                value hex_input
                prefix '#'
                length 6
                copypaste True

            action hex_input.Toggle()


screen _fox_color_picker_rgb_slider_pane(picker):
    vbox:
        spacing 10
        vbox:
            hbox:
                xfill True
                text "Red"
                text str(picker.rgb.red):
                    xalign 1.0
            bar:
                ysize 25
                range 255
                value picker.rgb.red
                changed _color_picker_rgb_bar_setter(picker, 'r')
        vbox:
            hbox:
                xfill True
                text "Green"
                text str(picker.rgb.green):
                    xalign 1.0
            bar:
                ysize 25
                range 255
                value picker.rgb.green
                changed _color_picker_rgb_bar_setter(picker, 'g')
        vbox:
            hbox:
                xfill True
                text "Blue"
                text str(picker.rgb.blue):
                    xalign 1.0
            bar:
                ysize 25
                range 255
                value picker.rgb.blue
                changed _color_picker_rgb_bar_setter(picker, 'b')


screen _fox_color_picker_hsl_slider_pane(picker):
    vbox:
        spacing 10
        vbox:
            hbox:
                xfill True
                text "Hue"
                text str(picker.hsl.hue):
                    xalign 1.0
            bar:
                ysize 25
                range 359
                value picker.hsl.hue
                changed _color_picker_hsl_bar_setter(picker, 'h')
        vbox:
            hbox:
                xfill True
                text "Saturation"
                text str(round(picker.hsl.saturation * 100)):
                    xalign 1.0
            bar:
                ysize 25
                range 1.0
                value picker.hsl.saturation
                changed _color_picker_hsl_bar_setter(picker, 's')
        vbox:
            hbox:
                xfill True
                text "Lightness"
                text str(round(picker.hsl.lightness * 100)):
                    xalign 1.0
            bar:
                ysize 25
                range 1.0
                value picker.hsl.lightness
                changed _color_picker_hsl_bar_setter(picker, 'l')


screen _fox_color_picker_hsv_slider_pane(picker):
    vbox:
        spacing 10
        vbox:
            hbox:
                xfill True
                text "Hue"
                text str(picker.hsv.hue):
                    xalign 1.0
            bar:
                ysize 25
                range 359
                value picker.hsv.hue
                changed _color_picker_hsv_bar_setter(picker, 'h')
        vbox:
            hbox:
                xfill True
                text "Saturation"
                text str(round(picker.hsv.saturation * 100)):
                    xalign 1.0
            bar:
                ysize 25
                range 1.0
                value picker.hsv.saturation
                changed _color_picker_hsv_bar_setter(picker, 's')
        vbox:
            hbox:
                xfill True
                text "Value"
                text str(round(picker.hsv.value * 100)):
                    xalign 1.0
            bar:
                ysize 25
                range 1.0
                value picker.hsv.value
                changed _color_picker_hsv_bar_setter(picker, 'v')


screen _fox_color_picker_slider_footer(picker):
    default preview = DynamicDisplayable(_color_picker_preview_cb, picker=picker)

    hbox:
        xfill True

        add preview:
            xsize 100
            ysize 100

        textbutton "Done":
            yalign 1.2
            xalign 1.0
            action Hide()
