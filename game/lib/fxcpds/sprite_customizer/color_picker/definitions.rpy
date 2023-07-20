init -1 python:
    import math

    def _color_picker_preview_cb(st, at, **kwargs):
        global _cs_color_picker_color
        return (Solid(_cs_color_picker_color), 0.0)


default _cs_color_picker_tab = "HSL"

image _cs_color_picker_coverall = Solid("#00000088")
image _cs_color_picker_background = Solid("#2e2c2c")
