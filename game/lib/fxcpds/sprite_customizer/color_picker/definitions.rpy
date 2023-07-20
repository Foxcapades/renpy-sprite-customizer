init -1 python:
    import math

    def _color_picker_preview_cb(st, at, **kwargs):
        global _cs_color_picker_color
        return (Solid(_cs_color_picker_color), 0.0)


default _cs_color_picker_tab = "HSL"

image _cs_color_picker_coverall = Solid(sc.modal_coverall_color)
image _cs_color_picker_background = Solid(sc.color_picker_background)
image _cs_color_picker_tab_header_active = Solid(sc.control_accent_color)
image _cs_color_picker_tab_header_muted = Transform("_cs_color_picker_tab_header_active", matrixcolor=BrightnessMatrix(-0.2))
