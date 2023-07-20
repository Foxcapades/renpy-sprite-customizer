# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#    Images
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

image cc_gui_option_arrow_right_idle = Transform(
    "lib/fxcpds/sprite_customizer/images/arrow.png",
    matrixcolor=TintMatrix(sc.control_idle_color),
    xsize=50,
    ysize=50
)

image cc_gui_option_arrow_right_hover = Transform(
    "lib/fxcpds/sprite_customizer/images/arrow.png",
    matrixcolor=TintMatrix(sc.control_hover_color),
    xsize=50,
    ysize=50
)

image cc_gui_option_arrow_left_idle = Transform(
    "lib/fxcpds/sprite_customizer/images/arrow.png",
    matrixcolor=TintMatrix(sc.control_idle_color),
    xsize=50,
    ysize=50,
    xzoom=-1.0
)

image cc_gui_option_arrow_left_hover = Transform(
    "lib/fxcpds/sprite_customizer/images/arrow.png",
    matrixcolor=TintMatrix(sc.control_hover_color),
    xsize=50,
    ysize=50,
    xzoom=-1.0
)

image cc_checkbox_blank_idle = Transform(
    "lib/fxcpds/sprite_customizer/images/checkbox_blank.png",
    matrixcolor=TintMatrix(sc.control_idle_color),
    xsize=50,
    ysize=50,
)

image cc_checkbox_blank_hover = Transform(
    "lib/fxcpds/sprite_customizer/images/checkbox_blank.png",
    matrixcolor=TintMatrix(sc.control_hover_color),
    xsize=50,
    ysize=50,
)

image cc_checkbox_check = Transform(
    "lib/fxcpds/sprite_customizer/images/check.png",
    matrixcolor=TintMatrix(sc.control_accent_color),
    xsize=50,
    ysize=50,
)

image cc_checkbox_checked_idle = Composite(
    (50, 50),
    (0, 0), "cc_checkbox_blank_idle",
    (0, 0), "cc_checkbox_check",
)

image cc_checkbox_checked_hover = Composite(
    (50, 50),
    (0, 0), "cc_checkbox_blank_hover",
    (0, 0), "cc_checkbox_check"
)

image cc_color_button_idle = Transform(
    "lib/fxcpds/sprite_customizer/images/color_button_outline.png",
    matrixcolor=TintMatrix(sc.control_idle_color),
    xsize=50,
    ysize=50,
)

image cc_color_button_hover = Transform(
    "lib/fxcpds/sprite_customizer/images/color_button_outline.png",
    matrixcolor=TintMatrix(sc.control_hover_color),
    xsize=50,
    ysize=50,
)

image cc_sprite_preview_background = Solid(sc.sprite_background_color)
