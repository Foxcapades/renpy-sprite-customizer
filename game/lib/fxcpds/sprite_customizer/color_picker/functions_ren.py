import renpy  # type: ignore
from classes_ren import ColorPicker

"""renpy
init -2 python:
"""

def _color_picker_preview_cb(st: float, at: float, picker: ColorPicker):
    return (picker.color.hex, 0.01)

def _color_picker_normalize_rgb(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    return (rgb[0]/255, rgb[1]/255, rgb[2]/255)

def _color_picker_rgb_bar_setter(picker: ColorPicker, channel: str):
    def setter(value: int):
        if channel == 'r':
            picker.rgb.set_red(value)
        elif channel == 'g':
            picker.rgb.set_green(value)
        elif channel == 'b':
            picker.rgb.set_blue(value)
        else:
            raise Exception('illegal state')

        picker.set_color(picker.rgb)
        renpy.restart_interaction()


    return setter

def _color_picker_hsv_bar_setter(picker: ColorPicker, channel: str):
    def setter(value: int | float):
        if channel == 'h':
            picker.hsv.set_hue(value)
        elif channel == 's':
            picker.hsv.set_saturation(value)
        elif channel == 'v':
            picker.hsv.set_value(value)
        else:
            raise Exception('illegal state')

        picker.set_color(picker.hsv)
        renpy.restart_interaction()

    return setter

def _color_picker_hsl_bar_setter(picker: ColorPicker, channel: str):
    def setter(value: int | float):
        if channel == 'h':
            picker.hsl.set_hue(value)
        elif channel == 's':
            picker.hsl.set_saturation(value)
        elif channel == 'l':
            picker.hsl.set_lightness(value)
        else:
            raise Exception('illegal state')

        picker.set_color(picker.hsl)
        renpy.restart_interaction()

    return setter
