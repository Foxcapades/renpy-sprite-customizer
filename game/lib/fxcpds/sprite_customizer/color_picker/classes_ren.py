from renpy import At, Fixed, Image, InputValue, Transform  # type: ignore
import renpy  # type: ignore
from fox_requirement_ren import fox_require_str
from fox_hex_utils_ren import fox_hex_is_valid
from fox_color_ren import FoxColor, FoxHSV, hex_to_fox_rgb
from screens import _color_picker_square  # type: ignore
from ..options.color_option_ren import SCColorOption

"""renpy
init python:
"""

import pygame


class ColorPicker(renpy.Displayable):
    """
    Visual Color Picker Displayable
    ===============================

    Class Properties
    ----------------
    WHITE : FoxHSV
        Static instance of white in HSV.  Used when calculating selected color.
    BLACK : FoxHSV
        Static instance of black in HSV.  Used when calculating selected color.
    RED : FoxHSV
        Static instance of red in HSV.  Used as a base for the color picker
        shader transform.
    SELECT : Image
        Selector image.
    HI_SPD : float
        High speed rerender interval in seconds.

    Instance Properties
    -------------------
    hsl : FoxHSL
        Currently selected color in HSL.
    hsv : FoxHSV
        Currently selected color in HSV.
    rgb : FoxRGB
        Currently selected color in RGB.
    """

    WHITE  = FoxHSV.white()
    BLACK  = FoxHSV.black()
    RED    = FoxHSV(0, 1.0, 1.0)
    SELECT = Image("lib/fxcpds/sprite_customizer/color_picker/selector.png")
    HI_SPD = 0.01

    def __init__(
        self,
        width: int,
        height: int,
        option: SCColorOption,
        start: FoxColor = FoxHSV(0, 1.0, 1.0),
        **kwargs
    ) -> None:
        """
        Initializes a new ColorPicker instance with the given arguments.

        Arguments
        ---------
        width : int
            Width of the color picker displayable.
        height : int
            Height of the color picker displayable.
        """
        super(ColorPicker, self).__init__(**kwargs)

        start = start.clone()

        self.hsl = start.to_hsl()
        self.hsv = start.to_hsv()
        self.rgb = start.to_rgb()

        self._color = self.hsv
        self._width = width
        self._height = height
        self._picker = Transform('#fff', xysize=(width, height))
        self._option = option

        self._dragged = False

        self._last_updated = 0.0

    @property
    def color(self) -> FoxColor:
        return self._color

    def set_color(self, color: FoxColor) -> None:
        self._color = color
        self.hsl = color.to_hsl()
        self.hsv = color.to_hsv()
        self.rgb = color.to_rgb()
        self._option.set_selection(self.rgb.hex)

    @property
    def rotation(self) -> int:
        return self._color.hsv[0]

    def set_rotation(self, rotation: int) -> None:
        self.hsv.set_hue(rotation)
        self.set_color(self.hsv)
        renpy.restart_interaction()

    def event(self, ev: pygame.event.Event, x: float, y: float, st: float) -> None:
        # Is it a primary mouse button click event?
        click = ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1

        # Is it a mouse move event?
        move = ev.type == pygame.MOUSEMOTION

        # Is it a primary mouse button release event?
        release = ev.type == pygame.MOUSEBUTTONUP and ev.button == 1

        # Bail if the event isn't relevant to us.
        if not (click or move or release):
            return

        # Figure out what percent of the square the mouse cursor is at (and if
        # it's even above the square in the first place)
        x_percent = x / self._width
        y_percent = y / self._height

        # If the x and y percents are in the 0-1 range, then the mouse cursor is
        # in the picker square
        hovered = 0.0 <= x_percent <= 1.0 and 0.0 <= y_percent <= 1.0

        # Flip the y percent to use it as the raw HSV color value
        y_percent = 1.0 - y_percent

        # If the user has clicked down the primary mouse button while the mouse
        # cursor is in the picker square.
        if click and hovered:
            self._dragged = True
            self.hsv.set_saturation(self._clamp(x_percent))
            self.hsv.set_value(self._clamp(y_percent))
            self.set_color(self.hsv)
            renpy.restart_interaction()

        # If the mouse is still clicked and is being moved, or "dragged" around
        # the screen.
        elif move and self._dragged:
            # Keep tracking even when we aren't in the square range because the
            # UX gets weird around the edges otherwise.
            self.hsv.set_saturation(self._clamp(x_percent))
            self.hsv.set_value(self._clamp(y_percent))

            if st - self._last_updated >= self.HI_SPD:
                self._last_updated = st
                self.set_color(self.hsv)
                renpy.restart_interaction()

        # If the mouse button was just released, end the dragging and set the
        # final color selection.
        elif release:
            self._dragged = False
            self.set_color(self.hsv)
            renpy.restart_interaction()

    def render(self, width, height, st, at) -> renpy.Render:
        view = renpy.Render(self._width, self._height)

        # Apply the shader to our picker square to get a new, transformed
        # displayable.
        picker = At(self._picker, _color_picker_square(self.RED.rotate_hue_by_degrees(self.rotation)))

        # Move the color selector around the screen by using the HSV values as
        # the position values.
        select = Transform(
            self.SELECT,
            anchor=(0.5, 0.5),
            xpos=self.hsv.saturation,
            ypos=1.0 - self.hsv.value,
        )

        # Assemble the picker pane.
        pane = Fixed(picker, select, xysize=(self._width, self._height))

        # RENDER THAT THING
        rend = renpy.render(pane, self._width, self._height, st, at)

        # Put that render into our view.
        view.blit(rend, (0, 0))

        renpy.redraw(self, self.HI_SPD)

        return view

    def visit(self) -> list[renpy.Displayable]:
        return [self._picker, self.SELECT]

    def update_position(self):
        h, s, v = self._color.hsv
        self.rotation = h
        self._xpos = s
        self._ypos = 1.0 - v

    @staticmethod
    def _clamp(percent: float) -> float:
        if percent > 1.0:
            return 1.0
        elif percent < 0.0:
            return 0.0
        else:
            return percent


class HexInputValue(InputValue):
    def __init__(self, picker: ColorPicker):
        self.default = False
        self._picker = picker
        self._last   = picker._color.hex[1:]
        self._value  = self._last

    def get_text(self) -> str:
        hex = self._picker._color.hex[1:]

        if hex == self._last:
            return self._value
        else:
            self._last = self._value = hex
            return hex

    def set_text(self, text: str):
        if fox_hex_is_valid(text):
            self._value = text

    def enter(self):
        l = len(self._value)

        if l == 3 or l == 6:
            tmp = '#' + self._value
            self._picker.set_color(hex_to_fox_rgb(tmp))

        renpy.restart_interaction()


class StringContainer(object):
    def __init__(self, value: str) -> None:
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def set_value(self, value: str) -> None:
        self._value = fox_require_str("value", value)