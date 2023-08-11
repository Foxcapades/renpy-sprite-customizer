define gui.color_picker.bg_muted = '#111111'
define gui.color_picker.bg_normal = '#222222'

define gui.color_picker.text_color_muted = gui.interface_text_color + '7F'
define gui.color_picker.text_color_normal = gui.interface_text_color

define gui.color_picker.text_input_background = '#ffffff'
define gui.color_picker.text_input_text_color = gui.accent_color

define gui.color_picker.tab_marker_muted = gui.hover_muted_color
define gui.color_picker.tab_marker_normal = gui.accent_color

define gui.color_picker.coverall_color = '#ffffff7f'


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
##
##    Color Picker Main Pane
##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

style _fox_color_picker_body:
    xcenter 0.5
    ycenter 0.5
    background None

style _fox_color_picker_picker_body:
    padding (10, 10, 5, 10)
    background gui.color_picker.bg_normal

style _fox_color_picker_slider_body:
    padding (5, 10, 10, 10)
    xsize 410
    ysize 420
    background gui.color_picker.bg_normal


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
##
##    Color Picker Tabs
##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##


style _fox_color_picker_tab:
    padding (12, 5)

style _fox_color_picker_tab_idle:
    is _fox_color_picker_tab
    background gui.color_picker.bg_muted

style _fox_color_picker_tab_selected:
    is _fox_color_picker_tab
    background gui.color_picker.bg_normal

style _fox_color_picker_tab_text:
    size 32

style _fox_color_picker_tab_text_idle:
    is _fox_color_picker_tab_text
    color gui.color_picker.text_color_muted

style _fox_color_picker_tab_text_selected:
    is _fox_color_picker_tab_text
    color gui.color_picker.text_color_normal

style _fox_color_picker_tab_marker:
    padding (12, 0)
    ysize 5

style _fox_color_picker_tab_marker_idle:
    is _fox_color_picker_tab_marker
    background gui.color_picker.tab_marker_muted

style _fox_color_picker_tab_marker_selected:
    is _fox_color_picker_tab_marker
    background gui.color_picker.tab_marker_normal


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
##
##    Color Hex Input
##
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

style _fox_color_picker_hex_input_button:
    ycenter 0.5
    background gui.color_picker.text_input_background
    xsize 155

style _fox_color_picker_hex_input_input:
    color gui.color_picker.text_input_text_color
    size 32
