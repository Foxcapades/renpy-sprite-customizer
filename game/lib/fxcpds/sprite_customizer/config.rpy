################################################################################
#                                                                              #
#   Sprite Customization Screen GUI Options                                    #
#                                                                              #
################################################################################

# Background color that will show behind the sprite preview side of the screen.
# If you wish to display an image as the background of that pane, changes may be
# made to the `cc_sprite_preview_background` image in the images.rpy file.
define sc.sprite_background_color = "#9cb9cb"

##
# General Control Configuration
##

# Background color that will show behind the sprite customization controls.
define sc.controls_background_color = "#1f1f1f"

# Text color for option group headers.
define sc.control_group_header_color = gui.accent_color

# Text color for string values such as the index number for list options. (The
# number that displays between the arrows).
define sc.control_value_color = "#bbbbbb"

# Text color for the option labels.
define sc.control_label_color = "#bbbbbb"

# Color used for hoverable controls that are not being hovered over.
define sc.control_idle_color = gui.idle_color

# Color used for hoverable controls that are being hovered over.
define sc.control_hover_color = gui.hover_color

# Accent color used for some control components such as the checkmark for
# boolean options.
define sc.control_accent_color = gui.accent_color


##
# Text Input Configuration
##

# Background color for text inputs that are not being hovered over.
define sc.input_background_idle_color = "#eee"

# Background color for text inputs that are being hovered over.
define sc.input_background_hover_color = "#c9c9c9"

# Text color for text inputs.
define sc.input_text_color = "#1f1f1f"

# Text color to display when a text input contains an invalid value.
define sc.input_invalid_color = "#ff0000"


##
# Modals
##

# Color for the solid that covers the screen when a modal is visible
define sc.modal_coverall_color = "#00000088"


##
# Color Picker Configuration
##

# Background color for the color picker display.
define sc.color_picker_background = "#2e2c2c"

# Muted background color for the color picker display.  This is used for
# inactive tabs.
define sc.color_picker_background_muted = "#1f1f1f"

# Text color that will be used for the color picker display.
define sc.color_picker_text_color = "#ddd"

# Muted text color that will be used for the color picker display.  This is used
# for inactive tabs.
define sc.color_picker_text_color_muted = "#bbb"

# Text hover color for the color picker display.
define sc.color_picker_text_color_hover = gui.hover_color